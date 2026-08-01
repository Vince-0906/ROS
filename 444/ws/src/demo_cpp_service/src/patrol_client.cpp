#include <rclcpp/rclcpp.hpp>
#include <chapt4_interfaces/srv/patrol.hpp>
#include <chrono>
#include <ctime>
#include <rcl_interfaces/msg/parameter.hpp>
#include <rcl_interfaces/msg/parameter_value.hpp>
#include <rcl_interfaces/msg/parameter_type.hpp>
#include <rcl_interfaces/srv/set_parameters.hpp>


using Patrol = chapt4_interfaces::srv::Patrol;
using namespace std::chrono_literals;
using SetP =rcl_interfaces::srv::SetParameters;

class PatrolClient: public rclcpp::Node
{
    private:
        rclcpp::TimerBase::SharedPtr timer_;
        rclcpp::Client<Patrol>::SharedPtr patrol_client_;

    public:
        PatrolClient(const std::string &node_name): Node(node_name)
        {
            srand(time(NULL));//初始化随机数种子
            patrol_client_ =this ->create_client<Patrol>("patrol");
            timer_ =this->create_wall_timer(5s,[&]()->void{
                // 1.检测服务是否可用
                while(!this->patrol_client_->wait_for_service(1s))
                {
                    if(!rclcpp::ok()){
                        RCLCPP_ERROR(this->get_logger(),"等到服务上线中,rclcpp死了");
                        return;
                    }
                    RCLCPP_INFO(this->get_logger(),"等待服务上线中...");
                }

                // 2.创建请求对象
                auto request =std::make_shared<Patrol::Request>();
                request->target_x=rand()%15;
                request->target_y=rand()%15;
                RCLCPP_INFO(this->get_logger(),"准备好目标点,x=%f,y=%f",request->target_x,request->target_y);

                // 3.发送请求
                this->patrol_client_->async_send_request(request,[&](rclcpp::Client<Patrol>::SharedFuture result_future)->void{
                    auto response =result_future.get();
                    if(response->result==Patrol::Response::SUCCESS)
                    {
                        RCLCPP_INFO(this->get_logger(),"服务调用成功,正在巡逻");
                    }
                    if(response->result==Patrol::Response::FAIL)
                    {
                        RCLCPP_ERROR(this->get_logger(),"服务调用失败,目标点不合法");
                    }
                });
            });
            
        }
        /*
        *创建客户端发送请求，返回结果*/
       SetP::Response::SharedPtr call_set_parameters(const rcl_interfaces::msg::Parameter &param)
       {
            auto param_client =this ->create_client<SetP>("/turtle_control/set_parameters");
                // 1.检测服务是否可用
                while(!param_client->wait_for_service(1s))
                {
                    if(!rclcpp::ok()){
                        RCLCPP_ERROR(this->get_logger(),"等到服务上线中,rclcpp死了");
                        return nullptr;
                    }
                    RCLCPP_INFO(this->get_logger(),"等待服务上线中...");
                }

                // 2.创建请求对象
                auto request =std::make_shared<SetP::Request>();
                request->parameters.push_back(param);

                // 3.发送请求
                auto future =param_client->async_send_request(request);
                rclcpp::spin_until_future_complete(this->get_node_base_interface(),future);
                auto response =future.get();
                return response;
       }
               /*
        *更新参数K*/
       void update_server_param_k(double k)
       {
        // 1.创建参数对象
        auto param =rcl_interfaces::msg::Parameter();
        param.name="k";
        // 2.创建参数值对象
        auto param_value =rcl_interfaces::msg::ParameterValue();
        param_value.type = rcl_interfaces::msg::ParameterType::PARAMETER_DOUBLE;
        param_value.double_value =k;
        param.value =param_value;
        // 3.请求更新参数并处理
        auto response =call_set_parameters(param);
        if(response == NULL){
            RCLCPP_ERROR(this->get_logger(),"更新参数失败");
            return;
        }
        for (auto result:response->results)
        {
            if(result.successful==false)
            {
                RCLCPP_ERROR(this->get_logger(),"更新参数失败,原因:%s",result.reason.c_str());
            }
            else
            {
                RCLCPP_INFO(this->get_logger(),"更新参数成功");
            }
        }
       }

};
int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    auto node= std::make_shared<PatrolClient>("patrol_client");
    node->update_server_param_k(4.0);
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}