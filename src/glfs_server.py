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
        self._log = lfs.LFS_Log(logfile)

    def lookup(self, request, context):
        try:
            ret = self._log.lookup(request.pinum,request.name)
        except:
            ret = -1
        return glfs_pb2.genericResponse(val = ret)
    
    def stat(self, request, context):
        try:
            s = self._log.stat(request.inum)
            response = glfs_pb2.statResponse(success=0, type = s[0], size = s[1])
        except:        
            response = glfs_pb2.statResponse(success=-1, type = -1, size = 0)
        return response
                                
    # Add additional GRPC server methods here. The above is a pretty good template
    # for what they should generally look like

def create_server(filename, port):
        servicer = GLFSServicer(filename)
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        glfs_pb2_grpc.add_glfsServicer_to_server(servicer, server)
        server.add_insecure_port("[::]:" + str(port))
        print("Server created with logfile" + filename + " listening on " + str(port))
        return server

# This is used if you want to run the server standalone. The test cases 
# start and stop their own server using the create server function above.
if __name__ == "__main__":
    logging.basicConfig()
    args = sys.argv[1:]
    server = create_server(args[0], args[1])
    server.start()
    server.wait_for_termination()
