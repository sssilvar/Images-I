#!/bin/env python3
import sys
from os.path import join, dirname, realpath

import PySide2.QtXml
from PySide2.QtCore import QFile
from PySide2.QtGui import QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QStyleFactory

cd = dirname(realpath(__file__))


def say_hello():
    print('Hi {name}!'.format(name=window.nameLineEdit.text()))
    # Increase progress bar by 10
    val = window.progressBar.value()
    window.progressBar.setValue(val + 10)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # style = QStyleFactory()
    # app.setStyle(style.create('windows'))

    # Load ui file
    mw_file = QFile(join(cd, 'ui', 'main_window.ui'))
    loader = QUiLoader()

    # Load and show
    window = loader.load(mw_file)
    window.setWindowIcon(QIcon(join(cd, 'ui', 'resources', 'icon.png')))
    window.show()

    # Connect greet button to action
    window.greetButton.clicked.connect(say_hello)
    window.actionExit.triggered.connect(app.exit)

    # Exec app
    sys.exit(app.exec_())
