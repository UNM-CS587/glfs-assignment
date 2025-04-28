include_directories(${CMAKE_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR})

if (ENABLE_LFS_C_LIBRARY)
    add_library(lfs SHARED
                lfs_impl.c)
    add_custom_command(OUTPUT ${CMAKE_CURRENT_LIST_DIR}/lfs.py
                       MAIN_DEPENDENCY ${CMAKE_CURRENT_LIST_DIR}/glfs-py.py)
    configure_file(lfs-c.py lfs.py @ONLY)
else (ENABLE_LFS_C_LIBARRY)
    configure_file(lfs-py.py lfs.py @ONLY)
endif (ENABLE_LFS_C_LIBRARY)

# Protobuf
set(protobuf_MODULE_COMPATIBLE TRUE)
find_package(Protobuf CONFIG REQUIRED)
message(STATUS "Using protobuf ${protobuf_VERSION}")

# Protobuf-compiler
set(_PROTOBUF_PROTOC $<TARGET_FILE:protobuf::protoc>)

 # gRPC
find_package(gRPC CONFIG REQUIRED)
message(STATUS "Using gRPC ${gRPC_VERSION}")

 # Proto file
get_filename_component(glfs_proto "glfs.proto" ABSOLUTE)
get_filename_component(glfs_proto_path "${glfs_proto}" PATH)

# Generated sources
set(glfs_grpc_src_py "${CMAKE_CURRENT_BINARY_DIR}/glfs_pb2_grpc.py")
set(glfs_proto_src_py "${CMAKE_CURRENT_BINARY_DIR}/glfs_pb2.py")
set(glfs_proto_src_pyi "${CMAKE_CURRENT_BINARY_DIR}/glfs_pb2.pyi")

find_package(PythonInterp REQUIRED)
find_package(Python3 REQUIRED)
add_custom_command(
    OUTPUT "${glfs_grpc_src_py}" "${glfs_proto_src_py}" "${glfs_proto_src_pyi}"
    COMMAND python3 
    ARGS -m  grpc_tools.protoc
      -I "${glfs_proto_path}"
      --python_out "${CMAKE_CURRENT_BINARY_DIR}"
      --pyi_out "${CMAKE_CURRENT_BINARY_DIR}"
      --grpc_python_out "${CMAKE_CURRENT_BINARY_DIR}"
      "${glfs_proto}"
    DEPENDS "${glfs_proto}")

# invoke custom command
add_custom_target ( glfs ALL
                    DEPENDS ${glfs_grpc_src_py} ${lfs_py} lfs)
