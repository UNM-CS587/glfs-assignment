# We use the Python ctypes module to define the binary formats of
# the data that goes into the log. As they're defined with python fields,
# after they're initialized, you can just use the fields and python handles
# the interpretation to C binary format.
#
# To use these for I/O, you'll use python binary files.
# For writing them, open a file for writing in binary mode 
# and use the write method of the structure, e.g.:
#
# f = open(filename, "wb")
# f.write(checkpoint)
#
# For reading them, ooen the file for reading in binary mode
# and use the readinto method of a file, e.g.:
# f = open(filename "rb")
# inode = LFS_Inode()
# f.readinto(inode)

from ctypes import *

class LFS_Checkpoint(Structure):
    _fields_ = [ ("loglen", c_int), ("imapents", c_int * 256) ]

LFS_InodeMapEntry = c_int * 16

class LFS_DirEnt(Structure):
    _fields_ = [ ("name", c_char * 28), ("inum", c_int) ]

class LFS_DirBlock(Structure):
    _fields_ = [ ("entries", LFS_DirEnt * 128) ]

class LFS_Inode(Structure):
    _fields_ = [ ("len", c_int), ("type", c_int), ("blockaddr", c_int * 14) ]

LFS_REGULAR_FILE = 1
LFS_DIRECTORY = 0

class LFS_Log:
    # Open the log file and define any internal state
    def __init__(self, filename):
        return

    # Flush and close the log file and any other internal state
    def __del__(self):
        return

    # Stat an inode, returning a tuple of the type and size
    def lookup(self, pinum, name):
        # Lookup a name in a parent inode, returning the inode number
        raise NotImplementedError()

    # Stat an inode, returning a tuple of the type and size
    def stat(self, inum):
        raise NotImplementedError()

    # Write to an inode, throwing an exception on failure. Note that buffer is a 
    # bytes object of length 4096, not a string.
    def write(self, inum, buffer, block):
        raise NotImplementedError()

    # Read from an inode, returning a bytes object of length 4096
    def read(self, inum, block):
        raise NotImplementedError()

    # Create a file or directory with a given name in a directory
    def creat(self, pinum, type, name):
        raise NotImplementedError()

    # Remove a file or directory with a given name in a directory
    def unlink(self, pinum, name):
        raise NotImplementedError()
