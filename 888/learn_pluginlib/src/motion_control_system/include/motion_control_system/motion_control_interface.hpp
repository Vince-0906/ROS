#ifndef MOTION_CONTROL_INTERFACE_HPP
#define MOTION_CONTROL_INTERFACE_HPP

namespace motion_control_system{
    class MotionController
    {
        private:
        public:
            virtual void start() = 0;
            virtual void stop() = 0;
    };
}




#endif // MOTION_CONTROL_INTERFACE_HPP