#ifndef COMMAND_H
#define COMMAND_H

#include <QObject>
#include <QString>

class Command : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString action READ action WRITE setAction NOTIFY actionChanged)

public:
    explicit Command(QObject *parent = nullptr);

    QString action() ;
    void setAction(const QString &value);

signals:
    void actionChanged();

public slots:
    void send(const QString value);

private:
    QString m_action;
};

#endif // COMMAND
