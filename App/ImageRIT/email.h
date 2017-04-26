#ifndef EMAIL_H
#define EMAIL_H

#include <QWidget>
#include "mainwindow.h"

namespace Ui {
class Email;
}

class Email : public QWidget
{
    Q_OBJECT

public:
    explicit Email(QWidget *parent = 0);
    ~Email();

private slots:
    void on_emailme_clicked();

private:
    Ui::Email *ui;
    MainWindow *p;
};

#endif // EMAIL_H
