# ROS 2 Gazebo 版本迁移指南

## Humble (旧版) vs Jazzy (新版) 差异总结

---

## 一、核心差异

### 1. Gazebo 版本
- **旧版 (Humble)**: Gazebo Classic (Gazebo 11)
- **新版 (Jazzy)**: Gazebo Sim (Gazebo Harmonic/Ionic，基于 Ignition)

### 2. 通信架构
- **旧版**: 插件直接发布 ROS 2 话题，无需桥接
- **新版**: 插件发布 Gazebo Transport 话题，**必须通过 `ros_gz_bridge` 桥接到 ROS 2**

这是最关键的区别！新版 Gazebo 使用独立的 Gazebo Transport 通信协议，与 ROS 2 完全隔离，需要显式配置桥接。

---

## 二、插件配置差异

### 1. 差速驱动插件

#### 旧版 (Gazebo Classic)
```xml
<plugin name="differential_drive_controller" filename="libgazebo_ros_diff_drive.so">
    <left_joint>left_wheel_joint</left_joint>
    <right_joint>right_wheel_joint</right_joint>
    <wheel_separation>0.2</wheel_separation>
    <wheel_diameter>0.065</wheel_diameter>
    
    <!-- 直接发布到 ROS 2 话题 -->
    <command_topic>/cmd_vel</command_topic>
    <odometry_topic>/odom</odometry_topic>
    
    <!-- 支持速度和加速度限制 -->
    <max_wheel_torque>20</max_wheel_torque>
    <max_wheel_acceleration>1.0</max_wheel_acceleration>
    
    <!-- 发布配置 -->
    <publish_odom>true</publish_odom>
    <publish_odom_tf>true</publish_odom_tf>
    <publish_wheel_tf>false</publish_wheel_tf>
    <odometry_frame>odom</odometry_frame>
    <robot_base_frame>base_footprint</robot_base_frame>
</plugin>
```

#### 新版 (Gazebo Sim)
```xml
<plugin name='gz::sim::systems::DiffDrive' filename='gz-sim-diff-drive-system'>
    <left_joint>left_wheel_joint</left_joint>
    <right_joint>right_wheel_joint</right_joint>
    <wheel_separation>0.2</wheel_separation>
    <wheel_radius>0.0325</wheel_radius>  <!-- 注意：是半径，不是直径！ -->
    
    <!-- 坐标系配置 -->
    <frame_id>odom</frame_id>
    <child_frame_id>base_footprint</child_frame_id>
</plugin>
```

**关键变化**：

| 项目 | 旧版 | 新版 |
|------|------|------|
| 文件名 | `libgazebo_ros_diff_drive.so` | `gz-sim-diff-drive-system` |
| 命名空间 | 无 | `gz::sim::systems::` |
| 轮子参数 | `wheel_diameter` (直径) | `wheel_radius` (半径，数值除以2) |
| 话题配置 | 直接 ROS 2 话题名 | Gazebo Transport 话题 (需要桥接) |
| 速度限制 | 支持 `max_wheel_torque` 等 | ❌ 不支持 |
| TF 发布控制 | `publish_odom_tf` | ❌ 不支持显式配置 |

**⚠️ 重要提示**：
- 新版中如果不配置 `<topic>` 标签，默认话题是 `/model/<model_name>/cmd_vel`
- 如果配置了 `<topic>/cmd_vel</topic>`，则监听 `/cmd_vel`（但这是 Gazebo 话题，仍需桥接）

---

### 2. 关节状态发布插件

#### 旧版 (Gazebo Classic)
```xml
<plugin name="joint_state_publisher" filename="libgazebo_ros_joint_state_publisher.so">
    <update_rate>50</update_rate>
    <joint_name>left_wheel_joint</joint_name>
    <joint_name>right_wheel_joint</joint_name>
    <!-- 直接发布到 ROS 2 的 /joint_states 话题 -->
</plugin>
```

