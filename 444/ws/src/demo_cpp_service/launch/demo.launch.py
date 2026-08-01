import launch
import launch_ros


def generate_launch_description():
    """产生一个launch描述符,用于启动demo_cpp_service节点。"""

    action_node_turtlesim_node = launch_ros.actions.Node(
            package='turtlesim',  # 包名
            executable='turtlesim_node',  # 可执行文件名
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
            # name='patrol_server',  # 节点名
            output='both'  # 输出到屏幕
        )
    return launch.LaunchDescription([
        action_node_turtlesim_node,
        action_node_patrol_client,
        action_node_turtle_control,

     # actions动作
    ])