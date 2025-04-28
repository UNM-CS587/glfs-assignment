"""The Python implementation of the glfs client."""

import logging

import grpc
import glfs_pb2
import glfs_pb2_grpc

class GLFS_Log:
    def __init__(self, hostname, port):
        channel = grpc.insecure_channel(hostname + ":" + str(port))
        self._stub = glfs_pb2_grpc.glfsStub(channel)

    def lookup(self, pfd, filename):
        response = self._stub.lookup(glfs_pb2.lookupRequest(pinum=pfd, name=filename))
        return response.fd

    def stat(self, fd):
        response = self._stub.stat(glfs_pb2.statRequest(inum=fd))
        return (response.type, response.size)

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
