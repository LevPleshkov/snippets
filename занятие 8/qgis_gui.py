import os
from datetime import datetime
import webbrowser


# определяем путь к файлу с иконкой для создания нового элемента
# на панели инструментов.
icon = 'clock.png'
data_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
icon_path = os.path.join(data_dir, icon)


# функция-слот, которая будет вызываться при срабатывании сигнала
# от нажатия на созданную иконку.
def show_time():
    now = datetime.now()
    current_time = now.strftime('%H:%M:%S')
    iface.messageBar().pushInfo('Current Time', current_time)

    
# создаем QAction - действие, которое может быть вызвано пользователем
# при выборе элемента в меню, на панели инструментов или горячими
# клавишами.  эти способы могут существовать одновременно и каждый
# из них будет вызывать одно и тот же отклик программы.
# одна и та же сущность QAction может быть добавлена и в меню,
# и на панель инструментов.
action = QAction()
# соединяем сгнал со слотом.
action.triggered.connect(show_time)
# устанавливаем иконку.
action.setIcon(QIcon(icon_path))
# добавляем на панель инструментов.
iface.addToolBarIcon(action)



# функция-слот для другого действия - открытия браузера по умолчанию
# на компьютере с запущенным приложением QGIS.
def open_webpage():
    webbrowser.open('https://github.com/LevPleshkov/snippets')


# создаем QAction с названием.
webpage_action = QAction('Open github snippets')
# соединяем сигнал и слот.
webpage_action.triggered.connect(open_webpage)
# в этот раз добавляем действие в меню 'Help', хотя можно этот же
# `webpage_action` добавить и на панель инструментов.
iface.helpMenu().addSeparator()
iface.helpMenu().addAction(webpage_action)
