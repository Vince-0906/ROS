#include <iostream>
#include "motion_control_system/spin_motion_controller.hpp"

namespace motion_control_system{
    void SpinMotionController::start()
    {
        //实现旋转运动控制逻辑
        std::cout << "SpinMotionController started." << std::endl;
    }

    void SpinMotionController::stop()
    {
        //停止运动控制
        std::cout << "SpinMotionController stopped." << std::endl;
    }
}//namespace motion_control_system

#include "pluginlib/class_list_macros.hpp"
PLUGINLIB_EXPORT_CLASS(motion_control_system::SpinMotionController, motion_control_system::MotionController)
//让SpinMotionController类可以被Classloader插件加载器识别和加载，并且它实现了MotionController接口