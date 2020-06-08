#ifndef TASKSMODEL_H
#define TASKSMODEL_H

#include <QAbstractListModel>

class TasksList;

class TasksModel : public QAbstractListModel
{
    Q_OBJECT

    Q_PROPERTY(TasksList *list READ list WRITE setList)

public:
    explicit TasksModel(QObject *parent = nullptr);

    enum {
        DescriptionRole
    };

    // Basic functionality:
    int rowCount(const QModelIndex &parent = QModelIndex()) const override;

    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override;

    virtual QHash<int, QByteArray> roleNames() const override;

    TasksList *list() const;
    void setList(TasksList *list);
    
private:
    TasksList *mList;
};

#endif // TASKSMODEL_H
