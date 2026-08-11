#ifndef __KINEMATICS_H__
#define __KINEMATICS_H__

#include <Arduino.h>

typedef struct
{
    float per_pulse_distance; // 每个脉冲对应的距离
    int16_t motor_speed; // 电机转速mm/s
    int64_t last_encoder_ticks; // 上一次编码器计数值

}motor_param_t;
typedef struct
{
    float x; // 线速度mm/s
    float y; // 角速度rad/s
    float angle; // 角度rad
    float linear_speed; // 线速度mm/s
    float angular_speed; // 角速度rad/s
}odom_t;
/**
 *  1.运动学正逆解类(两个轮子实时速度->当前实时角速度和线速度/当前目标角速度和线速度->两个轮子目标转速)
 *  
 */
class Kinematics
{
    public:
        Kinematics() = default;
        ~Kinematics() = default;
        odom_t& get_odom();
        void update_odom(uint16_t dt);
        void TransAngleInPI(float angle,float &out_angle);


        // 设置两轮之间的距离，单位为米
        void set_wheel_distance(float distance);
        
        // 设置电机参数
        void set_motor_param(uint8_t id,float per_pulse_distance);
        // 运动学正解，将两个轮子的实时速度转换为当前实时角速度和线速度
        void kinematics_forward(float left_speed,float right_speed,float *out_linear_speed,float *out_angular_speed);
        // 运动学逆解，将当前目标角速度和线速度转换为两个轮子目标转速
        void kinematics_inverse(float linear_speed,float angular_speed,float *out_left_speed,float *out_right_speed);
        // 更新电机速度和编码器计数值
        void update_motor_speed(uint64_t current_time,int32_t left_tick,int32_t right_tick);
        // 获取电机速度，返回速度
        int16_t get_motor_speed(uint8_t id);
    private:
    motor_param_t motor_param[2]; // 电机参数数组，存储两个电机的参数
    uint64_t last_update_time = 0; // 上一次更新速度的时间
    float wheel_distance= 0; // 两轮之间的距离，单位为米
    odom_t odom; // 里程计数据结构，存储当前的线速度、角速度和角度
};


#endif // __KINEMATICS_H__