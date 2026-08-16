---
tags:
  - ROS2
---
# 修改日志
```bash
export RCUTILS_CONSOLE_OUTPUT_FORMAT=[{function_name}:{line_number}]:{message}
```

# cmake
```bash
cmake .
make
```
# PYTHON
### 功能包创建
```bash
ros2 pkg create --build-type ament_python --license Apache-2.0 <功能包名>
```
# C++
## 功能包创建
```bash
ros2 pkg create --build-type ament_cmake --license Apache-2.0 <功能包名>
```
# 通用
## 构建功能包
```bash
colcon build
```

## 安装环境变量
```bash
source install/setup.bash
```

## 运行
```bash
ros2 run <功能包名> <可执行文件名>
```

## 查看服务
```bash
ros2 service list -t
```

## 查看参数

```bash
ros2 param list
```

## 详细参数查询
```bash
ros2 param describe /turtlesim background_r
/turtlesim为<节点名>
background_r为<参数名>
```

## 当前参数值查询
```bash
ros2 param get /turtlesim background_r
```

## 当前参数值修改
```bash
ros2 param set /turtlesim background_r 255
```

## 导出参数文件
```bash
ros2 param dump /turtlesim > turtlesim_param.yaml
```

## 使用参数启动

```bash
ros2 run turtlesim turtlesim_node --ros-args --params-file turtlesim_param.yaml 
```

## 查看节点
```bash
ros2 node list
```

## 节点信息查询
```bash
ros2 node info 节点名
```

## 输出节点信息
```bash
ros2 topic echo 节点名
```

## 输出节点参数
```bash
ros2 interface show 节点参数
```

## 手动发布节点
```bash
ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.5, y: 0.0} , angular: {z: 0.0}}"
/turtle1/cmd_vel为节点名
geometry_msgs/msg/Twist为节点参数
"{linear: {x: 0.5, y: 0.0} , angular: {z: 0.0}}"为节点参数内容
注意yaml格式
```

## 手动调用服务
```bash
ros2 service call /spawn turtlesim/srv/Spawn "{}"
/spawn为<服务名字>
turtlesim/srv/Spawn为<消息接口>
"{}"为<请求数据>
```

## 直接使用ROS2可视化工具
```bash
rqt
```

---

📑 [返回笔记索引](../README.md#笔记索引)
