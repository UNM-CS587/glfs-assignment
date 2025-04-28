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
Read these:
- [Distributed Systems](https://pages.cs.wisc.edu/~remzi/OSTEP/dist-intro.pdf)
- [Distributed File System: NFS](https://pages.cs.wisc.edu/~remzi/OSTEP/dist-nfs.pdf)
