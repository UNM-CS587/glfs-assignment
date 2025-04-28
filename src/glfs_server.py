# Basic packages to support a simple GRPC server

import logging
from concurrent import futures
import grpc
import glfs_pb2
import glfs_pb2_grpc
import sys

# The LFS pacakge we're using to implement the log
import lfs

class GLFSServicer(glfs_pb2_grpc.glfsServicer):
    def __init__(self, logfile):
        _log = lfs.LFS_Log(logfile)

    def lookup(self, request, context):
        inum=_log.lookup(request.pinum,request.name)
        return glfs_pb2.lookupResponse(inum)
    
    def stat(self, request, context):
        s = _log.stat(request.inum)
        response = glfs.pb_2.fstat(type = s[0], size = s[1])
                                
    # Add additional GRPC server methods here

def serve(filename, port ):
        servicer = GLFSServicer(filename)
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        hglfs_pb2_grpc.add_GLFSServicer_to_server(servicer, server)
        server.add_insecure_port("[::]:" + port)
        print("Server started with logfile" + filename + " listening on " + port)
        server.start()
        server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig()
    args = sys.argv[1:]
    serve(args[0], args[1])