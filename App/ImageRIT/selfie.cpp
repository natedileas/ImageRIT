#include "selfie.h"
#include "ui_selfie.h"
#include <QTime>

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
    // wait 1 second
    QTime dieTime= QTime::currentTime().addSecs(1);
    while (QTime::currentTime() < dieTime)
        QCoreApplication::processEvents(QEventLoop::AllEvents, 100);

    // TODO
    // countdown
    // send timestamp/command over connection
    // prompt for email
    // send email over connection
    p->pages->setCurrentIndex(1);
}
