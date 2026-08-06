#ifndef LINEAR_MOTION_CONTROLLER_HPP
#define LINEAR_MOTION_CONTROLLER_HPP
#include "motion_control_system/motion_control_interface.hpp"
namespace motion_control_system{
    class LinearMotionController : public MotionController
    {
        private:
        public:
            void start() override;
            void stop() override;
    };
}




#endif // MOTION_CONTROL_INTERFACE_HPP