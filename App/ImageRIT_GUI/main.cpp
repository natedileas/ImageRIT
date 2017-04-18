#include "mainwindow.h"
//#include "setup.h"
#include "client.h"
#include "panel.h"
#include <QApplication>
#include <QCoreApplication>
#include <QTime>

int main(int argc, char *argv[])
{
    QString hostname = "129.21.52.194";
    quint16 port = 12349;

    QByteArray hi("keepalive");

    QApplication a(argc, argv);

    MainWindow w;
    w.show();


    Panel b;
    // simulate connecting
    QTime dieTime= QTime::currentTime().addSecs(1);
    while (QTime::currentTime() < dieTime)
        QCoreApplication::processEvents(QEventLoop::AllEvents, 100);

    b.client.connect(hostname, port);
    //b.client.write(hi);
    w.setCentralWidget(&b);

    int ret = a.exec();
    //b.client.close();
    return ret;
}