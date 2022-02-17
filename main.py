from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox, QColumnView, QCheckBox, QLineEdit, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMainWindow, QLineEdit
from object import *
from threading import Thread

#Create application window (Создаю объект окна)
class StartWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Zoom-Auth')

        label = QLabel('Enter the JWT Token')

        #Create button
        button = QPushButton('Start')
        #Change button size
        button.setFixedSize(QSize(360, 45))
        #Enabled checkable
        button.setCheckable(True)
        #Function after click
        button.clicked.connect(self.CheckJWT)

        self.edit = QLineEdit()

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.edit)
        layout.addWidget(button)

        self.users_window = None

        self.setLayout(layout)

        #self.setCentralWidget(container)
        self.setFixedSize(QSize(400, 120))

    def CheckJWT(self):

        activeZoom = Zoom(str(self.edit.text()))

        if str(activeZoom.GetState()) == 'True':
            th = Thread(target=activeZoom.InitUsers())
            th.start()
            self.users_window = UsersWindow(activeZoom)
            self.users_window.show()
            self.close()
        else:
            message = QMessageBox()
            message.setWindowTitle('Error')
            message.setText(str(activeZoom.GetState()[0]) + ' ' + str(activeZoom.GetState()[1]))
            message.exec()

class UsersWindow(QWidget):

    def __init__(self, activeZoom):
        super().__init__()

        self.main_window = None

        self.activeZoom = activeZoom

        self.setWindowTitle('Zoom Users')

        self.item = {}

        label = QLabel('Select accounts to administer')

        grid_layout = QGridLayout()
        grid_layout.addWidget(label, 0, 0)

        i = 1

        for user in activeZoom.ZoomUsers:
            self.item[user.id] = QCheckBox(user.name)
            grid_layout.addWidget(self.item[user.id], i, 0)
            i += 1

        self.button = QPushButton('Select users')
        self.button.setFixedHeight(45)
        self.button.clicked.connect(self.ViewMainWindow)

        grid_layout.addWidget(self.button)

        self.setLayout(grid_layout)

    def ViewMainWindow(self):

        j = ''

        for user in self.activeZoom.ZoomUsers:
            #j += str(self.item[user.id].text() + ' - ')
            if self.item[user.id].isChecked() == True:
                j += str(self.item[user.id].text() + ' - ')
            else:
                self.activeZoom.ZoomUsers.remove(user)

        message = QMessageBox()
        message.setWindowTitle('Error')
        message.setText(str(j))
        message.exec()

        self.main_window = MainWindow(self.activeZoom)
        self.main_window.show()

        self.close()


class MainWindow(QWidget):
    def __init__(self, activeZoom):
        super().__init__()

        self.activeZoom = activeZoom
        self.userInfo = {}

        self.gridLayout = QGridLayout()

        i = 0
        for user in self.activeZoom.ZoomUsers:
            self.userInfo[user.id] = [QLabel(user.name), QColumnView()]
            self.gridLayout.addWidget(self.userInfo[user.id][0], i, 0)
            i += 1
            self.gridLayout.addWidget(self.userInfo[user.id][1], i, 0)
            i += 1

        self.setLayout(self.gridLayout)
        #self.setCentralWidget(self.gridLayout)







app = QApplication([])

start_window = StartWindow()
#View window (Отобразить окно, по умолчанию оно скрыто)
start_window.show()





#Start (Запускаем цикл событий, когда цикл оборвётся выполнится код который ниже данной команды)
app.exec()