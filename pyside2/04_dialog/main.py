#!/usr/bin/python3
import sys
from PySide2.QtWidgets import QLineEdit, QPushButton, QApplication, QVBoxLayout, QDialog


class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        # Create Widgets
        self.edit = QLineEdit('Write your name here')
        self.button = QPushButton('Greet me!')
        # Create a layout and add the buttons
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.edit)
        self.layout.addWidget(self.button)
        # Set dialog layout
        self.setLayout(self.layout)
        # Add button signal and connect it to greet
        self.button.clicked.connect(self.greet)

    def greet(self):
        print('Hello {name}!'.format(name=self.edit.text()))


if __name__ == '__main__':
    # Creat an app
    app = QApplication(sys.argv)

    # Add widget
    widget = Form()
    widget.show()

    # Exec app
    sys.exit(app.exec_())
