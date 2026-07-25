#include "rclcpp/rclcpp.hpp"

class PersonNode : public rclcpp::Node
{
    private:
        std::string name_;
        int age_;
    public:
        PersonNode(const std::string & node_name,const std::string & name_value, int age_value)
        :Node(node_name) /*调用父类构造函数，等于python中的super().__init__()*/ 
            {
                this->name_ = name_value;
                this->age_ = age_value;
            };
    void eat(const std::string & food_name)
    {
        RCLCPP_INFO(this->get_logger(),"我是%s,%d岁,爱吃%s",this->name_.c_str(),this->age_,food_name.c_str());
    };
};

int main(int argc,char** argv)
{
    rclcpp::init(argc,argv);
    auto node = std::make_shared<PersonNode>("person_node","Vince",22);
    node->eat("面包");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}