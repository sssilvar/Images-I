import sys
from PySide2.QtWidgets import QApplication, QMessageBox

if __name__ == '__main__':
    # Create the application object
    app = QApplication(sys.argv)

    # Create a simple dialog box
    msg_box = QMessageBox()
    msg_box.setText("Hello World!")
    msg_box.show()
    sys.exit(msg_box.exec_())
