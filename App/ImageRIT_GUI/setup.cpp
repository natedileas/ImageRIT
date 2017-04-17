#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QTcpSocket>

void setup_ui(MainWindow m, QString hostname, quint16 port)
{
    QTcpSocket socket;
    const int Timeout = 5 * 1000;

    socket.connectToHost(hostname, port);

    if (!socket.waitForConnected(Timeout)) {
                //emit error(socket.error(), socket.errorString());
                return;
    }

    QDataStream in(&socket);
    in.setVersion(QDataStream::Qt_5_0);
    QString setupstr;

    do {
        if (!socket.waitForReadyRead(Timeout)) {
            //emit error(socket.error(), socket.errorString());
            return;
        }

        in.startTransaction();
        in >> setupstr;
    } while (!in.commitTransaction());

    socket.disconnectFromHost();

    // do something with the string received

}
