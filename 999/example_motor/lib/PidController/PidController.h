#ifndef __PID_CONTROLLER_H__
#define __PID_CONTROLLER_H__

class PidController
{
    public:
        PidController() = default;
        PidController(float kp, float ki, float kd);
    private:
        // PID参数
        float target_;
        float out_min_;
        float out_max_;
        float kp_;
        float ki_;
        float kd_;
        float integral_max_ = 2500; // 积分上限
        // PID计算相关变量
        float error_;
        float error_sum_; // 积分误差
        float d_error_; // 微分误差(变化率)
        float last_error_; // 上一次误差
    public:
        float update(float current); // 更新PID控制器，返回控制量，提供当前值
        void update_target(float target); // 更新目标值
        void update_pid(float kp, float ki, float kd); // 更新PID参数
        void reset(); // 重置PID控制器
        void out_limit(float min, float max); // 设置输出上下限

};


#endif // __PID_CONTROLLER_H__