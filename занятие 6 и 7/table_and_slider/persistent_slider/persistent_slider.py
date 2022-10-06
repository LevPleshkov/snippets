import sys

# экспорт основных виджетов, необходимых для создания интерфейса
from PyQt5.QtWidgets import QApplication, QWidget

# экспорт файла с виджетом, подготовленным в Qt Designer
from .form import Ui_Widget

# модуль для чтения и записи бинарных данных
import pickle


# класс, который обеспечивает взаимосвязь свого графического
# интерфейса и пользовательских данных.  в этом случае, данные -
# это значение ползунка слайдера и привязанное к нему значение
# цифрового табло.  класс Ui_Widget сгенерирован автоматически
# из файла 'form.ui' (см. 'readme.txt'). 
class PersistentSlider(QWidget, Ui_Widget):
    def __init__(self):
        # вызов к инициализатору родительског класса:
        super().__init__()
        # путь к файлу с пользовательскими данными.
        self.file_name = 'persistent_slider/lcd_value.txt'
        # загрузка пользовательских данных.
        self.value = self.load_data()
        # настройка графического интерфейса.
        self.setup_gui()

    # метод для настройки и инициализации графического интерфейса.
    def setup_gui(self):
        # вызов метода, унаследованного от Ui_Widget.
        self.setupUi(self)
        # передача пользователских данных виджетам.
        self.lcdNumber.display(self.value)
        self.horizontalSlider.setValue(self.value)
        # соединение сигналов от виджета с кнопками 'Отмена' и 'ОК'
        # со слотами.  сигналы `accepted` и `rejected` являются
        # для этого виджета стандартными.  
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.rejected.connect(self.rejected)
        # выозв отрисовки виджета.
        self.show()

    # метод, выполняющий чтение сохраненных ранее данных из файла. 
    def load_data(self):
        # конструкция 'try-except' позволяет перехватывать исключения
        # (ошибки) от используемых кмпонентов - встроенных или 
        # сторонних модулей.
        try:
            file = open(self.file_name, 'rb')
            value = pickle.load(file)
            file.close()
        # в этом случае, метод `pickle.load()`
        # может вызват исключение `FileNotFoundError`, и тогда можно
        # попытваться его перехватить (блок `except`) и обработать,
        # т. е. изменить ход выполнения программы подходящим образом. 
        except FileNotFoundError:
            return 0
        # блок `else` выполняется, если исключений не возникло.
        else:
            return value
        # блок `finally` не обязательный и выполняется в любом случае.
        # finally:
        #     return -1

    # слот для принятия сигнала от виджета для случая нажатия 
    # кнопки 'ОК'.
    def accepted(self):
        # в таком случае - сохраняем текущее значение слайдера в файл.
        file = open(self.file_name, 'wb')
        pickle.dump(self.horizontalSlider.value(), file)
        file.close()
        self.close()

    # слот для принятия сигнала от виджета для случая нажатия 
    # кнопки 'Отмена'.
    def rejected(self):
        self.close()


if __name__ == '__main__':
    # объект приложения, запускать который можно из командной строки
    # с аргументами, передать который можно через параметр `sys.argv`. 
    app = QApplication(sys.argv)
    # инициализация виджета.
    widget = PersistentSlider()
    # запуск главного цикла-обработчика событий приложения.
    app.exec()
