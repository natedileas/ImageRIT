#include "mainwindow.h"
#include "ui_mainwindow.h"

#include "client.h"
#include "panel.h"
#include "config.h"
#include "selfie.h"
#include "email.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    this->show();

    pages = new QStackedWidget;

    Config *c = new Config(this);
    pages->addWidget(c);
    pages->setCurrentIndex(0);

    Panel *b = new Panel(this);
    pages->addWidget(b);

    selfie *s = new selfie(this);
    pages->addWidget(s);

    Email *e = new Email(this);
    pages->addWidget(e);
    this->setCentralWidget(pages);

    client = new Client;
}

MainWindow::~MainWindow()
{
    delete ui;
}
