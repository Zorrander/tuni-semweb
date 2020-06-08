#ifndef TASKSLIST_HPP
#define TASKSLIST_HPP

#include "rclcpp/rclcpp.hpp"
#include "cobot_msgs/srv/read_tasks.hpp"
#include <QObject>
#include <QVector>

struct TaskItem {
    QString description;
};

class TasksList : public QObject
{
    Q_OBJECT
public:
    explicit TasksList(QObject *parent = nullptr);

    QVector<TaskItem> items() const;

    bool setItemAt(int index, const TaskItem &item);


public slots:
    void appendItem();
    // void removeItem();

signals:
    void preItemAppended();
    void postItemAppended();

    // void preItemRemoved(int index);
    // void postItemRemoved();

private:
    QVector<TaskItem> mItems;
    std::shared_ptr<rclcpp::Node> node ;
    rclcpp::Client<cobot_msgs::srv::ReadTasks>::SharedPtr client;
};

#endif // TASKSLIST_HPP
