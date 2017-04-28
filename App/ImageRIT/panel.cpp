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
