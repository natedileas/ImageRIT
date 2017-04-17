#include "mainwindow.h"
//#include "setup.h"
#include "client.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QString hostname = "129.21.52.194";
    quint16 port = 12349;

    QByteArray hi("keepalive");

    QApplication a(argc, argv);

    MainWindow w;
    w.client.connect(hostname, port);
    w.client.write(hi);
    w.show();

    int ret = a.exec();
    //client.close();
    return ret;
}
