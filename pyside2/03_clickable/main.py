import sys
import random
from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QVBoxLayout


class MyWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        # Set a list of hellos
        self.hello = ["Hallo Welt", "你好，世界", "Hei maailma", "Hola Mundo", "Привет мир"]

        # Define some widgets
        self.button = QPushButton('Click me!')
        self.text = QLabel('Hola mundo')
        self.text.setAlignment(QtCore.Qt.AlignCenter)

        # Deine layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        # Connect button to event
        self.button.clicked.connect(self.magic)

    def magic(self):
        """Seletcts some random text from the list self.text"""
        self.text.setText(random.choice(self.hello))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    widget = MyWidget()
    widget.show()

    sys.exit(app.exec_())
