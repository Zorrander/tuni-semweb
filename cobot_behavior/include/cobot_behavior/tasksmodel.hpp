#ifndef TASKSMODEL_H
#define TASKSMODEL_H

#include <QAbstractListModel>

class TasksModel : public QAbstractListModel
{
    Q_OBJECT

public:
    explicit TasksModel(QObject *parent = nullptr);

    // Basic functionality:
    int rowCount(const QModelIndex &parent = QModelIndex()) const override;

    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override;

private:
};

#endif // TASKSMODEL_H
