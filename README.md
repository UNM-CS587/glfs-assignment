# Distributed File System - Part 2

In this assignment, you will extend the lfs code your wrote in the first part of the 
assignment to provide an RPC-based distributed file server and client library. 
Your server and client library will both be written in Python, starting from
the template code provided in [src/glfs_server.py](src/glfs_server.py) 
and [src/glfs_client.py](src/glfs_client.py). 

The server process will take a single command line argument, the name of the log
file in which server file information will be stored:

```python3 glfs_server.py logname.log portnumber```

The interface provided to clients by the server, the ``glfs`` interface, is almost 
exactly the LFS interface with the exception of initialization. On startup, the server
will create a GLFS Servicer object with the specified log file name. The server object will
use the existing LFS_Log object (from the relevant lfs.py) to open the appropriate log
file on the server. Clients will create a GLFS_Log object that includes he hostname and 
port number of the server to connect to - the GLFS_Log object has the same interface as
the LFS_Log object from the previous assignment - the difference it that GLFS_Log does 
all operations by connecting to the server over GPRC.

## Client-Server Communication
The glfs clients communicate with the glfs server using Google RPC. Specifically, you
will need to create a GRPC protocol specification (a start at one is provided in 
the file ``glfs.proto``) for each of the RPCs that you are implementing, including
describing the relevant arguments. I have already provided you the basic skeleton of
an GRPC definition for this assigment that includes the lookup and stat functions; you 
will need to enhance it to define other request and response types and other entry points.

## 
Read these:
- [Distributed Systems](https://pages.cs.wisc.edu/~remzi/OSTEP/dist-intro.pdf)
- [Distributed File System: NFS](https://pages.cs.wisc.edu/~remzi/OSTEP/dist-nfs.pdf)
