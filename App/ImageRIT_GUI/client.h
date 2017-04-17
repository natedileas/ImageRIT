#ifndef CLIENT_H
#define CLIENT_H

#include <QObject>
#include <QtCore>
#include <QtNetwork>

class Client : public QObject
{
    Q_OBJECT
public:
    Client(QObject *parent = 0);

public slots:
    bool connect(QString host, quint16 port);
    bool write(QByteArray data);

private:
    QTcpSocket *socket;
};

#endif // CLIENT_H
