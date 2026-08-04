import launch
import launch_ros
import os
from ament_index_python.packages import get_package_share_directory
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ros_gz_bridge.actions import RosGzBridge
from launch.actions import ExecuteProcess

def generate_launch_description():
    # 获取功能包share路径
    urdf_package_path = get_package_share_directory('szcbot_description')
    default_xacro_path = os.path.join(urdf_package_path, 'urdf', 'szcbot/szcbot.urdf.xacro')
    default_gazebo_world_path = os.path.join(urdf_package_path, 'world', 'complex_rooms.sdf')
    default_bridge_yaml_path = os.path.join(urdf_package_path, 'config', 'bridge.yaml')

    # 声明一个xacro目录参数，方便修改
    action_declare_arg_model_path = DeclareLaunchArgument(
        name='model',
        default_value=str(default_xacro_path),
        description='加载模型的xacro文件路径'
    )
    

    # 通过文件路径获取内容，并转换为参数值对象，以供传入robot_state_publisher
    command_result = launch.substitutions.Command(['xacro ', LaunchConfiguration('model')])
    robot_description_value = launch_ros.parameter_descriptions.ParameterValue(command_result, value_type=str)

    action_robot_state_publisher = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description_value}]
    )

    action_launch_gazebo = launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource(
            [get_package_share_directory('ros_gz_sim'), '/launch', '/gz_sim.launch.py']
        ),
        launch_arguments={'gz_args': f'-r {default_gazebo_world_path}'}.items()
    )

    action_create = launch_ros.actions.Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', '/robot_description', '-name', 'szcbot',
                   '-x', '0.0',
                   '-y', '0.0',
                   '-z', '0.01',
                    "-R", "0.0",    # roll
                    "-P", "0.0",    # pitch
                    "-Y", "3.14",    # yaw
                   '-world', 'complex_rooms'],
        output='screen',
        parameters=[{'use_sim_time': True}]
    )

    # 桥接配置参数声明
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

    # 使用 RosGzBridge action 来桥接话题
    bridge = RosGzBridge(
        bridge_name=LaunchConfiguration('bridge_name'),
        config_file=LaunchConfiguration('config_file')
    )

    # 静态坐标变换：将 Gazebo 的 frame_id 映射到 laser_link
    action_static_tf_lidar = launch_ros.actions.Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='lidar_frame_publisher',
        arguments=['0', '0', '0', '0', '0', '0', 'laser_link', 'szcbot/base_footprint/gpu_lidar']
    )
    # 静态坐标变换：将 Gazebo 的 frame_id 映射到 imu_link
    action_static_tf_imu = launch_ros.actions.Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='imu_frame_publisher',
        arguments=['0', '0', '0', '0', '0', '0', 'imu_link', 'szcbot/base_footprint/imu_sensor']
    )
    # 静态坐标变换：将 Gazebo 的 frame_id 映射到 camera_link
    action_static_tf_camera = launch_ros.actions.Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='camera_frame_publisher',
        arguments=['0', '0', '0', '0', '0', '0', 'camera_link', 'szcbot/base_footprint/camera']
    )
    # 静态坐标变换：将 Gazebo 的 frame_id 映射到 camera_link
    action_static_tf_depth_camera = launch_ros.actions.Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='depth_camera_frame_publisher',
        arguments=['0', '0', '0', '0', '0', '0', 'camera_link', 'szcbot/base_footprint/depth_camera']
    )

    action_load_joint_state_controller = launch.actions.ExecuteProcess(
        cmd='ros2 control load_controller szcbot_joint_state_broadcaster --set-state active'.split(' '),
        output='screen'
    )

    return launch.LaunchDescription([
        action_declare_arg_model_path,
        bridge_name_arg,
        config_file_arg,
        action_robot_state_publisher,
        action_launch_gazebo,
        action_create,
        bridge,
        action_static_tf_lidar,
        action_static_tf_imu,
        action_static_tf_camera,
        action_static_tf_depth_camera,
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=action_create,
                on_exit=[action_load_joint_state_controller],
            )
        )
    ])

