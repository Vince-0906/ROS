import launch
import launch_ros


def generate_launch_description():
    # 1.声明一个launch的参数
    action_declare_arg_background_g = launch.actions.DeclareLaunchArgument('launch_arg_bg', default_value="150")
    action_declare_max_speed = launch.actions.DeclareLaunchArgument('launch_arg_ms',default_value="2.0")

    # 2.把参数的值传递给节点
    """产生一个launch描述符,用于启动demo_cpp_service节点。"""

    action_node_turtlesim_node = launch_ros.actions.Node(
            package='turtlesim',  # 包名
            executable='turtlesim_node',  # 可执行文件名
            parameters=[{'background_g': launch.substitutions.LaunchConfiguration('launch_arg_bg',default="150")}],  # 参数
            # name='patrol_server',  # 节点名
            output='screen'  # 输出到屏幕
        )
    action_node_patrol_client = launch_ros.actions.Node(
            package='demo_cpp_service',  # 包名
            executable='patrol_client',  # 可执行文件名
            # name='patrol_server',  # 节点名
            output='log'  # 输出到屏幕
        )
    action_node_turtle_control = launch_ros.actions.Node(
            package='demo_cpp_service',  # 包名
            executable='turtle_control',  # 可执行文件名
            parameters=[{'max_speed': launch.substitutions.LaunchConfiguration('launch_arg_ms',default="2.0")}],  # 参数
            # name='patrol_server',  # 节点名
            output='both'  # 输出到屏幕
        )
    return launch.LaunchDescription([
        action_declare_arg_background_g,
        action_declare_max_speed,
        action_node_turtlesim_node,
        action_node_patrol_client,
        action_node_turtle_control,

     # actions动作
    ])