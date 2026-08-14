#include <Arduino.h>
#include <Esp32McpwmMotor.h>
#include <Esp32PcntEncoder.h>
#include <PidController.h>
#include <Kinematics.h>
// 引入microros和wifi相关库
#include <WiFi.h>
#include <micro_ros_platformio.h>
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <geometry_msgs/msg/twist.h> //消息接口


// 创建电机、编码器、PID控制器和运动学对象
rcl_allocator_t allocator; // 动态内存分配器，用于在运行时分配和释放内存
rclc_support_t support; // 用于存储时钟，内存分配器和上下文
rclc_executor_t executor; // 用于管理和调度ROS2节点的执行器
rcl_node_t node; // ROS2节点对象，用于与ROS2系统进行通信

rcl_subscription_t sub_cmd_vel; // 创建一个订阅者对象，用于接收ROS2消息
geometry_msgs__msg__Twist msg_cmd_vel; // 创建一个Twist消息对象，用于存储接收到的速度命令

Esp32McpwmMotor motor; // 创建一个名为motor的对象，用于控制电机
Esp32PcntEncoder encoders[2]; // 创建一个数组用于存储两个编码器
PidController pid_controller[2]; // 创建一个数组用于存储两个PID控制器
Kinematics kinematics; // 创建一个名为kinematics的对象，用于运动学计算

float target_linear_speed = 50.0; // 目标线速度，单位为mm/s
float target_angular_speed = 0.1; // 目标角速度，单位为弧度每秒
float out_left_speed = 0.0; // 左轮输出速度，单位为mm/s
float out_right_speed = 0.0; // 右轮输出速度，单位为mm/s

void twist_callback(const void * msg_in) // 回调函数，用于处理接收到的Twist消息
{
    // 1.将接收到的消息转换为Twist类型
    const geometry_msgs__msg__Twist * msg = (const geometry_msgs__msg__Twist *)msg_in;
    // 2.获取线速度和角速度
    target_linear_speed = msg->linear.x *1000; // 获取线速度
    target_angular_speed = msg->angular.z; // 获取角速度
    // 3.运动学逆解
    kinematics.kinematics_inverse(target_linear_speed, target_angular_speed, &out_left_speed, &out_right_speed); // 计算两轮目标速度
    Serial.printf("目标线速度=%f,目标角速度=%f,左轮目标速度=%f,右轮目标速度=%f\n", target_linear_speed, target_angular_speed, out_left_speed, out_right_speed); 
    pid_controller[0].update_target(out_left_speed); // 设置电机0的目标速度为左轮目标速度
    pid_controller[1].update_target(out_right_speed); // 设置电机1的目标速度为右轮目标速度
    

}

// 创建任务运行microros 相当于线程
void micro_ros_task(void *arg)
{
    // 1.设置传输协议并延迟一段时间等待设置完成
    IPAddress agent_ip; 
    agent_ip.fromString("192.168.31.93"); // 设置ROS2代理的IP地址
    set_microros_wifi_transports("SZC", "SZC030906", agent_ip, 8888); // 设置WiFi传输协议，指定设备名称、代理IP和端口号
    delay(2000); // 延迟1秒等待设置完成
    // 2.初始化内存分配器
    allocator = rcl_get_default_allocator(); // 获取默认的内存分配器
    // 3.初始化支持结构体
    rclc_support_init(&support, 0, NULL, &allocator); // 初始化支持结构体，传入参数为命令行参数和内存分配器
    // 4.初始化节点
    rclc_node_init_default(&node, "szcbot_motion_control", "", &support);
    // 5.初始化执行器
    unsigned int num_handles = 1; // 设置执行器的句柄数量为1
    rclc_executor_init(&executor, &support.context, num_handles, &allocator);
    // 6.初始化订阅者并添加到执行器
    rclc_subscription_init_default(
        &sub_cmd_vel, // 订阅者对象
        &node, // 节点对象
        ROSIDL_GET_MSG_TYPE_SUPPORT(geometry_msgs, msg, Twist), // 消息类型支持
        "cmd_vel"); // 订阅的主题名称
    rclc_executor_add_subscription(
        &executor, // 执行器对象
        &sub_cmd_vel, // 订阅者对象
        &msg_cmd_vel, // 消息对象
        &twist_callback, // 回调函数
        ON_NEW_DATA); // 触发条件为接收到新数据
    // 循环执行器
    rclc_executor_spin(&executor); // 启动执行器，开始处理ROS2消息和事件
}


void setup()
{
    Serial.begin(115200); // 初始化串口通信，波特率为115200
    // 初始化电机和编码器
    encoders[0].init(0, 32, 33); // 初始化第一个编码器，使用GPIO 32和33连接
    encoders[1].init(1, 26, 25); // 初始化第二个编码器，使用GPIO 26和25连接
    motor.attachMotor(0, 22, 23); // 将电机0连接到引脚22和引脚23
    motor.attachMotor(1, 12, 13); // 将电机1连接到引脚12和引脚13

    // 设置PID参数
    pid_controller[0].update_pid(0.625, 0.125, 0.01); // 设置电机0的PID参数
    pid_controller[1].update_pid(0.625, 0.125, 0.01); // 设置电机1的PID参数
    pid_controller[0].out_limit(-100, 100); // 设置电机0的输出上下限
    pid_controller[1].out_limit(-100, 100); // 设置电机1的输出上下限
    pid_controller[0].update_target(100); // 设置电机0的目标速度为100
    pid_controller[1].update_target(100); // 设置电机1的目标速度为100

    // 初始化运动学参数
    kinematics.set_wheel_distance(175); // 设置两轮之间的距离mm
    kinematics.set_motor_param(0, 0.10345); // 设置电机0的每个脉冲对应的距离mm
    kinematics.set_motor_param(1, 0.10345); // 设置电机1的每个脉冲对应的距离mm


    // 创建microros任务
    xTaskCreate(micro_ros_task, "micro_ros_task", 10240, NULL, 1, NULL);
}

void loop()
{
    delay(10); // 等待10毫秒
    // 打印速度
    kinematics.update_motor_speed(millis(), encoders[0].getTicks(), encoders[1].getTicks()); // 更新电机速度和编码器计数值
    // // 使用PID控制器获取输出值
    motor.updateMotorSpeed(0, pid_controller[0].update(kinematics.get_motor_speed(0)));
    motor.updateMotorSpeed(1, pid_controller[1].update(kinematics.get_motor_speed(1)));
    // Serial.printf("x,y,yaw=%f,%f,%f\n", kinematics.get_odom().x, kinematics.get_odom().y, kinematics.get_odom().angle);
    // Serial.printf("电机1=%f,电机2=%f\n", current_speed[0], current_speed[1]);


    // 读取并打印两个编码器的计数器数值
    // Serial.printf("tick1=%d,tick2=%d\n", encoders[0].getTicks(), encoders[1].getTicks());
    // motor.updateMotorSpeed(0, -70); // 设置电机0的速度为负70
    // motor.updateMotorSpeed(1, 70); // 设置电机1的速度为正70
    // delay(2000); // 延迟两秒

    // motor.updateMotorSpeed(0, 70); // 设置电机0的速度为正70
    // motor.updateMotorSpeed(1, -70); // 设置电机1的速度为负70
    // delay(2000); // 延迟两秒
}