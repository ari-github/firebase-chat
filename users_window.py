
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem

from PyQt5.QtGui import QFont
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QSize

import sys


class UsersWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.users_dic = dict()

    def init_ui(self):
        self.main_layout = QVBoxLayout()
        self.list_widget = QListWidget()

        self.main_layout.addWidget(self.list_widget)
        self.setLayout(self.main_layout)
        self.resize(400, 500)

    def add_user(self, username, uid):
        list_item = QListWidgetItem(username)
        list_item.setSizeHint(QSize(1, 50))
        list_item.setData(Qt.UserRole, uid)

        self.list_widget.addItem(list_item)

    def remove_user(self, uid):
        for i in range(self.list_widget.count()):
            if uid == self.list_widget.item(i).data(Qt.UserRole):
                self.list_widget.takeItem(i)
                break

    def move_to_top(self, uid, bold):
        for i in range(self.list_widget.count()):
            if uid == self.list_widget.item(i).data(Qt.UserRole):
                item = self.list_widget.takeItem(i)
                if bold:
                    font = QFont()
                    font.setBold(True)
                    item.setFont(font)

                self.list_widget.insertItem(0, item)
                break


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = UsersWindow()
    main.show()

    sys.exit(app.exec())
