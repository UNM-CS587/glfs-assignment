# Distributed File System - Part 2

In this assignment, you will extend the lfs code your wrote in the first part of the 
assignment to provide an RPC-based distributed file server and client library. 
Your server and client library will both be written in Python, starting from
the template code provided in [src/glfs-server.py](src/glfs-server.py) 
and [src/glfs.py](src/glfs.py). 

The server process will take a single command line argument, the name of the log
file in which server file information will be stored:

```python3 glfs-server.py logname.log portnumber```

The interface provided to clients by the server, the ``glfs`` interface, is almost 
exactly the LFS interface with the exception of initialization. On startup, the server
will create an LFS object with the specified log file name. Clients, however, will call 
``glfs_init`` and specify the hostname and port number of the server to connect to.
``glfs_init`` will return an opaque handle object to pass to other glfs calls.

## Client-Server Communication
The glfs clients communicate with the glfs server using Google RPC. Specifically, you
will need to create a GRPC protocol specification (an empty one is provided in 
the file ``glfs.proto``) for each of the RPCs that you are implementing, including
describing the relevant arguments. There will be one  FLGS 

## 
## Building and testing infrastructure

Because the LFS assignment code is a mixture of C and Python code, building and testing 
it is somewhat complicated. First:
  1. Edit CMakeLists.txt to set ENABLE_LFS_C_LIBRARY to either "ON" or "OFF" depending on 
     if you plan to implement the library purely in C ("ON") with the provided python 
     interface code tying it to the test cases, or purely in Python ("OFF") if you do not
     plan to write the interface in C.
  2. Run the script `compile.sh` (e.g. by running `./compile.sh` from the command line)
     to download the relevant test submodule and build the initial code and tests. After 
     this is done, you should be able to compile and test simply by running "make" and 
     "make test" in the build directory.
  3. Change to the 'build' directory and run 'make test' to run currently deployed 
     testcases. 

Finally, watch for announcements from me that new testcases are available - when new 
testcases are available, I will tell you the commands to run to update your test 
directory with the new tests.

## On-Disk File System: A Log-Structured File System

