import sys
from PySide2.QtWidgets import QApplication, QMainWindow

from ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


if __name__ == '__main__':
    app = QApplication()

    # Add window
    window = MainWindow()
    window.show()

    # Execute the app
    sys.exit(app.exec_())
