#include <QObject>
#include <QString>

#include <iostream>

#include "include/cobot_behavior/command.hpp"

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "cobot_msgs/msg/command.hpp"

Command::Command(QObject *parent) :
    QObject(parent)
{
    node = rclcpp::Node::make_shared("minimal_publisher");
    publisher = node->create_publisher<cobot_msgs::msg::Command>("plan_request", 10);
}

QString Command::action()
{
    return m_action;
}

QString Command::targets()
{
    return m_targets;
}

void Command::setAction(const QString &value)
{
    if (value != m_action) {
       m_action = value;
       emit actionChanged();
    }
}

void Command::setTargets(const QString &value)
{
    if (value != m_targets) {
       m_targets = value;
       emit targetsChanged();
    }
}

void Command::send(const QString qstr_action, const QString qstr_targets){
    // std::cin.ignore();
    cobot_msgs::msg::Command message;
    message.action = qstr_action.toUtf8().constData();
    message.targets.insert(message.targets.end(), qstr_targets.toUtf8().constData()) ;
    RCLCPP_INFO(node->get_logger(), "Publishing: '%s' - '%s", (message.action.c_str(), message.targets[0].c_str()));
    publisher->publish(message);
    rclcpp::spin_some(node);
}

