#include <Kinematics.h>
    // 设置两轮之间的距离，单位为米
    void Kinematics::set_wheel_distance(float distance)
    {
        wheel_distance = distance;
    }
    
    // 设置电机参数
    void Kinematics::set_motor_param(uint8_t id,float per_pulse_distance)
    {
        motor_param[id].per_pulse_distance = per_pulse_distance;
    }
    // 运动学正解，将两个轮子的实时速度转换为当前实时角速度和线速度
    void Kinematics::kinematics_forward(float left_speed,float right_speed,float *out_linear_speed,float *out_angular_speed)
    {
        *out_linear_speed = (left_speed + right_speed) / 2;
        *out_angular_speed = (right_speed - left_speed) / wheel_distance;
    }
    // 运动学逆解，将当前目标角速度和线速度转换为两个轮子目标转速
    void Kinematics::kinematics_inverse(float linear_speed,float angular_speed,float *out_left_speed,float *out_right_speed)
    {
        *out_left_speed = linear_speed - angular_speed * wheel_distance / 2;
        *out_right_speed = linear_speed + angular_speed * wheel_distance / 2;
    }
    // 输入：左右轮脉冲速度，当前时间，输出：电机速度和编码器计数值
    void Kinematics::update_motor_speed(uint64_t current_time,int32_t left_tick,int32_t right_tick)
    {
        int16_t delta_tick[2]= {0,0}; // 用于两次读取之间的编码器计数值变化量
        
        uint16_t dt = current_time - last_update_time; // 计算时间间隔
        delta_tick[0] = left_tick - motor_param[0].last_encoder_ticks;
        delta_tick[1] = right_tick - motor_param[1].last_encoder_ticks;
        // 计算速度
        motor_param[0].motor_speed = delta_tick[0]*0.10345/dt*1000;
        motor_param[1].motor_speed = delta_tick[1]*0.10345/dt*1000;
        // 更新
        motor_param[0].last_encoder_ticks = left_tick;
        motor_param[1].last_encoder_ticks = right_tick;
        last_update_time = current_time;

        update_odom(dt); // 更新里程计数据

    }
    // 获取电机速度，返回速度
    int16_t Kinematics::get_motor_speed(uint8_t id)
    {
        return motor_param[id].motor_speed;
    }

odom_t& Kinematics::get_odom()
{
    return odom;
}
void Kinematics::update_odom(uint16_t dt)
{
    float dt_s = dt / 1000.0; // 将毫秒转换为秒
    // 获取实时角速度和线速度
    this->kinematics_forward(motor_param[0].motor_speed, motor_param[1].motor_speed, &odom.linear_speed, &odom.angular_speed);
    odom.linear_speed = odom.linear_speed/1000.0; // 将线速度从mm/s转换为m/s
    // 角度积分
    odom.angle += odom.angular_speed * dt_s; // 角度积分
    TransAngleInPI(odom.angle, odom.angle); // 将角度限制在[-π, π]范围内
    // 计算机器人的行走距离(沿自身前进方向的)
    float delta_distance = odom.linear_speed * dt_s;
    odom.x += delta_distance * cos(odom.angle); // 分解x坐标
    odom.y += delta_distance * sin(odom.angle); // 分解y坐标
}
void Kinematics::TransAngleInPI(float angle,float &out_angle)
{
    if (angle > M_PI)
    {
        out_angle = angle - 2 * M_PI;
    }
    else if (angle < -M_PI)
    {
        out_angle = angle + 2 * M_PI;
    }
    else
    {
        out_angle = angle;
    }
}