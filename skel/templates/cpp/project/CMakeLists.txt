cmake_minimum_required(VERSION 3.16)
project({{project}})

if (NOT CMAKE_BUILD_TYPE)
    message(STATUS "Setting build type to Debug")
    set(CMAKE_BUILD_TYPE "Debug")
endif()

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

find_package(Boost REQUIRED COMPONENTS program_options)

add_executable({{project}} main.cpp)
target_link_libraries({{project}} Boost::program_options)
