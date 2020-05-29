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
    Q_PROPERTY(QString action READ action WRITE setAction NOTIFY actionChanged)
    Q_PROPERTY(QString targets READ targets WRITE setTargets NOTIFY targetsChanged)

public:
    explicit Command(QObject *parent = nullptr);
    QString action() ;
    QString targets() ;
    void setAction(const QString &value);
    void setTargets(const QString &value);

signals:
    void actionChanged();
    void targetsChanged();

public slots:
    void send(const QString qstr_action, const QString qstr_targets);

private:
    std::shared_ptr<rclcpp::Node> node ;
    QString m_action;
    QString m_targets;
    rclcpp::Publisher<cobot_msgs::msg::Command>::SharedPtr publisher;
};

#endif // COMMAND
