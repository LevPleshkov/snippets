import sys

from PyQt5 import QtCore

# экспорт основных виджетов, необходимых для создания интерфейса
from PyQt5.QtWidgets import (
    QApplication,
    QWidget, QLabel, QPushButton, QVBoxLayout
)

# чтобы убедиться в корректном импорте, можно сравнить версии
# PyQt и Qt. 
print( QtCore.PYQT_VERSION_STR )
print( QtCore.QT_VERSION_STR )

# # объект приложения, запускать который можно из командной строки
# с аргументами, передать который можно через параметр `sys.argv`,
# либо передать пустой список аргументов.
app = QApplication(sys.argv)


# класс - виджет графического интефейса.  виджет содержит два
# элемента - надпись типа `QLabel` и кнопку типа `QPushButton`, 
# при нажатии которой 5 раз, виджет закрывается.  
class Widget(QWidget):
    def __init__(self):
        # 
        super(Widget, self).__init__()
        # настройка параметров окна виджета.
        self.setWindowTitle('Test Window')
        self.resize(300, 100)
        # настройка счетчика нажатий на кнопку.
        self.counter = int(sys.argv[1])
        # настройка графического интерфейса.
        self.init_gui()

    # метод для настройки и инициализации графического интерфейса.
    def init_gui(self):
        # строки, передаваемые объектам PyQt5 могут быть легко
        # форматированы. 
        label = QLabel('<center>Good Evening</center>')
        # с помощью символа амперсанд, можно указать горячю клавишу
        # для комбинации 'ctrl+...'. 
        button = QPushButton('&Quit')

        # Layout помогает разместить дочерние виджеты внутри
        # родительского.  здесь, используем вертикальное размещение
        # для того, чтобы надпись и кнопка находились друг под другом.  
        vbox = QVBoxLayout()
        # после создания, необходимо добавить виджеты в лэйаут.
        vbox.addWidget(label)
        vbox.addWidget(button)
        # и установить дэйаут для виджета с помощью унаследованного
        # от `QWidget` меода. 
        self.setLayout(vbox)

        # соединить встроенный сигнал `clicked` у кнопки со слотом,
        # объявленным как обычная функций (или метод).
        button.clicked.connect(self.quit)

        # выозв отрисовки виджета.
        self.show()

    # метод-слот, который вызыватся при нажатии на кнопку (принимает
    # сигнал), уменьшает значения счетчика нажатий до 0 и закрывает
    # виджет.
    def quit(self):
        print('Quit in ', self.counter)
        self.counter -= 1
        if self.counter == 0:
            sys.exit()


# инициализация виджета.
widget = Widget()
# запуск главного цикла-обработчика событий приложения.
app.exec()
