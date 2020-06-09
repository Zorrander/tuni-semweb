#include "include/cobot_behavior/tasksmodel.hpp"
#include "include/cobot_behavior/taskslist.hpp"

TasksModel::TasksModel(QObject *parent)
    : QAbstractListModel(parent),
      mList(nullptr)
{
}

int TasksModel::rowCount(const QModelIndex &parent) const
{
    // For list models only the root node (an invalid parent) should return the list's size. For all
    // other (valid) parents, rowCount() should return 0 so that it does not become a tree model.
    if (parent.isValid() || !mList)
        return 0;

    return mList->items().size();
}

QVariant TasksModel::data(const QModelIndex &index, int role) const
{
    if (!index.isValid() || !mList)
        return QVariant();

    const TaskItem item = mList->items().at(index.row());
    switch(role){
        case DescriptionRole:
            return QVariant(item.description);
    }

    return QVariant();
}

QHash<int, QByteArray> TasksModel::roleNames() const
{
    QHash<int, QByteArray> names;
    names[DescriptionRole] = "description";
    return names;
}

TasksList *TasksModel::list() const
{
    return mList;
}

void TasksModel::setList(TasksList *list)
{
    beginResetModel();

    if (mList)
        mList->disconnect(this);

    mList = list;

    if (mList){
        connect(mList, &TasksList::preItemAppended, this, [=](){
            const int index = mList->items().size();
            beginInsertRows(QModelIndex(), index, index);
        });

        connect(mList, &TasksList::postItemAppended, this, [=](){
            endInsertRows();
        });
    }

    endResetModel();
}

void TasksModel::fetch(const QString description)
{
    //TaskInfoDialog mDialog = new TaskInfoDialog(description.toUtf8().constData()) ;
    //mdialog.setModal(true);
    //mDialog.exec();
    int a = 0;
}
