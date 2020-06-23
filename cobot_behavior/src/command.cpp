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
    cmd_publisher = node->create_publisher<std_msgs::msg::String>("command", 10);
    plan_publisher = node->create_publisher<cobot_msgs::msg::Command>("plan_request", 10);
    m_actionlist = QStringList() << "Give" << "Take" << "Open" << "Close" ;
    m_targetlist = QStringList() << "Separator" << "Common rail" << "Piston" << "Tappet" << "Screw" << "Bolt" << "Tool" << "PLC";
}

void Command::send(const QString cmd)
{
    // std::cin.ignore();
    std_msgs::msg::String message;
    message.data = cmd.toUtf8().constData();
    cmd_publisher->publish(message);
    rclcpp::spin_some(node);
}

void Command::plan(const QString qstr_action, const QString qstr_targets)
{
    // std::cin.ignore();
    cobot_msgs::msg::Command message;
    message.action = qstr_action.toUtf8().constData();
    message.targets.insert(message.targets.end(), qstr_targets.toUtf8().constData()) ;
    RCLCPP_INFO(node->get_logger(), "Publishing: '%s' - '%s", (message.action.c_str(), message.targets[0].c_str()));
    plan_publisher->publish(message);
    rclcpp::spin_some(node);
}

QStringList Command::actionlist()
{
    return m_actionlist;
}

QStringList Command::objectlist()
{
    return m_targetlist;
}


