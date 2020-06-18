#ifndef ROBOT_H
#define ROBOT_H

#include <QObject>
#include <QString>
#include "rclcpp/rclcpp.hpp"
#include "cobot_msgs/msg/command.hpp"
#include "std_msgs/msg/string.hpp"
#include "cobot_msgs/srv/named_target.hpp"
#include "cobot_msgs/srv/move_gripper.hpp"
#include "cobot_msgs/srv/grasp.hpp"
#include <QQmlListProperty>

class Robot : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString targetname READ targetname WRITE setTargetname NOTIFY targetnameChanged)
    Q_PROPERTY(QStringList targetlist READ targetlist NOTIFY targetlisthanged)
    Q_PROPERTY(qreal targetlist READ targetlist NOTIFY targetlisthanged)
    Q_PROPERTY(QList<qreal> ee_pose READ ee_pose NOTIFY eeposeChanged)

public:
    explicit Robot(QObject *parent = nullptr);
    QString targetname() ;
    QStringList targetlist();
    QList<qreal> ee_pose();
    void setTargetname(const QString &value);

signals:
    void targetnameChanged();
    void targetlisthanged();
    void eeposeChanged(QQmlListProperty<qreal>);


public slots:
    void save(const QString value);
    void move_target(const QString value);
    void open_gripper();
    void close_gripper();
    void grasp1();
    void routine(const QString value);

private:
    std::shared_ptr<rclcpp::Node> node ;
    rclcpp::Client<cobot_msgs::srv::NamedTarget>::SharedPtr store_pose_client;
    rclcpp::Client<cobot_msgs::srv::NamedTarget>::SharedPtr move_named_target_client;
    rclcpp::Client<cobot_msgs::srv::MoveGripper>::SharedPtr move_gripper_client;
    rclcpp::Client<cobot_msgs::srv::Grasp>::SharedPtr grasp_client;
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr  command_publisher ;
    QString m_targetname;
    QStringList m_target_list;
    QList<qreal> m_ee_pose;
};


#endif // ROBOT_H
