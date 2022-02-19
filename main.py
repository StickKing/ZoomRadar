from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox, QColumnView, QTableWidgetItem, QCheckBox, QLineEdit, QGridLayout, QTableWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMainWindow, QLineEdit
from object import *
from threading import Thread
import multiprocessing

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

        grid_layout = QVBoxLayout()
        grid_layout.addWidget(label)

        height = 20

        for user in activeZoom.ZoomUsers:
            self.item[user.id] = QCheckBox(user.name)
            grid_layout.addWidget(self.item[user.id])
            height += 25

        self.button = QPushButton('Select users')
        self.button.setFixedHeight(45)
        self.button.clicked.connect(self.ViewMainWindow)

        grid_layout.addWidget(self.button)

        self.setLayout(grid_layout)

        self.setFixedSize(QSize(400, height))

    def ViewMainWindow(self):

        delList = []
        items = 0

        for user in self.activeZoom.ZoomUsers:
            if self.item[user.id].isChecked() == False:
                delList.append(user)
            else:
                items += 1

        for user in delList:
            self.activeZoom.ZoomUsers.remove(user)

        if items == 0:
            message = QMessageBox()
            message.setWindowTitle('Warning')
            message.setText('No element is selected!')
            message.exec()
        else:
            self.main_window = MainWindow(self.activeZoom)
            self.main_window.show()
            self.close()


class MainWindow(QWidget):
    def __init__(self, activeZoom):
        super().__init__()

        self.activeZoom = activeZoom
        self.userInfo = {}

        self.gridLayout = QGridLayout()

        for user in self.activeZoom.ZoomUsers:
            th = Thread(target=user.GetAllConference())
            th.start()

        vertical = 0
        horizontal = 0
        for user in self.activeZoom.ZoomUsers:
            self.userInfo[user.id] = [QLabel(user.name), QTableWidget()]

            rowCount = 1
            self.userInfo[user.id][1].setRowCount(rowCount)

            self.userInfo[user.id][1].setColumnCount(4)

            self.userInfo[user.id][1].setHorizontalHeaderLabels(['Topic', 'Date', 'Start Time', 'End Time'])

            if user.getResult != 'None':
                hor = 0
                ver = 0
                for meet in user.getResult:
                    self.userInfo[user.id][1].setItem(ver, hor, QTableWidgetItem(meet['topic']))

                    hor += 1
                    self.userInfo[user.id][1].setItem(ver, hor, QTableWidgetItem(meet['start_time'].split('T')[0]))

                    start_hour = int(meet['start_time'].split('T')[1].split(':')[0]) + 3
                    start_minet = meet['start_time'].split(':')[1]
                    # Час окончания конференции
                    end_hour = str(start_hour + meet['duration'] // 60)
                    # Минута окончания конференции
                    end_minet = str(meet['duration'] % 60 + int(start_minet))
                    if end_minet == '0':
                        end_minet = end_minet + '0'

                    hor += 1
                    self.userInfo[user.id][1].setItem(ver, hor, QTableWidgetItem(str(start_hour) + ':' + meet['start_time'].split(':')[1] ))

                    hor += 1
                    self.userInfo[user.id][1].setItem(ver, hor, QTableWidgetItem(end_hour + ':' + end_minet))

                    ver += 1
                    hor = 0
                    rowCount += 1

                    self.userInfo[user.id][1].setRowCount(rowCount)
                self.userInfo[user.id][1].resizeColumnsToContents()


            self.gridLayout.addWidget(self.userInfo[user.id][0], vertical, horizontal)
            vertical += 1
            self.gridLayout.addWidget(self.userInfo[user.id][1], vertical, horizontal)

            if horizontal == 2:
                horizontal = 0
                vertical += 1
            else:
                horizontal += 1
                vertical -= 1

        self.setLayout(self.gridLayout)







app = QApplication([])

start_window = StartWindow()
#View window (Отобразить окно, по умолчанию оно скрыто)
start_window.show()





#Start (Запускаем цикл событий, когда цикл оборвётся выполнится код который ниже данной команды)
app.exec()