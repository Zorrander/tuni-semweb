#ifndef METHODSMODEL_H
#define METHODSMODEL_H

#include <QAbstractListModel>

class MethodsModel : public QAbstractListModel
{
    Q_OBJECT

public:
    explicit MethodsModel(QObject *parent = nullptr);

    // Header:
    QVariant headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const override;

    // Basic functionality:
    int rowCount(const QModelIndex &parent = QModelIndex()) const override;

    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override;

private:
};

#endif // METHODSMODEL_H
