#include "client.h"

static inline QByteArray IntToArray(qint32 source);

Client::Client(QObject *parent) : QObject(parent)
{
    socket = new QTcpSocket(this);
}

bool Client::connect(QString host, quint16 port)
{
    disconnect_from_host(true);

    socket->connectToHost(host, port);
    return socket->waitForConnected();
}

bool Client::write(QByteArray data)
{
    if(socket->state() == QAbstractSocket::ConnectedState)
    {
        socket->write(IntToArray(data.size())); //write size of data
        socket->write(data); //write the data itself
        return socket->waitForBytesWritten();
    }
    else
        return false;
}

void Client::disconnect_from_host(bool)
{
    write(QByteArray("{\"bye\":0}"));
    socket->close();
    socket->disconnectFromHost();
}

QByteArray IntToArray(qint32 source) //Use qint32 to ensure that the number have 4 bytes
{
    //Avoid use of cast, this is the Qt way to serialize objects
    QByteArray temp;
    QDataStream data(&temp, QIODevice::ReadWrite);
    data << source;
    return temp;
}
