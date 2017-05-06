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
    //generic slots
    void dial_changed(int value);
    void button_toggled(bool value);

    // custom slots
    void on_selfie_2_clicked();
    void on_email_clicked();
    void go_to_server();
    void affine(int value);
    void hsv(int value);
    void lab(int value);
    void roll(int value);
    void face(bool value);

    void color_changed(int value);
    void on_pushButton_7_clicked();
    void on_pushButton_8_clicked();
    void on_pushButton_15_clicked();
    void on_pushButton_9_clicked();
    void on_pushButton_10_clicked();

    void on_color_reset_clicked();
    void on_filter_reset_clicked();

    void on_affinereset_clicked();

private:
    Ui::Panel *ui;
    MainWindow *p;
};

#endif // PANEL_H
