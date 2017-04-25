#ifndef SELFIE_H
#define SELFIE_H

#include <QWidget>

namespace Ui {
class selfie;
}

class selfie : public QWidget
{
    Q_OBJECT

public:
    explicit selfie(QWidget *parent = 0);
    ~selfie();

private:
    Ui::selfie *ui;
};

#endif // SELFIE_H
