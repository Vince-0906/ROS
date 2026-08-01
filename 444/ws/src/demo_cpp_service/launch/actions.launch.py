import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    action_declare_start_rqt = launch.actions.DeclareLaunchArgument('start_rqt', default_value="False")

    start_rqt = launch.substitutions.LaunchConfiguration('start_rqt',default="False")

    # 动作1.包含并启动其他launch文件
    multisim_launch_file_path = [get_package_share_directory('turtlesim'),'/launch/','multisim.launch.py']
    action_include_launch = launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource(
            multisim_launch_file_path
        )
    )

    # 动作2.打印数据
    action_log_info = launch.actions.LogInfo(msg=str(multisim_launch_file_path))

    # 动作3.执行进程,其实就算执行一个命令行，例如：ros2 topic list

    action_topic_list = launch.actions.ExecuteProcess(
        condition=launch.conditions.IfCondition(start_rqt),
        # if start_rqt;
        # run:rqt
        cmd=['rqt']
    )
    # 动作4.组织动作成组，把多个动作放到一个组里，组里的动作可以并行执行，也可以顺序执行
    action_group = launch.actions.GroupAction([
        # 动作5.定时器
        launch.actions.TimerAction(period=2.0,actions=[action_include_launch]),
        launch.actions.TimerAction(period=5.0,actions=[action_topic_list])
    ])

    return launch.LaunchDescription([
        action_log_info,
        action_declare_start_rqt,
        action_group
     # actions动作
    ])