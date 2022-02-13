from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox, QLineEdit, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMainWindow, QLineEdit
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

        self.setLayout(layout)

        #self.setCentralWidget(container)
        self.setFixedSize(QSize(400, 120))

    def CheckJWT(self):

        activeZoom = Zoom(str(self.edit.text()))

        if str(activeZoom.GetState()) == 'True':
            th = Thread(target=activeZoom.InitUsers())
            th.start()
            self.close()
            users_windows.show()


        else:
            message = QMessageBox()
            message.setWindowTitle('Error')
            message.setText(str(activeZoom.GetState()[0]) + ' ' + str(activeZoom.GetState()[1]))
            #message.setIcon(QMessageBox.Information)
            message.exec()

class UsersWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Zoom Users')

        label = QLabel('Select accounts to administer')

        self.edit = QLineEdit()

        grid_layout = QGridLayout()

        grid_layout.addWidget(label, 0, 0, 1, 1)
        grid_layout.addWidget(self.edit, 0, 1, 1, 1)

        self.setLayout(grid_layout)







app = QApplication([])
start_window = StartWindow()
#View window (Отобразить окно, по умолчанию оно скрыто)
start_window.show()

users_windows = UsersWindow()

#Start (Запускаем цикл событий, когда цикл оборвётся выполнится код который ниже данной команды)
app.exec()