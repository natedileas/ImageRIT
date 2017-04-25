#ifndef CONFIG_H
#define CONFIG_H

#include <QWidget>
#include "mainwindow.h"


namespace Ui {
class Config;
}

class Config : public QWidget
{
    Q_OBJECT

public:
    explicit Config(QWidget *parent = 0);
    ~Config();

private slots:
    void on_reconnect_clicked();

    void on_back_clicked();

private:
    Ui::Config *ui;
    MainWindow *p;

};

#endif // CONFIG_H
