#ifndef SECRETSERVER_H
#define SECRETSERVER_H

#include <QObject>
#include <QWidget>

class SecretServer : public QObject
{
    Q_OBJECT
public:
    bool eventFilter(QObject * obj, QEvent * ev);

    void installOn(QWidget * widget) {
        widget->installEventFilter(this);
    }
signals:
    void doubleclick();

public slots:
};

#endif // SECRETSERVER_H
