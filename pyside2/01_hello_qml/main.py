import sys

from PySide2.QtWidgets import QApplication
from PySide2.QtQuick import QQuickView
from PySide2.QtCore import QUrl

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = QQuickView()
    url = QUrl('view.qml')

    view.setSource(url)
    view.show()
    sys.exit(app.exec_())
