cmake_minimum_required(VERSION 2.8)
# project(ydlidar_sdk C CXX)

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
##################################################
# Add c++11 Flag
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

##########################################################
IF (CMAKE_SYSTEM_NAME MATCHES "Linux")
    MESSAGE(STATUS "Current platform: Linux")
	#Linux add -fPIC
	add_compile_options(-fPIC)
ENDIF (CMAKE_SYSTEM_NAME MATCHES "Linux")
#or
#set(CMAKE_POSITION_INDEPENDENT_CODE ON)

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
include_directories(core)
include_directories(src)

#############################################################################
# addd subdirectory
add_subdirectory(core)
add_subdirectory(src)


#############################################################################
# PARSE libraries
include(common/ydlidar_parse)
include_directories(${SDK_INCS})
include_directories(${CMAKE_CURRENT_BINARY_DIR})
########################################################
## Create configure file for inclusion in library
# configure_file("${CMAKE_CURRENT_SOURCE_DIR}/ydlidar_config.h.in"
#   "${CMAKE_CURRENT_BINARY_DIR}/ydlidar_config.h" )
# set(GENERATED_HEADERS ${CMAKE_CURRENT_BINARY_DIR}/ydlidar_config.h )


#############################################################################
# SET(LIBRARY_OUTPUT_PATH ${CMAKE_BINARY_DIR})
#############################################################################################
#shared library
# if(BUILD_SHARED_LIBS)
# ydlidar_add_library(${YDSDK_NAME} SHARED ${SDK_SOURCES} ${SDK_HEADERS} ${GENERATED_HEADERS})
# else()
# ydlidar_add_library(${PROJECT_NAME} STATIC ${SDK_SOURCES} ${SDK_HEADERS} ${GENERATED_HEADERS})
# endif()

# target_link_libraries(${YDSDK_NAME} ${SDK_LIBS})

# append path
# list(APPEND SDK_INCS ${CMAKE_INSTALL_PREFIX}/include/src
#     ${CMAKE_INSTALL_PREFIX}/include)

###############################################################################
# install package
# string(TOUPPER ${YDSDK_NAME} PROJECT_PKG_NAME)
