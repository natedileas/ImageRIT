#include "selfie.h"
#include "ui_selfie.h"
#include <QTime>
#include <QString>

selfie::selfie(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::selfie)
{
    ui->setupUi(this);
    p = qobject_cast<MainWindow *>(parent);
}

selfie::~selfie()
{
    delete ui;
}

void selfie::on_back_clicked()
{
    p->pages->setCurrentIndex(1);
}

void selfie::on_selfie_b_clicked()
{
    // send timestamp/command over connection
    QString send = QString("{\"selfie\":{\"time\":\"%1\"}}").arg(QTime::currentTime().toString());
    QByteArray msg(send.toUtf8());
    p->client->write(msg);

    // wait 1 second (JUST AN EXAMPLE)
    QTime dieTime= QTime::currentTime().addSecs(3);
    while (QTime::currentTime() < dieTime)
        QCoreApplication::processEvents(QEventLoop::AllEvents, 100);

    // TODO
    // countdown

    // prompt for email
    // send email over connection
    p->pages->setCurrentIndex(1);
}
