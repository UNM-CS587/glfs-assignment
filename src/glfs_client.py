"""The Python implementation of the GRPC helloworld.Greeter client."""

import logging

import grpc
import helloworld_pb2
import helloworld_pb2_grpc

class GLFS_Log:
    def __init(self, hostname, port)__:
        _channel = grpc.insecure_channel(hostname + ":" + port)
        _stub = glfs_pb2_grpc.grpcStub(_channel)

    def lookup(filename):
        response = _stub.lookup(glfs_pb2.filename(name=filename)
        return response.fd

    def stat(inum):
        response = _stub.stat(glfs_pb2.fd(fd=inum))
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
