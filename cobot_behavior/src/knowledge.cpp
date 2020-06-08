#include "include/cobot_behavior/knowledge.hpp"

Knowledge::Knowledge(QObject *parent) :
    QObject(parent)
{
    node = rclcpp::Node::make_shared("minimal_client");
    client = node->create_client<cobot_msgs::srv::Export>("export_onto");
}

QString Knowledge::filename()
{
    return m_filename;
}


void Knowledge::setFilename(const QString &value)
{
    if (value != m_filename) {
       m_filename = value;
       emit filenameChanged();
    }
}

void Knowledge::export_ontology(const QString qstr_filename){
    auto request = std::make_shared<cobot_msgs::srv::Export::Request>();
    request->filename = qstr_filename.toUtf8().constData();
    auto result = client->async_send_request(request);
    rclcpp::spin_some(node);
}

