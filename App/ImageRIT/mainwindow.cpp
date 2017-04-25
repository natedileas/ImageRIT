#include "mainwindow.h"
#include "ui_mainwindow.h"

#include "client.h"
#include "panel.h"
#include "config.h"
#include "selfie.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    pages = new QStackedWidget;
    this->setCentralWidget(pages);

    Config *c = new Config(this);
    pages->addWidget(c);

    Panel *b = new Panel(this);
    pages->addWidget(b);

    selfie *s = new selfie(this);
    pages->addWidget(s);

    pages->setCurrentIndex(1);

    client = new Client;
}

MainWindow::~MainWindow()
{
    delete ui;
}
