#include "panel.h"
#include "ui_panel.h"
#include "mainwindow.h"
#include "secretserver.h"
#include <QDebug>

Panel::Panel(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Panel)
{
    ui->setupUi(this);

    p = qobject_cast<MainWindow *>(parent);

    connect(ui->Binarize, SIGNAL(toggled(bool)), this, SLOT(button_toggled(bool)));
    connect(ui->Gamma, SIGNAL(valueChanged(int)), this, SLOT(dial_changed(int)));

    //affine
    connect(ui->rotate, SIGNAL(valueChanged(int)), this, SLOT(affine(int)));
    connect(ui->scale, SIGNAL(valueChanged(int)), this, SLOT(affine(int)));

    // add secret server button (double click on image in selfie view)
    SecretServer *s = new SecretServer();
    s->installOn(ui->server_label);
    connect(s, SIGNAL(doubleclick()), this, SLOT(go_to_server()));
}

Panel::~Panel()
{
    delete ui;
}

void Panel::affine(int value)
{
    int scale_ = ui->scale->value();
    int angle_ = ui->rotate->value();

    QString send = QString("{\"affine\": [%1, %2]}").arg(QString::number(angle_), QString::number(scale_));
    QByteArray msg(send.toUtf8());
    qDebug() << send;

    p->client->write(msg);
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

void Panel::go_to_server()
{
    p->pages->setCurrentIndex(1);
}


void Panel::on_selfie_2_clicked()
{
    QPushButton * b = qobject_cast<QPushButton *>(sender());
    b->setEnabled(false);  // no more clicks accepted until exit
    // send timestamp/command over connection
    // wait 3 seconds (JUST AN EXAMPLE)
    QTime dieTime= QTime::currentTime().addSecs(3);
    while (QTime::currentTime() < dieTime)
        QCoreApplication::processEvents(QEventLoop::AllEvents, 100);

    // TODO
    // countdown
    QString send = "{\"selfie\":0}";
    QByteArray msg(send.toUtf8());
    p->client->write(msg);

    b->setEnabled(true);  // now accept clicks again
}


void Panel::on_email_clicked()
{
    // prompt for email
    // send email over connection
    QString email = ui->email_entry->text();

    QString message = QString("{\"email\":\"%1\"}").arg(email);
    QByteArray msg(message.toUtf8());
    p->client->write(msg);
    qDebug() << message;
}

void Panel::on_affine_reset_clicked()
{
    ui->rotate->setValue(0);
    ui->scale->setValue(50);
}

void Panel::on_color_reset_clicked()
{
    ui->Gamma->setValue(74);
    ui->Gamma_2->setValue(0);
}
