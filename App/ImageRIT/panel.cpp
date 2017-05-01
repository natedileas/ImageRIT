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
    //connect(ui->Gamma, SIGNAL(valueChanged(int)), this, SLOT(dial_changed(int)));

    //affine
    connect(ui->rotate, SIGNAL(valueChanged(int)), this, SLOT(affine(int)));
    connect(ui->scale, SIGNAL(valueChanged(int)), this, SLOT(affine(int)));

    // color
    connect(ui->r1, SIGNAL(valueChanged(int)), this, SLOT(color_changed(int)));
    connect(ui->r2, SIGNAL(valueChanged(int)), this, SLOT(color_changed(int)));
    connect(ui->r3, SIGNAL(valueChanged(int)), this, SLOT(color_changed(int)));
    connect(ui->r4, SIGNAL(valueChanged(int)), this, SLOT(color_changed(int)));
    connect(ui->r5, SIGNAL(valueChanged(int)), this, SLOT(color_changed(int)));
    connect(ui->g1, SIGNAL(valueChanged(int)), this, SLOT(color_changed(int)));
    connect(ui->g2, SIGNAL(valueChanged(int)), this, SLOT(color_changed(int)));
    connect(ui->g3, SIGNAL(valueChanged(int)), this, SLOT(color_changed(int)));
    connect(ui->g4, SIGNAL(valueChanged(int)), this, SLOT(color_changed(int)));
    connect(ui->g5, SIGNAL(valueChanged(int)), this, SLOT(color_changed(int)));
    connect(ui->b1, SIGNAL(valueChanged(int)), this, SLOT(color_changed(int)));
    connect(ui->b2, SIGNAL(valueChanged(int)), this, SLOT(color_changed(int)));
    connect(ui->b3, SIGNAL(valueChanged(int)), this, SLOT(color_changed(int)));
    connect(ui->b4, SIGNAL(valueChanged(int)), this, SLOT(color_changed(int)));
    connect(ui->b5, SIGNAL(valueChanged(int)), this, SLOT(color_changed(int)));

    // add secret server button (double click on image in selfie view)
    SecretServer *s = new SecretServer();
    s->installOn(ui->server_label);
    connect(s, SIGNAL(doubleclick()), this, SLOT(go_to_server()));
}

Panel::~Panel()
{
    delete ui;
}

void Panel::color_changed(int value)
{
    QString r1 = QString::number(ui->r1->value());
    QString r2 = QString::number(ui->r2->value());
    QString r3 = QString::number(ui->r3->value());
    QString r4 = QString::number(ui->r4->value());
    QString r5 = QString::number(ui->r5->value());
    QString g1 = QString::number(ui->g1->value());
    QString g2 = QString::number(ui->g2->value());
    QString g3 = QString::number(ui->g3->value());
    QString g4 = QString::number(ui->g4->value());
    QString g5 = QString::number(ui->g5->value());
    QString b1 = QString::number(ui->b1->value());
    QString b2 = QString::number(ui->b2->value());
    QString b3 = QString::number(ui->b3->value());
    QString b4 = QString::number(ui->b4->value());
    QString b5 = QString::number(ui->b5->value());


    QString s1 = QString("{\"color\": [%1, %2, %3, %4, %5, %6, %7, %8, ").arg( \
                r1, r2, r3, r4, r5, g1, g2, g3);
    QString s2 = QString("%9, %10, %11, %12, %13, %14, %15]}").arg( \
                g4, g5, b1, b2, b3, b4, b5);

    QString send = s1 + s2;
    QByteArray msg(send.toUtf8());
    qDebug() << send;

    p->client->write(msg);
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
    ui->r1->setValue(0);
    ui->r2->setValue(256);
    ui->r3->setValue(50);
    ui->r4->setValue(0);
    ui->r5->setValue(256);

    ui->g1->setValue(0);
    ui->g2->setValue(256);
    ui->g3->setValue(50);
    ui->g4->setValue(0);
    ui->g5->setValue(256);

    ui->b1->setValue(0);
    ui->b2->setValue(256);
    ui->b3->setValue(50);
    ui->b4->setValue(0);
    ui->b5->setValue(256);
}
