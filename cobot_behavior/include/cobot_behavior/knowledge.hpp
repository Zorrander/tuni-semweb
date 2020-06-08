#ifndef KNOWLEDGE_H
#define KNOWLEDGE_H

#include <QObject>
#include <QString>
#include <QStringListModel>
#include <string>
#include "rclcpp/rclcpp.hpp"
#include "cobot_msgs/srv/export.hpp"

class Knowledge : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString filename READ filename WRITE setFilename NOTIFY filenameChanged)
    Q_PROPERTY(QStringListModel *tasks READ tasks)

public:
    explicit Knowledge(QObject *parent = nullptr);
    QString filename() ;
    void setFilename(const QString &value);
    QStringListModel *tasks();

signals:
    void filenameChanged();

public slots:
    void export_ontology(const QString qstr_filename);

private:
    std::shared_ptr<rclcpp::Node> node ;
    rclcpp::Client<cobot_msgs::srv::Export>::SharedPtr client;
    QString m_filename;
};


#endif // KNOWLEDGE_H
