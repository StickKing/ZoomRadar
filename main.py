from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QLabel, QPushButton, QMainWindow, QLineEdit



#Create application window (Создаю объект окна)
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Zoom-Auth')

        label = QLabel('Enter the JWT Token')

        button = QPushButton('Start')

        edit = QLineEdit()

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(edit)
        layout.addWidget(button)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)


app = QApplication([])
window = MainWindow()
#View window (Отобразить окно, по умолчанию оно скрыто)
window.show()

#Start (Запускаем цикл событий, когда цикл оборвётся выполнится код который ниже данной команды)
app.exec()