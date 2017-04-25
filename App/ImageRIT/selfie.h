#ifndef SELFIE_H
#define SELFIE_H

#include <QWidget>
#include "mainwindow.h"

namespace Ui {
class selfie;
}

class selfie : public QWidget
{
    Q_OBJECT

public:
    explicit selfie(QWidget *parent = 0);
    ~selfie();

private slots:
    void on_back_clicked();

    void on_selfie_b_clicked();

private:
    Ui::selfie *ui;
    MainWindow *p;
};

#endif // SELFIE_H