#### 新版 (Gazebo Sim)
```xml
<plugin name='gz::sim::systems::JointStatePublisher' filename='gz-sim-joint-state-publisher-system'>
    <joint_name>left_wheel_joint</joint_name>
    <joint_name>right_wheel_joint</joint_name>
    <!-- 发布到 Gazebo Transport，需要桥接到 ROS 2 -->
</plugin>
```

**关键变化**：
- 新版不直接发布到 ROS 2，发布到 Gazebo Transport
- 默认话题路径：`/world/<world_name>/model/<model_name>/joint_state`
- **必须在 bridge.yaml 中配置桥接**

---

## 三、话题桥接配置（新版特有）

### 为什么需要桥接？

新版 Gazebo 与 ROS 2 完全隔离：
- Gazebo 插件 → Gazebo Transport 话题
- ROS 2 节点 → ROS 2 话题
- 需要 `ros_gz_bridge` 在两者之间转换消息

### 桥接配置文件 `config/bridge.yaml`

```yaml
# ROS 2 与 Gazebo 之间的话题桥接配置

# 时钟同步：从 Gazebo 到 ROS 2
- ros_topic_name: "clock"
  gz_topic_name: "/clock"
  ros_type_name: "rosgraph_msgs/msg/Clock"
  gz_type_name: "gz.msgs.Clock"
  direction: "GZ_TO_ROS"

# 速度控制：从 ROS 2 到 Gazebo (双向)
- gz_topic_name: "/cmd_vel"
  ros_type_name: "geometry_msgs/msg/Twist"
  gz_type_name: "gz.msgs.Twist"
  # 不指定 direction 表示双向

# 里程计：从 Gazebo 到 ROS 2
- ros_topic_name: "odometry"
  gz_topic_name: "/odometry"
  ros_type_name: "nav_msgs/msg/Odometry"
  gz_type_name: "gz.msgs.Odometry"
  direction: "GZ_TO_ROS"

# 关节状态：从 Gazebo 到 ROS 2
- ros_topic_name: "joint_states"
  gz_topic_name: "/world/room/model/szcbot/joint_state"
  ros_type_name: "sensor_msgs/msg/JointState"
  gz_type_name: "gz.msgs.Model"
  direction: "GZ_TO_ROS"

# TF 变换：从 Gazebo 到 ROS 2
- ros_topic_name: "tf"
  gz_topic_name: "/tf"
  ros_type_name: "tf2_msgs/msg/TFMessage"
  gz_type_name: "gz.msgs.Pose_V"
  direction: "GZ_TO_ROS"
```

**配置说明**：
- `ros_topic_name`: ROS 2 话题名（相对路径，会加上节点命名空间）
- `gz_topic_name`: Gazebo Transport 话题名（绝对路径）
- `direction`: 
  - `GZ_TO_ROS` - 仅 Gazebo → ROS 2
  - `ROS_TO_GZ` - 仅 ROS 2 → Gazebo
  - 不指定 - 双向桥接

---

## 四、Launch 文件差异

### 旧版 (Gazebo Classic)
```python
from launch import LaunchDescription
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([
        # 直接启动 Gazebo Classic
        ExecuteProcess(
            cmd=['gazebo', '--verbose', world_path],
            output='screen'
        ),
        # 无需桥接节点
    ])
```

### 新版 (Gazebo Sim)
```python
import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from ros_gz_bridge.actions import RosGzBridge

def generate_launch_description():
    # 获取配置文件路径
    urdf_package_path = get_package_share_directory('szcbot_description')
    default_gazebo_world_path = os.path.join(urdf_package_path, 'world', 'room.sdf')
    default_bridge_yaml_path = os.path.join(urdf_package_path, 'config', 'bridge.yaml')
    
    # 启动 Gazebo Sim
    action_launch_gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            get_package_share_directory('ros_gz_sim'), 
            '/launch/gz_sim.launch.py'
        ]),
        launch_arguments={'gz_args': f'-r {default_gazebo_world_path}'}.items()
    )
    
    # 桥接配置参数
    bridge_name_arg = DeclareLaunchArgument(
        'bridge_name',
        default_value='szcbot_bridge',
        description='Name of ros_gz_bridge node'
    )
    
    config_file_arg = DeclareLaunchArgument(
        'config_file',
        default_value=default_bridge_yaml_path,
        description='YAML config file'
    )
    
    # ⚠️ 必须添加桥接节点
    bridge = RosGzBridge(
        bridge_name=LaunchConfiguration('bridge_name'),
        config_file=LaunchConfiguration('config_file')
    )
    
    return LaunchDescription([
        bridge_name_arg,
        config_file_arg,
        action_launch_gazebo,
        bridge  # 桥接节点
    ])
```

