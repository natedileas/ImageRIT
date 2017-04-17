#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "client.h"

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

    Client client;

private slots:
    void on_dial_changed(int value);

private:
    Ui::MainWindow *ui;
};

#endif // MAINWINDOW_H
