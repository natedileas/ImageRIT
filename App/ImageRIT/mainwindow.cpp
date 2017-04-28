#include "mainwindow.h"
#include "ui_mainwindow.h"

#include "client.h"
#include "panel.h"
#include "config.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    this->show();

    Config *c = new Config(this);
    ui->pages->addWidget(c);
    ui->pages->setCurrentIndex(1);

    Panel *b = new Panel(this);
    ui->pages->addWidget(b);

    client = new Client;
    pages = ui->pages;
}

MainWindow::~MainWindow()
{
    delete ui;
}
