cmake_minimum_required(VERSION 3.11)
project(skel)

if (NOT CMAKE_BUILD_TYPE)
    message(STATUS "Setting build type to Debug")
    set(CMAKE_BUILD_TYPE "Debug")
endif()

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Boost REQUIRED COMPONENTS program_options)

add_executable(skel main.cpp)
target_link_libraries(skel Boost::program_options)