**关键差异**：
1. 导入 `ros_gz_bridge.actions.RosGzBridge`
2. 创建 `bridge.yaml` 配置文件
3. 添加 `RosGzBridge` action 到 LaunchDescription
4. 使用 `gz_sim.launch.py` 而不是直接调用 `gazebo` 命令

---

## 五、迁移步骤清单

### ✅ 步骤 1：更新插件配置

**文件位置**: `urdf/*/plugins/*.xacro`

- [ ] 修改插件文件名：`libgazebo_ros_*.so` → `gz-sim-*-system`
- [ ] 添加命名空间：`gz::sim::systems::`
- [ ] 调整参数名：`wheel_diameter` → `wheel_radius`（数值除以2）
- [ ] 移除不支持的参数：
  - `max_wheel_torque`
  - `max_wheel_acceleration`
  - `publish_odom_tf`
  - `publish_wheel_tf`
  - `update_rate`

### ✅ 步骤 2：创建桥接配置

**新建文件**: `config/bridge.yaml`

- [ ] 创建 YAML 配置文件
- [ ] 配置必需话题：
  - `/clock` - 时钟同步
  - `/cmd_vel` - 速度控制
  - `/odom` 或 `/odometry` - 里程计
  - `/joint_states` - 关节状态
  - `/tf` - 坐标变换
- [ ] 确认 Gazebo 侧实际话题名（使用 `gz topic -l` 查看）

### ✅ 步骤 3：更新 Launch 文件

**文件位置**: `launch/*.launch.py`

- [ ] 导入 `ros_gz_bridge.actions.RosGzBridge`
- [ ] 添加桥接配置参数声明
- [ ] 创建 `RosGzBridge` action
- [ ] 将桥接节点添加到 LaunchDescription

### ✅ 步骤 4：验证话题连通性

```bash
# 1. 检查 ROS 2 话题
ros2 topic list

# 2. 检查 Gazebo 话题
gz topic -l

# 3. 测试速度控制
ros2 run teleop_twist_keyboard teleop_twist_keyboard

# 4. 检查里程计
ros2 topic echo /odom

# 5. 检查关节状态
ros2 topic echo /joint_states

# 6. 在 RViz2 中验证 TF 树
rviz2
```

---

## 六、常见问题排查

### 问题 1：机器人无法移动

**可能原因**：
1. `/cmd_vel` 话题没有正确桥接
2. 插件中配置的话题名与 bridge.yaml 不匹配

**排查步骤**：
```bash
# 检查 ROS 2 话题
ros2 topic list | grep cmd_vel
ros2 topic echo /cmd_vel

# 检查 Gazebo 话题
gz topic -l | grep cmd_vel
gz topic -e -t /cmd_vel  # 或 /model/szcbot/cmd_vel
```

**解决方案**：
- 确保插件中的 `<topic>` 标签与 bridge.yaml 中的 `gz_topic_name` 一致
- 或者移除插件中的 `<topic>` 标签，使用默认话题 `/model/<model_name>/cmd_vel`

### 问题 2：RViz2 中轮子没有 Transform

**可能原因**：
1. `/joint_states` 话题没有数据
2. `JointStatePublisher` 插件未正确加载
3. bridge.yaml 中的 `gz_topic_name` 路径错误

