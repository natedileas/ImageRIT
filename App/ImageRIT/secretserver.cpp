#include "secretserver.h"
#include <QEvent>

bool SecretServer::eventFilter(QObject * obj, QEvent * ev) {
    if (ev->type() == QEvent::MouseButtonDblClick)
      emit doubleclick();
    return false;
}
