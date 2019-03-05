#!/usr/bin/python3
import sys
from PySide2.QtWidgets import QLineEdit, QPushButton, QApplication, QVBoxLayout, QDialog


class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        # Create Widgets
        self.edit = QLineEdit('Write your name here')
        self.button = QPushButton()
        # TODO: Finish
