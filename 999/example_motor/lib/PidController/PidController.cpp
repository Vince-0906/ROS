#include <PidController.h>
#include <Arduino.h>
// PidController类的构造函数，初始化PID参数
    PidController::PidController(float kp, float ki, float kd)
    {
        kp_ = kp;
        ki_ = ki;
        kd_ = kd;
    }


// update函数用于更新PID控制器，返回控制量，提供当前值
    float PidController::update(float current)
    {
        error_ = target_ - current; // 计算误差
        error_sum_ += error_; // 积分误差累加

        // 积分上下限限制
        if (error_sum_ > integral_max_)
        {
            error_sum_ = integral_max_;
        }
        else if (error_sum_ < -integral_max_)
        {
            error_sum_ = -integral_max_;
        }

        d_error_ = error_ - last_error_ ; // 计算微分误差
        last_error_ = error_; // 更新上一次误差
        float output = kp_ * error_ + ki_ * error_sum_ + kd_ * d_error_; // PID公式计算输出
        if (output > out_max_) // 输出上限限制
        {
            output = out_max_;
        }
        else if (output < out_min_) // 输出下限限制
        {
            output = out_min_;
        }
        return output; // 返回控制量
    }
    void PidController::update_target(float target)
    {
        target_ = target;
    }
    void PidController::update_pid(float kp, float ki, float kd)
    {
        kp_ = kp;
        ki_ = ki;
        kd_ = kd;
    }
    void PidController::reset()
    {
        error_ = 0;
        error_sum_ = 0;
        d_error_ = 0;
        last_error_ = 0;
        integral_max_ = 2500;
    }



    void PidController::out_limit(float min, float max)
    {
        out_min_ = min;
        out_max_ = max;
    }