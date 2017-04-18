#ifndef PANEL_H
#define PANEL_H

#include <QWidget>
#include "client.h"

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

private:
    Ui::Panel *ui;
};

#endif // PANEL_H
