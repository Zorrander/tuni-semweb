#include "include/cobot_behavior/robot.hpp"

Robot::Robot(QObject *parent) :
    QObject(parent)
{
    node = rclcpp::Node::make_shared("minimal_client");
    store_pose_client = node->create_client<cobot_msgs::srv::NamedTarget>("store_position");
    move_named_target_client = node->create_client<cobot_msgs::srv::NamedTarget>("move_to");
    grasp_client = node->create_client<cobot_msgs::srv::Grasp>("grasp");
    move_gripper_client = node->create_client<cobot_msgs::srv::MoveGripper>("move_gripper");
    command_publisher = node->create_publisher<std_msgs::msg::String>("command", 10);
    ee_pose = node->create_subscription<std_msgs::msg::String>(
    "topic", 10, std::bind(&MinimalSubscriber::topic_callback, this, _1));
    m_target_list = (QStringList()<<"ready");
}

QString Robot::targetname()
{
    return m_targetname;
}

QStringList Robot::targetlist()
{
    return m_target_list;
}

QList<qreal> Robot::ee_pose()
{
    return m_ee_pose;
}

void Robot::setTargetname(const QString &value)
{
    if (value != m_targetname) {
       m_targetname = value;
       emit targetnameChanged();
    }
}

void Robot::save(const QString value){
    auto request = std::make_shared<cobot_msgs::srv::NamedTarget::Request>();
    request->name = value.toUtf8().constData();
    m_target_list.append(value);
    emit targetlisthanged();
    auto result = store_pose_client->async_send_request(request);
    rclcpp::spin_some(node);
}

void Robot::move_target(const QString value)
{
    auto request = std::make_shared<cobot_msgs::srv::NamedTarget::Request>();
    request->name = value.toUtf8().constData();
    auto result = move_named_target_client->async_send_request(request);
    rclcpp::spin_some(node);
}

void Robot::open_gripper()
{
    auto request = std::make_shared<cobot_msgs::srv::MoveGripper::Request>();
    auto result = move_gripper_client->async_send_request(request);
    rclcpp::spin_some(node);
}

void Robot::close_gripper()
{
    auto request = std::make_shared<cobot_msgs::srv::MoveGripper::Request>();
    request->width = 0.01;
    auto result = move_gripper_client->async_send_request(request);
    rclcpp::spin_some(node);
}

void Robot::grasp1()
{
    auto request = std::make_shared<cobot_msgs::srv::Grasp::Request>();
    request->width = 0.01;
    request->force = 50.0;
    auto result = grasp_client->async_send_request(request);
    rclcpp::spin_some(node);
}

void Robot::routine(const QString value)
{
    auto message = std_msgs::msg::String();
    message.data = value.toUtf8().constData() ;
    command_publisher->publish(message);
    std::cout << "Sent";
    rclcpp::spin_some(node);
    // for (size_t var = 0; var < 10; ++var) {
    //    this->close_gripper();
    //    this->open_gripper();
    // }
}

void Robot::setEe_pose(const QList<qreal> &ee_pose)
{
    m_ee_pose = ee_pose;
}


