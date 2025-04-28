# Code to interface the C LFS implementation with the python test code
# For C implementations, we use the Python ctypes module to directly interface 
# to the underlying C code loaded as a shared library.
from ctypes import *

LFS_REGULAR_FILE = 1
LFS_DIRECTORY = 0

class LFS_Log:
    # Open the log file and define any internal state
    def __init__(self, filename):
        self.lfslib = cdll.LoadLibrary("liblfs.so")
        # We allocate lots of memory for the handle as a bytearray and pass its 
        # address to LFS init, assuming it is large enough.
        self.handle = create_string_buffer(4096*8)
        self.lfslib.LFS_Init.argtypes=c_char_p,c_char_p
        ret = self.lfslib.LFS_Init(self.handle, filename.encode('utf-8'))
        if ret != 0:
            raise RuntimeError("LFS_Init returned " + str(ret))

    def __del__(self):
        self.lfslib.LFS_Close(self.handle)

    # Lookup a name in a directory given by inode number returning an inode
    def lookup(self, pinum, name):
        ret = self.lfslib.LFS_Lookup(self.handle, pinum, name.encode('utf-8'))
        # Translate the error into a generic exception
        if ret < 0:
            raise RuntimeError("LFS_Lookup returned " + str(ret))
        return ret

    # Stat an inode, returning a tuple of the type and size
    def stat(self, inum):
        type = c_int(0)
        size = c_int(0)
        ret = self.lfslib.LFS_Stat(self.handle, inum, byref(type), byref(size))
        if ret < 0:
            raise RuntimeError("LFS_Stat returned " + str(ret))
        return (type.value, size.value)

    # Write to an inode, throwing an exception on failure
    def write(self, inum, buffer, block):
        self.lfslib.LFS_Write.argtypes=c_char_p,c_int,c_char_p,c_int
        ret = self.lfslib.LFS_Write(self.handle, inum, buffer, block)
        if ret < 0:
            raise RuntimeError("LFS_Write returned " + str(ret))

    # Read from an inode, returning a bytes object
    def read(self, inum, block):
        buffer = create_string_buffer(4096)
        ret = self.lfslib.LFS_Read(self.handle, inum, buffer, block)
        if ret < 0:
            raise RuntimeError("LFS_Read returned " + str(ret))
        return bytes(buffer)

    # Create a file or directory with a given name in a directory
    def creat(self, pinum, type, name):
        ret = self.lfslib.LFS_Creat(self.handle, pinum, type, name.encode('utf-8'))
        # Translate the error into a generic exception
        if ret != 0:
            raise RuntimeError("LFS_Creat returned " + str(ret))

    # Unlink a named file or directory with a given name in a directory
    def unlink(self, pinum, name):
        ret = self.lfslib.LFS_Unlink(self.handle, pinum, name.encode('utf-8'))
        # Translate the error into a generic exception
        if ret != 0:
            raise RuntimeError("LFS_Unlink returned " + str(ret))
