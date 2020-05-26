#ifndef COMMAND_H
#define COMMAND_H

#include <QObject>
#include <QString>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

class Command : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString action READ action WRITE setAction NOTIFY actionChanged)

public:
    explicit Command(QObject *parent = nullptr);
    QString action() ;
    void setAction(const QString &value);

signals:
    void actionChanged();

public slots:
    void send(const QString value);

private:
    std::shared_ptr<rclcpp::Node> node ;
    QString m_action;
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher;
};

#endif // COMMAND
