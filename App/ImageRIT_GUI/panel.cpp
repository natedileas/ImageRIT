#include "panel.h"
#include "ui_panel.h"
#include <QDebug>

Panel::Panel(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Panel)
{
    ui->setupUi(this);

    connect(ui->Binarize, SIGNAL(toggled(bool)), this, SLOT(on_button_toggled(bool)));
    connect(ui->Gamma, SIGNAL(valueChanged(int)), this, SLOT(on_dial_changed(int)));
}

Panel::~Panel()
{
    delete ui;
}

void Panel::on_dial_changed(int value)
{
    QObject* obj = sender();
    QString send = QString("{\"%1\": [%2]}").arg(obj->objectName(), QString::number(value));
    QByteArray msg(send.toUtf8());
    qDebug() << send;

    client.write(msg);
}

void Panel::on_button_toggled(bool value)
{
    QObject* obj = sender();
    QString send = QString("{\"%1\": %2}").arg(obj->objectName(), QString::number(value));
    QByteArray msg(send.toUtf8());
    qDebug() << send;

    client.write(msg);
}
