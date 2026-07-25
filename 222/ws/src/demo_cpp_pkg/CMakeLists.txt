cmake_minimum_required(VERSION 3.8)
project(demo_cpp_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
message(STATUS ${rclcpp_INCLUDE_DIRS}) #头文件及rclcpp依赖的头文件
message(STATUS ${rclcpp_LIBARARIES}) #库文件和eclcpp依赖的库文件
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)
include_directories(include) #包含头文件 
add_executable(cpp_node src/cpp_node.cpp)
add_executable(person_node src/person_node.cpp)
add_executable(learn_auto src/learn_auto.cpp)
add_executable(learn_shared_ptr src/learn_shared_ptr.cpp)
add_executable(learn_lambda src/learn_lambda.cpp)
add_executable(learn_functional src/learn_functional.cpp)
add_executable(learn_thread src/learn_thread.cpp)

find_package(rclcpp REQUIRED) #查找头文件和库文件

ament_target_dependencies(cpp_node rclcpp) #将rclcpp的头文件和库文件链接到cpp_node
ament_target_dependencies(person_node rclcpp) #将rclcpp的头文件和库文件链接到person_node

install(TARGETS
  cpp_node person_node learn_auto learn_shared_ptr learn_lambda learn_functional learn_thread
  DESTINATION lib/${PROJECT_NAME}
  )



if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
