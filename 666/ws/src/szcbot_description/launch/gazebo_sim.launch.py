import launch
import launch_ros
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # 获取功能包share路径
    urdf_package_path = get_package_share_directory('szcbot_description')
    default_xacro_path = os.path.join(urdf_package_path, 'urdf', 'szcbot/szcbot.urdf.xacro')
    # default_rviz_config_path = os.path.join(urdf_package_path, 'config', 'display_robot_model.rviz')
    default_gazebo_world_path = os.path.join(urdf_package_path, 'world', 'room.sdf')
    # 声明一个xacro目录参数，方便修改
    action_declare_arg_model_path = launch.actions.DeclareLaunchArgument(
        name='model',
        default_value= str(default_xacro_path),
        description='加载模型的xacro文件路径'
    )

    # 通过文件路径获取内容，并转换为参数值对象，以供传入robot_state_publisher

    command_result = launch.substitutions.Command(['xacro ', launch.substitutions.LaunchConfiguration('model')])
    robot_description_value = launch_ros.parameter_descriptions.ParameterValue(command_result, value_type=str)

    action_robot_state_publisher = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description_value}]
    )

    action_launch_gazebo = launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch','gz_sim.launch.py')
        ),
        launch_arguments=[('gz_args', default_gazebo_world_path),('verbose', 'true')],  # 传入gazebo世界文件路径参数
    )

    action_create = launch_ros.actions.Node(
        package='ros_gz_sim',
        executable='create',
        arguments=["-topic", "/robot_description", "-name", "szcbot",
                "-x", "0.0",
                "-y", "0.0",
                "-z", "0.0",
                '-world', 'room'],
        output="screen",
        parameters=[{'use_sim_time': True}]
)


    return launch.LaunchDescription([
        action_declare_arg_model_path,
        action_robot_state_publisher,
        action_launch_gazebo,
        action_create
    ])
