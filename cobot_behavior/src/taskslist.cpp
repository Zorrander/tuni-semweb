#include "include/cobot_behavior/taskslist.hpp"

TasksList::TasksList(QObject *parent) : QObject(parent)
{
    mItems.append({QStringLiteral("TestA")});
    mItems.append({QStringLiteral("TestB")});
    mItems.append({QStringLiteral("TestC")});
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

