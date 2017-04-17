#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "client.h"
#include <QDebug>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    //connect signals and slots
    connect(ui->binary, SIGNAL(stateChanged(int)), this, SLOT(on_dial_changed(int)));
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_dial_changed(int value)
{
    QObject* obj = sender();
    QString send = QString("{\"%1\": %2}").arg(obj->objectName(), QString::number(value));
    QByteArray msg(send.toUtf8());
    qDebug() << send;
    //qDebug() << QStringLiteral("Val: %1").arg(value);
    //qDebug() << QStringLiteral("Sender: %1").arg(obj->objectName());

    client.write(msg);
}
