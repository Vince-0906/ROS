#include <QApplication>
#include <QLabel>
#include <QString>
#include <rclcpp/rclcpp.hpp>
#include <status_monitor/msg/system_status.hpp>
#include <thread>
#include <sstream>

using SystemStatus = status_monitor::msg::SystemStatus;

class SystemStatusDisplay : public rclcpp::Node
{
    private:
    rclcpp::Subscription<SystemStatus>::SharedPtr subscriber_;
    QLabel* label_;

    public:
    SystemStatusDisplay() : Node("system_status_display")
    {
        label_ = new QLabel();

        subscriber_ = this->create_subscription<SystemStatus>("system_status",10,[&](const SystemStatus::SharedPtr msg) -> void
        {
            label_->setText(get_qstr_from_msg(msg));
        });
        label_->setText(get_qstr_from_msg(std::make_shared<SystemStatus>()));
        label_->show();
    };

    QString get_qstr_from_msg(const SystemStatus::SharedPtr msg)
    {
        std::stringstream show_str;
        show_str <<"================系统状态显示可视化================\n"<<
        "数据名称: =====数据=====单位\n"<<
        "数据时间: \t" << msg->stamp.sec << "\ts\n"<<
        "主机名称: \t" << msg->host_name << "\t\n"<<
        "CPU使用率: \t" << msg->cpu_percent << "\t%\n"<<
        "内存使用率: \t" << msg->memory_percent << "\t%\n"<<
        "内存总大小: \t" << msg->memory_total << "\tMB\n"<<
        "内存剩余大小: \t" << msg->memory_available << "\tMB\n"<<
        "网络发送数据: \t" << msg->net_sent << "\tMB\n"<<
        "网络接收数据: \t" << msg->net_recv << "\tMB\n"<<
        "=================================================";
        return QString::fromStdString(show_str.str());
    };
    
};
int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    QApplication app(argc, argv);

    auto node =std::make_shared<SystemStatusDisplay>();
    std::thread spin_thread([&]()->void{
        rclcpp::spin(node);//阻塞代码
    });
    spin_thread.detach();
    app.exec();//执行应用,阻塞代码
    return 0;
}