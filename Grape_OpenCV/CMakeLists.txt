cmake_minimum_required(VERSION 3.1)

project(OpenCV_Test)

set(CMAKE_PREFIX_PATH /home/master/libtorch)

find_package(OpenCV REQUIRED)
find_package(Torch REQUIRED)
find_package(TorchVision REQUIRED) 

add_executable(test hough_circle.cpp)

target_link_libraries(test ${OpenCV_LIBS})
target_link_libraries(test ${TORCH_LIBRARIES})
target_link_libraries(test TorchVision::TorchVision)

set_property(TARGET test PROPERTY CXX_STANDARD 14)

