#include <QObject>
#include <QString>
#include <iostream>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

#include "include/cobot_behavior/skill.hpp"
using std::placeholders::_1;

class MinimalSubscriber : public rclcpp::Node
{
  public:
    MinimalSubscriber()
    : Node("minimal_subscriber")
    {
      subscription_ = this->create_subscription<std_msgs::msg::String>(
      "topic", 10, std::bind(&MinimalSubscriber::topic_callback, this, _1));
      RCLCPP_INFO(this->get_logger(), "Node initialized");
    }

  private:
    void topic_callback(const std_msgs::msg::String::SharedPtr msg) const
    {
      RCLCPP_INFO(this->get_logger(), "I heard: '%s'", msg->data.c_str());
    }
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
};


Skill::Skill(QObject *parent) :
    QObject(parent)
{
}

QString Skill::action()
{
    return m_action;
}

void Skill::setAction(const QString &value)
{
    if (value != m_action) {
       m_action = value;
       emit actionChanged();
    }
}

void Skill::send(const QString value){
    std::cout << "Hello world: " << value.toUtf8().constData();
}

