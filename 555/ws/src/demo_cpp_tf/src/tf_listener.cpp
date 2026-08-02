#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/transform_stamped.hpp> //提供geometry_msgs消息接口
#include <tf2/LinearMath/Quaternion.h> //提供tf2类
#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp> //提供tf2和geometry_msgs之间的转换接口
#include <tf2_ros/transform_listener.h> //变换监听器接口
#include <chrono> //提供时间接口'
#include <tf2_ros/buffer.h> //提供tf2缓冲区接口
#include <tf2/utils.h> //四元数和欧拉角转换接口


using namespace std::chrono_literals; //使用命名空间，方便使用时间单位

class TFListener : public rclcpp::Node
{
    private:
    std::shared_ptr<tf2_ros::TransformListener> listener_; //变换监听器对象
    rclcpp::TimerBase::SharedPtr timer_; //定时器对象
    std::shared_ptr<tf2_ros::Buffer> buffer_; //tf2缓冲区对象

    public:
    TFListener():Node("tf_listener")
    {
        this->buffer_ = std::make_shared<tf2_ros::Buffer>(this->get_clock());
        this->listener_ = std::make_shared<tf2_ros::TransformListener>(*buffer_, this); //创建变换监听器对象
        timer_ = this->create_wall_timer(1s, std::bind(&TFListener::getTransform, this)); //创建定时器对象，每隔1s调用一次getTransform函数
    };

    void getTransform()
    {
        // 到buffer_查询坐标关系
        try
        {
            //查询坐标关系
            const auto transform = buffer_->lookupTransform("base_link", "target_point", this->get_clock()->now(), rclcpp::Duration::from_seconds(1.0));
            // 获取查询结果
            auto translation = transform.transform.translation;
            auto rotation = transform.transform.rotation;
            double y, p, r;
            tf2::getEulerYPR(rotation, y, p, r); //将四元数转换为欧拉角
            RCLCPP_INFO(get_logger(), "坐标关系: 平移量: x: %f, y: %f, z: %f", translation.x, translation.y, translation.z);
            RCLCPP_INFO(get_logger(), "旋转角度: yaw: %f, pitch: %f, roll: %f", y, p, r);
        }
        catch(const std::exception& e)
        {
            RCLCPP_WARN(get_logger(), "不能获取坐标关系: %s", e.what());
        }
    }
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv); //初始化ROS2客户端库
    auto node = std::make_shared<TFListener>();
    rclcpp::spin(node); //循环等待回调函数执行
    rclcpp::shutdown(); //关闭ROS2客户端库
    return 0;
}