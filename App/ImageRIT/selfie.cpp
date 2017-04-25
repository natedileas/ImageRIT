#include "selfie.h"
#include "ui_selfie.h"

selfie::selfie(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::selfie)
{
    ui->setupUi(this);
}

selfie::~selfie()
{
    delete ui;
}
