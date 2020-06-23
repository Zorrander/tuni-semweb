#ifndef COMMAND_H
#define COMMAND_H

#include <QObject>
#include <QString>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "cobot_msgs/msg/command.hpp"

class Command : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString actionlist READ actionlist NOTIFY actionlistChanged)
    Q_PROPERTY(QStringList objectlist READ objectlist NOTIFY objectlistChanged)

public:
    explicit Command(QObject *parent = nullptr);
    QStringList actionlist() ;
    QStringList objectlist() ;

signals:
    void actionlistChanged();
    void objectlistChanged();

public slots:
    void send(const QString cmd);
    void plan(const QString qstr_action, const QString qstr_targets);

private:
    std::shared_ptr<rclcpp::Node> node ;
    QString m_cmd;
    QStringList m_actionlist;
    QStringList m_targetlist;
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr cmd_publisher;
    rclcpp::Publisher<cobot_msgs::msg::Command>::SharedPtr plan_publisher;
};

#endif // COMMAND