Your on-disk file system structures will roughly follow that of the
log-structured file system discussed in class and presented
[here](https://pages.cs.wisc.edu/~remzi/OSTEP/file-lfs.pdf). The specific
format of the log you will used is includd in the proved C, C++, and 
Python files. Specifically
  * On-disk, the first structure in the log is a single checkpoint region.
    The checkpoint contain a disk pointer (a file offset) to the current end 
    of the log as well as pointers to pieces of the inode map. It assumes 
    there are a maximum of 4096 inodes and that each piece of the inode map 
    has 16 entries.

  * After the checkpoint region, the on-disk image just consists of an ever-growing 
    log (i.e., no cleaning). Thus, whenever you write to the disk, you'll write 
    all file system updates to the end of the log, and then update the checkpoint 
    region as need be. For example, if you are adding a new block to a file, you will 
    write the data block, new version of the inode, and a new piece of the inode map 
    to the end of the log; when this write completes, you will update the checkpoint 
    region with the requisite new values. 

  * The inode map is just an array, indexed by inode number. Each entry is a simple 
    4-byte integer, which is just the disk address of the location of the inode in 
    question. It is stored on disk in 16 entry pieces, your LFS code will read any
    valid pieces at startup to consttruct the runtime inode map, and write new fragments 
    of the inode map as part of log writes and updates to the checkpoint region on where
    the current inode map fragments are in the log when updating the checkpoint region
    after a log write.

  * Each inode is simple: a size field (the number of the last byte in the file), a 
    type field (regular or directory), and 14 direct pointers; thus, the maximum file 
    size is 14 times the 4KB block size, or 56 KB.

  * The other structure you'll have to manage on disk are directories. Each directory 
    has an inode, and points to one or more data blocks that contain directory entries. 
    Each entry in the directory is 32 bytes: a name no longer than 28 bytes (including
    a null terminator) and a (4 byte) inode number. When a new directory is created, 
    it should contain two entries: the name `.` (dot), which refers to this new 
    directory's inode number, and `..` (dot-dot), which refers to the parent directory's 
    inode number. For directory entries that are not yet in use (in an allocated 4-KB 
    directory block), the inode number should be set to -1. This way, utilities can 
    scan through the entries to check if they are valid.

When your library is initialized, it is passed the name of the file system image file
storing the log. If this file does not exist, the file server should create
it, and initialize it properly, and force it to disk. Such initialization includes 
creating the checkpoint region, the initial inode map, and creating a single root 
directory with proper `.` and `..` entries. The root inode number should be 0.

When booting off of an existing image, your server should read in the checkpoint region 
(and keep an in-memory version of it), as well as the entire inode map and keep it 
in-memory, too.


## File System Image Library

If implemented in C, the file system image library should export the following interfaces
as defined in lfs.h:

- `int LFS_Init(LFS_Handle_t *handle, char *filename)`: `LFS_Init()` takes the name 
of a file system image file and either opens the provided file system image or, if 
the provided file does not exist, initializes an empty file system image. The 
handle is updated to initialize any relevant (student-defined) data for implementing
the provided calls below. Failure mode: cannot open/create provided filename.
and port number and uses those to find the server exporting the file system.
- `int LFS_Lookup(LFS_Handle_t *handle, int pinum, char *name)`: `LFS_Lookup()` takes the parent
inode number (which should be the inode number of a directory) and looks up
the entry `name` in it. The inode number of `name` is returned. Success: 
return inode number of name; failure: return -1. Failure modes: invalid pinum,
name does not exist in pinum.
- `int LFS_Stat(LFS_Handle_t *handle, int inum, int *type, int *size): Returns basic information
information about the file specified by inum. Upon success, return 0,
otherwise -1. Failure modes: inum does not exist. 
- `int LFS_Write(LFS_Handle_t *handle, int inum, char *buffer, int block)`: `LFS_Write()` writes a
block of size 4096 bytes at the block offset specified by `block`. Returns 0
on success, -1 on failure. Failure modes: invalid inum, invalid block, not a
regular file (because you can't write to directories).
- `int LFS_Read(LFS_Handle_t *handle, int inum, char *buffer, int block)`: `LFS_Read()` reads
a block specified by `block` into the buffer from file specified by
`inum`. The routine should work for either a file or directory;
directories should return data in the format specified by
`LFS_DirEnt_t`. Success: 0, failure: -1. Failure modes: invalid inum,
invalid block. 
- `int LFS_Creat(LFS_Handle_t *handle, int pinum, int type, char *name)`: `LFS_Creat()` makes a
file (`type == LFS_REGULAR_FILE`) or directory (`type == LFS_DIRECTORY`)
in the parent directory specified by `pinum` of name `name`. Returns 0 on
success, -1 on failure. Failure modes: pinum does not exist, or name is too
long. If `name` already exists, return success (think about why in terms of 
RPC semantics).
- `int LFS_Unlink(LFS_Handle_t *handle, int pinum, char *name)`: `LFS_Unlink()` removes the file or
directory `name` from the directory specified by `pinum`. 0 on success, -1
on failure. Failure modes: pinum does not exist, directory is NOT empty. Note
that the name not existing is NOT a failure by our definition (think about why
in terms of later RPC semantics). 
- `int LFS_Close(LFS_Handle_t *handle)`: `LFS_Close()` just tells the library to 
force all of its data structures to disk, release any allocated data in the 
provided LFS Handle, and close the log file.

## Relevant Chapters

Read these:
- [Log-structured File System](https://pages.cs.wisc.edu/~remzi/OSTEP/file-lfs.pdf)
- [Distributed Systems](https://pages.cs.wisc.edu/~remzi/OSTEP/dist-intro.pdf)
- [Distributed File System: NFS](https://pages.cs.wisc.edu/~remzi/OSTEP/dist-nfs.pdf)
