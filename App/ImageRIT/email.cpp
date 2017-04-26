#include "email.h"
#include "ui_email.h"
#include <QDebug>

Email::Email(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Email)
{
    ui->setupUi(this);
    p = qobject_cast<MainWindow *>(parent);
}

Email::~Email()
{
    delete ui;
}

void Email::on_emailme_clicked()
{
    // prompt for email
    // send email over connection
    QString email = ui->email_entry->text();

    QString message = QString("{\"email\":\"%1\"}").arg(email);
    QByteArray msg(message.toUtf8());
    p->client->write(msg);
    qDebug() << message;
    p->pages->setCurrentIndex(1);
}

void Email::on_back_clicked()
{
    p->pages->setCurrentIndex(1);
}
