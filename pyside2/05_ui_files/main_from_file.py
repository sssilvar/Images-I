#!/bin/env python3
import sys
from os.path import join, dirname, realpath

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QMainWindow, QApplication
from PySide2.QtCore import QFile

root = dirname(realpath(__file__))


def say_hello():
    print('Hello! Button pressed')


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Load mainwindow.ui directly
    ui_file = QFile(join(root, 'mainwindow.ui'))
    ui_file.open(QFile.ReadOnly)

    loader = QUiLoader()
    window = loader.load(ui_file)

    ui_file.close()
    window.show()

    # Connect button to function
    window.pushButton.clicked.connect(say_hello)

    sys.exit(app.exec_())
