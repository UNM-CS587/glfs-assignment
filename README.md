# Distributed File System - Part 2

In this assignment, you will extend the lfs code your wrote in the first part of the 
assignment to provide an RPC-based distributed file server and client library. 
Your server and client library will both be written in Python, starting from
the template code provided in [src/glfs_server.py](src/glfs_server.py),
[src/glfs_client.py](src/glfs_client.py), and [src/glfs.proto](src/glfs.proto). 

The server process will take a single command line argument, the name of the log
file in which server file information will be stored:

```python3 glfs_server.py logname portnumber```

The interface provided to clients by the server, the ``glfs`` interface, is almost 
exactly the LFS interface with the exception of initialization. On startup, the server
creates a GLFS Servicer object with the specified log file name and listens for GRPC
connections on the specified port number. The server object will use the existing LFS_Log 
object (from lfs.py) to open the appropriate log file on the server using your LFS code. 
Clients will create a GLFS_Log object using the hostname and port number of the server 
to connect to - the GLFS_Log object has the same interface as the LFS_Log object from 
the previous assignment - the difference it that GLFS_Log does all operations by connecting 
to the server over GPRC. The pre-supplied python server and client files include the setup
and skeleton code for this purpose.

## Client-Server Communication

The glfs clients communicate with the glfs server using Google RPC. Specifically, you
will need to create a GRPC protocol specification (a start at one is provided in 
the file ``glfs.proto``) for each of the RPCs that you are implementing, including
describing the relevant arguments. Arguments are specified as Google Protocol Buffer 
objects. I have already provided you the basic skeleton of an GRPC definition for this 
assigment that includes the lookup and stat functions; you will need to enhance it to 
define other request and response types and other entry points. For more information on
Google RPC and Google Protocol Buffer specifications, start here:
  - [Google RPC in Python](https://grpc.io/docs/languages/python/basics/)
  - [Google Protocol Buffers](https://protobuf.dev/overview/)

## Compiling and Testing the Project

Like the previous project, this project support a combination of C and Python code. 
To compile and test the project, do the following:
1. Add your completed LFS code from assignment 2 to this project, (e.g. put your version
of [src/lfs_impl.c](src/lfs_impl.c), [src/lfs_impl.h](src/lfs_impl.h), 
and/or [src/lfs-py.py](src/lfs-py.py)) in place.
2. If using a python-only implementation of LFS, change the top-level CMakeFile.txt to 
disable C compilation as in the previous assignment.
3. Run ``compile.sh`` to set up the compilation environment for your program and perform
an initial build.
4. Modify [src/glfs_server.py](src/glfs_server.py), [src/glfs_client.py](src/glfs_client.py), 
and [src/glfs.proto](src/glfs.proto) to define the rest of the GLFS interface and implement
the remaining client and server entry points, using the examples for ``lookup`` and ``stat`` 
as guidance. Note that the build system will automatically run the GRPC protocol compiler 
to generate client and server stubs from ``glfs.proto``; you do not need to do so manually.
5. In the build directory, run ``make`` and ``make test`` to run all test cases. Any error output
will be in the relevant log files.
