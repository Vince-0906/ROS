# Copyright(c) 2020 eaibot limited.
cmake_minimum_required(VERSION 3.5)
project(ydlidar C CXX)

##################ros2#############################################
# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()



# add_subdirectory(sdk)
#########################################################
set(YDLIDAR_SDK_VERSION_MAJOR 1)
set(YDLIDAR_SDK_VERSION_MINOR 2)
set(YDLIDAR_SDK_VERSION_PATCH 9)
set(YDLIDAR_SDK_VERSION ${YDLIDAR_SDK_VERSION_MAJOR}.${YDLIDAR_SDK_VERSION_MINOR}.${YDLIDAR_SDK_VERSION_PATCH})

set(YDSDK_NAME "ydsdk")
##########################################################
# Detect wordsize:
IF(CMAKE_SIZEOF_VOID_P EQUAL 8)  # Size in bytes!
	SET(CMAKE_MRPT_WORD_SIZE 64)
ELSE()
	SET(CMAKE_MRPT_WORD_SIZE 32)
ENDIF()

#####################################################
# add cmake module path
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
set(SDK_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}")
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
#############################################################################
# include cmake file
include(common/ydlidar_base)


############################################################################
# include headers
include_directories(.)
include_directories(sdk/core)
include_directories(sdk/src)
include_directories(sdk/core/common)

#############################################################################
# addd subdirectory
add_subdirectory(sdk/core)
add_subdirectory(sdk/src)


#############################################################################
# PARSE libraries
include(common/ydlidar_parse)
include_directories(${SDK_INCS})
include_directories(${CMAKE_CURRENT_BINARY_DIR})

####################find package#####################################
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rmw REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(visualization_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(std_srvs REQUIRED)

############## YDLIDAR SDK START#####################################
#find ydlidar_sdk package
# find_package(ydlidar_sdk REQUIRED)
############## YDLIDAR SDK END#####################################

#Include directories
include_directories(
  ${PROJECT_SOURCE_DIR}
  ${PROJECT_SOURCE_DIR}/sdk
  ${PROJECT_SOURCE_DIR}/src
  ${YDLIDAR_SDK_INCLUDE_DIRS})

#link library directories
link_directories(${YDLIDAR_SDK_LIBRARY_DIRS})

#---------------------------------------------------------------------------------------
# generate excutable and add libraries
#---------------------------------------------------------------------------------------
add_executable(${PROJECT_NAME}_node
    src/${PROJECT_NAME}_node.cpp ${SDK_SOURCES} ${SDK_HEADERS} ${GENERATED_HEADERS})
# add_dependencies(${PROJECT_NAME}_node ydsdk)
#---------------------------------------------------------------------------------------
# link libraries
#--------------------------------------------------------------------------------------
ament_target_dependencies(${PROJECT_NAME}_node
    "rclcpp"
    "sensor_msgs"
    "visualization_msgs"
    "geometry_msgs"
    "std_srvs"
    )

target_link_libraries(${PROJECT_NAME}_node
    ${YDLIDAR_SDK_LIBRARIES})

#---------------------------------------------------------------------------------------
# generate excutable and add libraries
#---------------------------------------------------------------------------------------
add_executable(${PROJECT_NAME}_client
    src/${PROJECT_NAME}_client.cpp)
#---------------------------------------------------------------------------------------
# link libraries
#--------------------------------------------------------------------------------------
ament_target_dependencies(${PROJECT_NAME}_client
    "rclcpp"
    "sensor_msgs"
    "visualization_msgs"
    "geometry_msgs"
    "std_srvs"
    )

#---------------------------------------------------------------------------------------
# Install
#---------------------------------------------------------------------------------------
install(TARGETS
    ${PROJECT_NAME}_node ${PROJECT_NAME}_client
    DESTINATION lib/${PROJECT_NAME})

install(DIRECTORY launch params startup config
    DESTINATION share/${PROJECT_NAME})

if(BUILD_TESTING)
    find_package(ament_lint_auto REQUIRED)
    ament_lint_auto_find_test_dependencies()
endif()

ament_package()

