#ifndef PANEL_H
#define PANEL_H

#include <QWidget>
#include "mainwindow.h"

namespace Ui {
class Panel;
}

class Panel : public QWidget
{
    Q_OBJECT

public:
    explicit Panel(QWidget *parent = 0);
    ~Panel();

    Client client;

private slots:
    void dial_changed(int value);
    void button_toggled(bool value);

    void on_server_clicked();

private:
    Ui::Panel *ui;
    MainWindow *p;
};

#endif // PANEL_H
