#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include "include/cobot_behavior/command.hpp"
#include "include/cobot_behavior/knowledge.hpp"
#include "include/cobot_behavior/tasksmodel.hpp"
#include "include/cobot_behavior/taskslist.hpp"
#include "include/cobot_behavior/robot.hpp"
#include <QQmlContext>
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
using std::placeholders::_1;

class MinimalSubscriber : public rclcpp::Node
{
  public:
    MinimalSubscriber()
    : Node("minimal_subscriber")
    {
      subscription_ = this->create_subscription<std_msgs::msg::String>(
      "topic", 10, std::bind(&MinimalSubscriber::topic_callback, this, _1));
      RCLCPP_INFO(this->get_logger(), "Node initialized");
    }

  private:
    void topic_callback(const std_msgs::msg::String::SharedPtr msg) const
    {
      RCLCPP_INFO(this->get_logger(), "I heard: '%s'", msg->data.c_str());
    }
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
};


int main(int argc, char *argv[])
{
    QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);

    QGuiApplication app(argc, argv);

    QQmlApplicationEngine engine;

    rclcpp::init(argc, argv);
    // auto node = std::make_shared<MinimalSubscriber>() ;

    qmlRegisterType<Command>("CobotCommand",1, 0, "Command");
    qmlRegisterType<Knowledge>("CobotKnowledge",1, 0, "Knowledge");
    qmlRegisterType<TasksModel>("Tasks",1, 0, "Tasks");
    qmlRegisterType<Robot>("Robot",1, 0, "Robot");

    qmlRegisterUncreatableType<TasksList>("TasksList", 1, 0, "TasksList", QStringLiteral("TasksList should not be created in QML"));

    engine.load(QUrl(QStringLiteral("qrc:/main.qml")));
    if (engine.rootObjects().isEmpty())
        return -1;

    TasksList tasksList;
    engine.rootContext()->setContextProperty(QStringLiteral("tasksList"), &tasksList);


    while (rclcpp::ok())
    {
        //std::cout << "Test";
        //rclcpp::spin_some(node);
        app.processEvents();
    }

}
