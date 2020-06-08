#include "include/cobot_behavior/taskslist.hpp"

using namespace std::chrono_literals;

TasksList::TasksList(QObject *parent) : QObject(parent)
{
    node = rclcpp::Node::make_shared("task_client");

    client = node->create_client<cobot_msgs::srv::ReadTasks>("/read_tasks");

    while (!client->wait_for_service(1s)) {
        RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "service not available, waiting again...");
    }
    RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Service connected!");
    std::cout << "Service connected!";
    auto request = std::make_shared<cobot_msgs::srv::ReadTasks::Request>();
    auto result = client->async_send_request(request);

    rclcpp::spin_until_future_complete(node, result);

    for (size_t var = 0; var < result.get()->tasks.size() ; ++var) {
       RCLCPP_INFO(rclcpp::get_logger("rclcpp"), result.get()->tasks[var].name);
       TaskItem item;
       item.description = result.get()->tasks[var].name;
       mItems.append(item);
    }
}

QVector<TaskItem> TasksList::items() const
{
    return mItems;
}

bool TasksList::setItemAt(int index, const TaskItem &item)
{
    if (index < 0 || index >= mItems.size())
        return false;

    const TaskItem &oldItem = mItems.at(index);
    if (item.description == oldItem.description)
        return false;

    mItems[index] = item;
    return true;
}

void TasksList::appendItem()
{
    emit preItemAppended();

    TaskItem item;
    mItems.append(item);

    emit postItemAppended();
}

