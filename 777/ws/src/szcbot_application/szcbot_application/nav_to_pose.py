from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator
import rclpy


def main():
    rclpy.init()
    nav = BasicNavigator()
    nav.waitUntilNav2Active() # 等待导航系统激活
    goal_pose = PoseStamped()
    goal_pose.header.frame_id = "map"
    goal_pose.header.stamp = nav.get_clock().now().to_msg()
    goal_pose.pose.position.x = 2.0
    goal_pose.pose.position.y = 1.0
    goal_pose.pose.orientation.w = 1.0
    nav.goToPose(goal_pose)
    while not nav.isTaskComplete():
        feedback = nav.getFeedback()
        nav.get_logger().info(f"剩余距离: {feedback.distance_remaining:.2f} 米，剩余时间: {feedback.estimated_time_remaining.sec} 秒")
        # nav.cancelTask()  # 取消任务
    result = nav.getResult()
    nav.get_logger().info(f'导航结果：{result}')

    # rclpy.spin(nav)
    # rclpy.shutdown()
