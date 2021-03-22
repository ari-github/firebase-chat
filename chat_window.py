from PyQt5.QtWidgets import QWidget, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QDialog, QApplication
from PyQt5.QtGui import QFont
from PyQt5 import QtWidgets

import sys


class ChatWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def add_message(self, message):
        self.chat_text.append(message)
        print(message)

    def init_ui(self):
        font = QFont()
        font.setPointSize(9)

        self.chat_text = QTextEdit()
        self.chat_text.setReadOnly(True)

        self.chat_text.setFont(font)

        self.text_box = QLineEdit()
        self.text_box.setFont(font)

        self.button = QPushButton()
        self.button.setText('send!')
        self.button.setFont(font)
        # self.button.clicked.connect(self.send_click)

        self.main_vb = QVBoxLayout()

        self.main_vb.addWidget(self.chat_text)
        self.main_vb.addWidget(self.text_box)
        self.main_vb.addWidget(self.button)

        self.setLayout(self.main_vb)
        self.resize(400, 500)
        self.setWindowTitle('Chat')
        self.text_box.setFocus()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = ChatWindow()
    main.show()
    sys.exit(app.exec())