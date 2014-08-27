cmake_minimum_required (VERSION 2.8)
project (libsaps)
add_executable(testsaps testsaps.cpp)
add_library(saps param.cpp saps.cpp)
TARGET_LINK_LIBRARIES(testsaps itpp saps)

enable_testing()
add_test(testsaps_runs testsaps NameFileResult=/tmp/testitpp Hi=Hallo)
