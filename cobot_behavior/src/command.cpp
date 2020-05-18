#include <QObject>
#include <QString>
#include "include/cobot_behavior/command.hpp"
#include <iostream>

Command::Command(QObject *parent) :
    QObject(parent)
{
}

QString Command::action()
{
    return m_action;
}

void Command::setAction(const QString &value)
{
    if (value != m_action) {
       m_action = value;
       emit actionChanged();
    }
}

void Command::send(const QString value){
    std::cout << "Hello world: " << value.toUtf8().constData();
}

