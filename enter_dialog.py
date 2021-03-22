from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLineEdit, QDialogButtonBox, QFormLayout, QDialog, QMessageBox, QLabel, QPushButton
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
import qdarkstyle
import sys

from firebase import db, auth
from window import Window


class ClickLabel(QLabel):
    clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()


class RegisterDialog(QDialog):

    confirm = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(RegisterDialog, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(self.windowFlags()^ Qt.WindowContextHelpButtonHint)

        font = QFont()
        font.setPointSize(9)

        self.username = QLineEdit(self)
        self.email = QLineEdit(self)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)

        self.lable = ClickLabel('<font>Already have an account</font><font color="blue"> Login</font>')

        register_layout = QFormLayout()
        register_layout.addRow("Username", self.username)
        register_layout.addRow("Email", self.email)
        register_layout.addRow("Password", self.password)
        register_layout.addWidget(self.lable)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.control)
        self.buttons.rejected.connect(self.reject)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(register_layout)
        layout.addWidget(self.buttons)
        self.setLayout(layout)

        self.setWindowTitle('Register Box')
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

        self.setGeometry(600, 100, 400, 200)
        self.setSizeGripEnabled(False)
        # self.setFixedSize(self.sizeHint())

    def control(self):
        username = self.username.text()
        email = self.email.text()
        password = self.password.text()

        if username.strip() == '' or email.strip() == '' or password.strip() == '':
            QMessageBox.warning(self, 'Error', "Pleas fill all the fields")
            return
        elif len(password.strip()) < 6:
            QMessageBox.warning(self, 'Error', "Password must tbe at least 6 characters")
            return

        try:
            auth.create_user_with_email_and_password(email, password)
        except:
            QMessageBox.warning(self, 'Error', "You already have an account")
            print(sys.exc_info())
            return

        auth.sign_in_with_email_and_password(email, password)
        uid = auth.current_user['localId']
        user_data = {'username': username,
                     'email': email,
                     'password': password,
                     'id': uid}

        db.child('users').child(uid).set(user_data)
        self.confirm.emit(username)
        self.close()


class LoginDialog(QDialog):

    confirm = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)

        font = QFont()
        font.setPointSize(9)

        self.email = QLineEdit(self)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)

        self.lable = ClickLabel('<font>Don\'t have an account</font><font color="blue"> Register now</font>')

        login_layout = QFormLayout()
        login_layout.addRow("Email", self.email)
        login_layout.addRow("Password", self.password)
        login_layout.addWidget(self.lable)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.control)
        self.buttons.rejected.connect(self.reject)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(login_layout)
        layout.addWidget(self.buttons)
        self.setLayout(layout)

        self.setWindowTitle('Login Box')
        self.setWindowIcon(QtGui.QIcon('dc1.png'))
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

        self.setGeometry(600, 100, 400, 200)
        self.setSizeGripEnabled(False)
        # self.setFixedSize(self.sizeHint())

    def control(self):
        email = self.email.text()
        password = self.password.text()

        try:
            auth.sign_in_with_email_and_password(email, password)
        except:
            QMessageBox.warning(self, 'Error', "Wrong username or password! \n\n")
            print(sys.exc_info())
            return

        uid = auth.current_user['localId']
        username = db.child('users').child(uid).child('username').get().val()
        self.confirm.emit(username)
        self.close()


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    login = LoginDialog()
    register = RegisterDialog()


    def show_log():
        register.close()
        login.show()


    def show_reg():
        login.close()
        register.show()


    def log_confirm(username):
        print('Logging in ...')
        main = Window(username)
        main.show()

    def reg_confirm(username):
        print('Register succeeded!')
        main = Window(username)
        main.show()

    login.confirm.connect(log_confirm)
    register.confirm.connect(reg_confirm)

    login.lable.clicked.connect(show_reg)
    register.lable.clicked.connect(show_log)

    login.show()

    sys.exit(app.exec())
