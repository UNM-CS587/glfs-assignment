#!/bin/bash
# Get the testing submodule
git submodule init
git submodule update -r

# Use pip to install pytest-cmake
pip install -U --break-system-packages pytest pytest-cmake grpcio grpcio-tools

# Build everything
mkdir build
cmake -B build
cmake --build build
