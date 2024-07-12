import sys
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QDialog, QApplication, QVBoxLayout, QLabel, QPushButton, QLineEdit
from PyQt5.QtCore import Qt

class Edit(QLineEdit):
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            return
        super().keyPressEvent(event)


class Dial(QDialog):
    log = None
    has = None
    def __init__(self):
        super().__init__()
        
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 100)

        label = QLabel("Zaloguj się", self)
        label.setAlignment(Qt.AlignCenter)

        self.login = Edit(self)
        self.login.setPlaceholderText("Login")
        self.login.textChanged.connect(self.loginChanged)

        self.haslo = Edit(self)
        self.haslo.setPlaceholderText("Hasło")
        self.haslo.textChanged.connect(self.hasloChanged)

        potwierdz = QPushButton("Potwierdź", self)
        potwierdz.clicked.connect(self.potwierdz)

        layout = QVBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(self.login)
        layout.addWidget(self.haslo)
        layout.addWidget(potwierdz)

        self.setWindowTitle('Dialog')
        self.show()
    
    def loginChanged(self):
        self.log = self.login.text()

    def hasloChanged(self):
        self.has = self.haslo.text()

    def potwierdz(self):
        self.close()
