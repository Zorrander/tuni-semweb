#ifndef ROBOT_H
#define ROBOT_H

#include <QObject>
#include <QString>
#include "rclcpp/rclcpp.hpp"
#include "cobot_msgs/srv/named_target.hpp"
#include "cobot_msgs/srv/move_gripper.hpp"

class Robot : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString targetname READ targetname WRITE setTargetname NOTIFY targetnameChanged)
    Q_PROPERTY(QStringList targetlist READ targetlist NOTIFY targetlisthanged)

public:
    explicit Robot(QObject *parent = nullptr);
    QString targetname() ;
    QStringList targetlist();
    void setTargetname(const QString &value);

signals:
    void targetnameChanged();
    void targetlisthanged();

public slots:
    void save(const QString value);
    void move_target(const QString value);
    void open_gripper();
    void close_gripper();

    void routine();


private:
    std::shared_ptr<rclcpp::Node> node ;
    rclcpp::Client<cobot_msgs::srv::NamedTarget>::SharedPtr store_pose_client;
    rclcpp::Client<cobot_msgs::srv::NamedTarget>::SharedPtr move_named_target_client;
    rclcpp::Client<cobot_msgs::srv::MoveGripper>::SharedPtr move_gripper_client;
    QString m_targetname;
    QStringList m_target_list;
};


#endif // ROBOT_H
