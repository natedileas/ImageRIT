#include "mainwindow.h"
#include <QApplication>
#include <QCoreApplication>
#include <QStyleFactory>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    a.setStyle(QStyleFactory::create("Android"));
    MainWindow w;
    w.show();

    int ret = a.exec();
    return ret;
}
