# CMake Specification for CS587 LFW Assignment

# Basic CMake Setup
cmake_minimum_required(VERSION 3.12)

project(UNM-CS887-LFS)

enable_testing()

# Students will need to use either lfs-c.py or lfs-py.py in src/
# as the interface code to the test cases. The C code is interfaced to
# python using lfs-c.py if ENABLE_LFS_C_LIBRARY is "ON". If ENABLE_LFS_C_LIRARY
# is "OFF", lfs-py.py is used instead.

# The student should set this variable appropriately.
set(ENABLE_LFS_C_LIBRARY ON)

add_subdirectory(src)

# And the directory that incldues python test code as a submodule
add_subdirectory(test)
