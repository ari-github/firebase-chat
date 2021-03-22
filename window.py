import threading

from PyQt5.QtWidgets import QWidget, QHBoxLayout

from PyQt5.QtGui import QFont
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from users_window import UsersWindow
from chat_window import ChatWindow
from firebase import auth, db
import sys
import qdarkstyle


class Window(QWidget):

    def __init__(self, username):
        super().__init__()
        self.users_dic = dict()
        self.messages = dict()

        self.username = username
        self.uid = auth.current_user['localId']

        self.win_id = None

        self.init_ui()
        self.users_streamer = db.child("users").stream(self.users_listener)
        self.message_streamer = db.child("user_messages").child(self.uid).stream(self.message_listener)

    def message_listener(self, data):
        try:
            sender = data['data']['sender']
            message = data['data']['message']
            self.messages[sender].append(f'{self.users_dic[sender]["username"]}: {message}')
            if self.win_id == sender:
                self.chat_win.add_message(f'{self.users_dic[sender]["username"]}: {message}')
            else:
                self.user_win.move_to_top(sender, bold=True)
        except:
            print(sys.exc_info())

    def users_listener(self, users_data):
        try:
            if users_data['path'] == '/':
                self.users_dic.update(users_data['data'])
                for key in self.users_dic:
                    self.user_win.add_user(self.users_dic[key]["username"], key)
                    self.messages[key] = list()

            else:
                self.users_dic[users_data['data']['id']] = users_data['data']

                self.user_win.add_user(users_data['data']["username"], users_data['data']['id'])
                self.messages[users_data['data']['id']] = list()

            print(f'user list update: {self.users_dic}')
            self.user_win.remove_user(self.uid)
            self.users_dic.pop(self.uid)
        except:
            print(sys.exc_info())

    def lunch_messages(self, user_id):
        self.chat_win.text_box.show()
        self.chat_win.button.show()
        self.chat_win.chat_text.clear()

        for mes in self.messages[user_id]:
            self.chat_win.add_message(mes)

    def user_clicked(self, item):
        key = item.data(Qt.UserRole)
        font = QFont()
        font.setBold(False)
        item.setFont(font)

        if key != self.win_id:
            self.win_id = key
            self.lunch_messages(key)

    def send_clicked(self):
        text = self.chat_win.text_box.text()
        self.chat_win.text_box.setText('')

        if text == '':
            return

        self.messages[self.win_id].append(text)
        self.chat_win.add_message(text)

        self.user_win.move_to_top(self.win_id, bold=False)
        self.user_win.list_widget.item(0).setSelected(True)

        threading.Thread(target=self.send_message, args=(text,)).start()

    def send_message(self, text):
        # data = dict()
        # for key in list(self.users_dic):
        #     data[f'{key}/{db.generate_key()}'] = {'sender': self.uid, 'message': text}
        db.child('user_messages').child(self.win_id).push({'sender': self.uid, 'message': text})

    def init_ui(self):
        self.user_win = UsersWindow()
        self.user_win.list_widget.itemClicked.connect(self.user_clicked)

        self.chat_win = ChatWindow()
        self.chat_win.button.clicked.connect(self.send_clicked)

        self.chat_win.text_box.hide()
        self.chat_win.button.hide()

        hb = QHBoxLayout()

        hb.addWidget(self.user_win, 2)
        hb.addWidget(self.chat_win, 3)

        self.setLayout(hb)
        self.resize(800, 600)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.setWindowTitle(f'Welcome to the chat {self.username}')

    def keyPressEvent(self, event):
        if event.key() == 16777220 and self.focusWidget() == self.chat_win.text_box:
            self.send_clicked()

    def closeEvent(self, event):
        self.users_streamer.close()
        self.message_streamer.close()

