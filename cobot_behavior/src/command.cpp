#include <QObject>
#include <QString>

#include <iostream>

#include "include/cobot_behavior/command.hpp"

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"


Command::Command(QObject *parent) :
    QObject(parent)
{
    node = rclcpp::Node::make_shared("minimal_publisher");
    publisher = node->create_publisher<std_msgs::msg::String>("topic", 10);
}

QString Command::action()
{
    return m_action;
}

void Command::setAction(const QString &value)
{
    if (value != m_action) {
       m_action = value;
       emit actionChanged();
    }
}

void Command::send(const QString value){
    // std::cin.ignore();
    std_msgs::msg::String message;
    message.data = value.toUtf8().constData();
    RCLCPP_INFO(node->get_logger(), "Publishing: '%s'", message.data.c_str());
    publisher->publish(message);
    rclcpp::spin_some(node);
}

