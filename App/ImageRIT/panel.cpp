#include "panel.h"
#include "ui_panel.h"
#include "mainwindow.h"
#include <QDebug>

Panel::Panel(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Panel)
{
    ui->setupUi(this);

    p = qobject_cast<MainWindow *>(parent);

    connect(ui->Binarize, SIGNAL(toggled(bool)), this, SLOT(button_toggled(bool)));
    connect(ui->Gamma, SIGNAL(valueChanged(int)), this, SLOT(dial_changed(int)));
}

Panel::~Panel()
{
    delete ui;
}

void Panel::dial_changed(int value)
{
    QObject* obj = sender();
    QString send = QString("{\"%1\": [%2]}").arg(obj->objectName(), QString::number(value));
    QByteArray msg(send.toUtf8());
    qDebug() << send;

    p->client->write(msg);
}

void Panel::button_toggled(bool value)
{
    QObject* obj = sender();
    QString send = QString("{\"%1\": %2}").arg(obj->objectName(), QString::number(value));
    QByteArray msg(send.toUtf8());
    qDebug() << send;

    p->client->write(msg);
}

void Panel::on_server_clicked()
{
    p->pages->setCurrentIndex(0);
}

void Panel::on_selfie_clicked()
{
    p->pages->setCurrentIndex(2);
}
