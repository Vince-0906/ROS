---
tags:
  - ROS2
---
# 通信方式
## Topic
基于发布-订阅
类似于发blog的writer和reader
> [!note]
> 发布者 订阅者 话题名称 话题类型

## Service
客户端发送请求，服务端处理并返回
类似于Q&A
## Parameter
参数设置和读取
查看/更改当前的status等
## Action
实时控制
服务端可以反馈请求吗，客户端可以取消请求

# 应用框架
## Gazebo
仿真工具，模拟机器人的行为和环境
## Navigation 2
移动机器人提供导航功能
## Moveit 2
机械臂运动规划

可以替代具体的ROS版本
```bash
$ROS_DISTRO
```

---

📑 [返回笔记索引](../README.md#笔记索引)
