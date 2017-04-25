#include "config.h"
#include "ui_config.h"
#include "mainwindow.h"
#include <QString>
#include <QDebug>
Config::Config(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Config)
{
    ui->setupUi(this);
    p = qobject_cast<MainWindow *>(parent);
}

Config::~Config()
{
    delete ui;
}

void Config::on_reconnect_clicked()
{
    // TODO add connection checking/ disconnect functionality
    // TODO check if fields arefilled
    QString hostname = ui->hostname->text();
    qint32 port = ui->port->text().toInt();
    // if they are, connect

    //TODO also send server code

    qDebug() << QString("%1 %2").arg(hostname, QString::number(port));

    if (p->client->connect(hostname, port)){
        // if connect succeeds go to the panel view
        qDebug() << "Connected";
    }
}

void Config::on_back_clicked()
{
    p->pages->setCurrentIndex(1);
}

void Config::on_disconnect_clicked()
{
    p->client->disconnect_from_host(true);
    qDebug() << "Disconnected";
}