**排查步骤**：
```bash
# 检查 ROS 2 joint_states
ros2 topic hz /joint_states
ros2 topic echo /joint_states

# 检查 Gazebo 关节话题
gz topic -l | grep joint

# 查看可能的话题名：
# - /world/<world_name>/model/<model_name>/joint_state
# - /world/<world_name>/model/<model_name>/joint_states
```

**解决方案**：
- 根据 `gz topic -l` 的实际输出修改 bridge.yaml 中的 `gz_topic_name`
- 确保 `JointStatePublisher` 插件在 URDF 中正确配置

### 问题 3：[Err] Failed to load system plugin

**错误示例**：
```
[Err] [SystemLoader.cc:92] Failed to load system plugin 
[libgazebo_ros_diff_drive.so] : Could not find shared library.
```

**原因**：使用了旧版插件名称

**解决方案**：
- 将 `filename="libgazebo_ros_diff_drive.so"` 改为 `filename="gz-sim-diff-drive-system"`
- 添加命名空间：`name="gz::sim::systems::DiffDrive"`

### 问题 4：话题名不匹配

**症状**：
- 插件配置了 `<topic>/cmd_vel</topic>`
- bridge.yaml 配置了 `gz_topic_name: "/model/szcbot/cmd_vel"`
- 两者无法通信

**原因**：插件中配置的话题名会覆盖默认行为

**解决方案（两种）**：

**方案 A**：移除插件中的话题配置（推荐）
```xml
<plugin name='gz::sim::systems::DiffDrive' filename='gz-sim-diff-drive-system'>
    <!-- 移除这些行，使用默认话题 -->
    <!-- <topic>/cmd_vel</topic> -->
    <!-- <odom_topic>/odometry</odom_topic> -->
</plugin>
```
```yaml
# bridge.yaml 使用默认话题
- gz_topic_name: "/model/szcbot/cmd_vel"
```

**方案 B**：保持插件配置，修改 bridge.yaml
```xml
<plugin name='gz::sim::systems::DiffDrive' filename='gz-sim-diff-drive-system'>
    <topic>/cmd_vel</topic>
    <odom_topic>/odometry</odom_topic>
</plugin>
```
```yaml
# bridge.yaml 匹配插件配置
- gz_topic_name: "/cmd_vel"
- gz_topic_name: "/odometry"
```

---

## 七、参考资源

### 官方文档
- [Gazebo Sim 插件文档](https://gazebosim.org/api/sim/8/namespacegz_1_1sim_1_1systems.html)
- [ros_gz_bridge 文档](https://github.com/gazebosim/ros_gz/tree/ros2/ros_gz_bridge)
- [ROS 2 Jazzy 发行说明](https://docs.ros.org/en/jazzy/Releases/Release-Jazzy-Jalisco.html)

### 常用命令

```bash
# 查看 Gazebo 话题列表
gz topic -l

# 监听 Gazebo 话题
gz topic -e -t /cmd_vel

# 查看 Gazebo 话题详情
gz topic -i -t /cmd_vel

# 查看 ROS 2 话题
ros2 topic list
ros2 topic info /cmd_vel
ros2 topic echo /cmd_vel

# 查看 TF 树
ros2 run tf2_tools view_frames
```

---

## 八、总结

### 核心要点

1. **新版 Gazebo 与 ROS 2 完全隔离**，必须通过桥接通信
2. **所有插件都需要更新**文件名和命名空间
3. **必须创建 bridge.yaml** 并配置所有需要的话题
4. **话题名称要匹配**：插件配置 ↔ bridge.yaml ↔ ROS 2 节点
5. **使用 `gz topic -l` 确认**实际的 Gazebo 话题名称

### 迁移优势

虽然迁移需要额外配置，但新版 Gazebo 提供：
- 更好的性能和稳定性
- 更现代的架构设计
- 更丰富的传感器支持
- 更好的分布式仿真能力
- 与 ROS 2 的清晰隔离（便于独立开发和测试）

---
**适用版本**: ROS 2 Humble → Jazzy, Gazebo Classic → Gazebo Sim
