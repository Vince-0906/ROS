#include <iostream>
#include "motion_control_system/zshaped_motion_controller.hpp"

namespace motion_control_system{
    void ZShapedMotionController::start()
    {
        //实现Z形运动控制逻辑
        std::cout << "ZShapedMotionController started." << std::endl;
    }

    void ZShapedMotionController::stop()
    {
        //停止运动控制
        std::cout << "ZShapedMotionController stopped." << std::endl;
    }
}//namespace motion_control_system

#include "pluginlib/class_list_macros.hpp"
PLUGINLIB_EXPORT_CLASS(motion_control_system::ZShapedMotionController, motion_control_system::MotionController)
//让ZShapedMotionController类可以被Classloader插件加载器识别和加载，并且它实现了MotionController接口