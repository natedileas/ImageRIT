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

    connect(ui->invert, SIGNAL(toggled(bool)), this, SLOT(button_toggled(bool)));
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

    //hsv
    connect(ui->h, SIGNAL(valueChanged(int)), this, SLOT(hsv(int)));
    connect(ui->s, SIGNAL(valueChanged(int)), this, SLOT(hsv(int)));
    connect(ui->v, SIGNAL(valueChanged(int)), this, SLOT(hsv(int)));
    //lab
    connect(ui->l, SIGNAL(valueChanged(int)), this, SLOT(lab(int)));
    connect(ui->a, SIGNAL(valueChanged(int)), this, SLOT(lab(int)));
    connect(ui->b, SIGNAL(valueChanged(int)), this, SLOT(lab(int)));
    //roll
    connect(ui->roll_r, SIGNAL(valueChanged(int)), this, SLOT(roll(int)));
    connect(ui->roll_b, SIGNAL(valueChanged(int)), this, SLOT(roll(int)));
    connect(ui->roll_g, SIGNAL(valueChanged(int)), this, SLOT(roll(int)));

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

void Panel::hsv(int value)
{
    QString r1 = QString::number(ui->h->value());
    QString r2 = QString::number(ui->s->value());
    QString r3 = QString::number(ui->v->value());

    QString send = QString("{\"hsv\": [%1, %2, %3]}").arg(r1, r2, r3);

    QByteArray msg(send.toUtf8());
    qDebug() << send;

    p->client->write(msg);
}

void Panel::lab(int value)
{
    QString r1 = QString::number(ui->l->value());
    QString r2 = QString::number(ui->a->value());
    QString r3 = QString::number(ui->b->value());

    QString send = QString("{\"lab\": [%1, %2, %3]}").arg(r1, r2, r3);

    QByteArray msg(send.toUtf8());
    qDebug() << send;

    p->client->write(msg);
}

void Panel::roll(int value)
{
    QString r1 = QString::number(ui->roll_r->value());
    QString r2 = QString::number(ui->roll_g->value());
    QString r3 = QString::number(ui->roll_b->value());

    QString send = QString("{\"roll\": [%1, %2, %3]}").arg(r1, r2, r3);

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

    ui->h->setValue(100);
    ui->s->setValue(100);
    ui->v->setValue(100);
    ui->l->setValue(100);
    ui->a->setValue(100);
    ui->b->setValue(100);
}

void Panel::on_pushButton_7_clicked()
{
    ui->r1->setValue(0);
    ui->r2->setValue(88);
    ui->r3->setValue(100);
    ui->r4->setValue(0);
    ui->r5->setValue(256);

    ui->g1->setValue(0);
    ui->g2->setValue(123);
    ui->g3->setValue(74);
    ui->g4->setValue(0);
    ui->g5->setValue(256);

    ui->b1->setValue(0);
    ui->b2->setValue(57);
    ui->b3->setValue(94);
    ui->b4->setValue(0);
    ui->b5->setValue(256);
}

void Panel::on_pushButton_8_clicked()
{
    ui->r1->setValue(0);
    ui->r2->setValue(256);
    ui->r3->setValue(39);
    ui->r4->setValue(66);
    ui->r5->setValue(199);

    ui->g1->setValue(0);
    ui->g2->setValue(256);
    ui->g3->setValue(79);
    ui->g4->setValue(47);
    ui->g5->setValue(240);

    ui->b1->setValue(85);
    ui->b2->setValue(256);
    ui->b3->setValue(100);
    ui->b4->setValue(88);
    ui->b5->setValue(193);
}

void Panel::on_pushButton_15_clicked()
{
    //[10, 256, 21, 66, 199, 118, 136, 79, 47, 240, 39, 73, 100, 45, 131]
    ui->r1->setValue(10);
    ui->r2->setValue(256);
    ui->r3->setValue(21);
    ui->r4->setValue(66);
    ui->r5->setValue(199);

    ui->g1->setValue(118);
    ui->g2->setValue(136);
    ui->g3->setValue(79);
    ui->g4->setValue(47);
    ui->g5->setValue(240);

    ui->b1->setValue(39);
    ui->b2->setValue(73);
    ui->b3->setValue(100);
    ui->b4->setValue(45);
    ui->b5->setValue(131);
}

void Panel::on_pushButton_9_clicked()
{
    //[0, 256, 50, 0, 256, 27, 111, 25, 202, 137, 0, 99, 19, 53, 164]
    ui->r1->setValue(0);
    ui->r2->setValue(256);
    ui->r3->setValue(50);
    ui->r4->setValue(0);
    ui->r5->setValue(256);

    ui->g1->setValue(27);
    ui->g2->setValue(111);
    ui->g3->setValue(25);
    ui->g4->setValue(202);
    ui->g5->setValue(137);

    ui->b1->setValue(0);
    ui->b2->setValue(99);
    ui->b3->setValue(19);
    ui->b4->setValue(53);
    ui->b5->setValue(164);
}

void Panel::on_pushButton_10_clicked()
{
    ui->invert->toggle();
    on_pushButton_9_clicked();
}

void Panel::on_quantize_s_valueChanged(int value)
{
    if (ui->quantize_b->isChecked()){
        QString send = QString("{\"quantize\": [%1]}").arg(QString::number(value));
        QByteArray msg(send.toUtf8());
        qDebug() << send;

        p->client->write(msg);
    }
}
