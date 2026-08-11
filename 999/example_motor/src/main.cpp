#include <Arduino.h>
#include <Esp32McpwmMotor.h>
#include <Esp32PcntEncoder.h>
#include <PidController.h>
#include <Kinematics.h>

Esp32McpwmMotor motor; // 创建一个名为motor的对象，用于控制电机
Esp32PcntEncoder encoders[2]; // 创建一个数组用于存储两个编码器
PidController pid_controller[2]; // 创建一个数组用于存储两个PID控制器
Kinematics kinematics; // 创建一个名为kinematics的对象，用于运动学计算

float target_linear_speed = 50.0; // 目标线速度，单位为mm/s
float target_angular_speed = 0.1; // 目标角速度，单位为弧度每秒
float out_left_speed = 0.0; // 左轮输出速度，单位为mm/s
float out_right_speed = 0.0; // 右轮输出速度，单位为mm/s

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
    // 测试运动学正逆解
    kinematics.kinematics_inverse(target_linear_speed, target_angular_speed, &out_left_speed, &out_right_speed); // 计算两轮目标速度
    Serial.printf("目标线速度=%f,目标角速度=%f,左轮目标速度=%f,右轮目标速度=%f\n", target_linear_speed, target_angular_speed, out_left_speed, out_right_speed); 
    pid_controller[0].update_target(out_left_speed); // 设置电机0的目标速度为左轮目标速度
    pid_controller[1].update_target(out_right_speed); // 设置电机1的目标速度为右轮目标速度
}

void loop()
{
    delay(10); // 等待10毫秒
    // 打印速度
    kinematics.update_motor_speed(millis(), encoders[0].getTicks(), encoders[1].getTicks()); // 更新电机速度和编码器计数值
    // // 使用PID控制器获取输出值
    motor.updateMotorSpeed(0, pid_controller[0].update(kinematics.get_motor_speed(0)));
    motor.updateMotorSpeed(1, pid_controller[1].update(kinematics.get_motor_speed(1)));
    Serial.printf("x,y,yaw=%f,%f,%f\n", kinematics.get_odom().x, kinematics.get_odom().y, kinematics.get_odom().angle);
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