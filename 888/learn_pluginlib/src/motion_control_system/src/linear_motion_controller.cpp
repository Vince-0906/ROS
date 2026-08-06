#include <iostream>
#include "motion_control_system/linear_motion_controller.hpp"

namespace motion_control_system{
    void LinearMotionController::start()
    {
        //实现直线运动控制逻辑
        std::cout << "LinearMotionController started." << std::endl;
    }

    void LinearMotionController::stop()
    {
        //停止运动控制
        std::cout << "LinearMotionController stopped." << std::endl;
    }
}//namespace motion_control_system

#include "pluginlib/class_list_macros.hpp"
PLUGINLIB_EXPORT_CLASS(motion_control_system::LinearMotionController, motion_control_system::MotionController)
//让LinearMotionController类可以被Classloader插件加载器识别和加载，并且它实现了MotionController接口