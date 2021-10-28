# кроме классов импортируем пространство имен `Qt`, которое содержит
# некоторые необходимые нам перечисления.
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt
import lasio
import typing
import numpy
import pandas


class LasTableModel(QAbstractTableModel):
    """ Класс - модель данных, которая пока умеет только считывать
        текстовый файл с данными и отображать его в таблице с
        возможностью редактирования, но не сохраняет внесенные
        изменения. """

    def __init__(self, path):
        super().__init__()
        # это копия данных из файла, хранящаяся в удобном для нас виде
        # для любых операций по работе с таблицей.
        self.las = lasio.read(path).df()

    # для того, чтобы унаследовать класс `QAbstractTableModel`,
    # необходимо переопределить минимум три метода:
    #  - rowCount, возвращающий количество строк таблицы,
    #  - columnCount, возвращающий количество столбцов,
    #  - data, возвращающий значение ячейки таблицы.
    # эти методы вызываются представлением автоматически для
    # отрисовки содержимого таблицы.

    # параметр `parent` в этих методах является ссылкой на
    # верхний узел таблицы, являющийся 'родителем' для всех
    # ячеек таблицы.

    # параметр `index` имеет среди прочих два метода (`row()` и
    # `column()`), указывающие на ячейку таблицы.

    # параметр `role` указывает на то, какое назначение вызова того
    # или иного метода.

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return self.las.shape[0]

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return self.las.shape[1]

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        # необходимо отображать значение ячейки и в режиме просмотра,
        # и в режиме редактирования.
        if role == Qt.DisplayRole or role == Qt.EditRole:
            value = None
            try:
                value = float(self.las.iloc[index.row(), index.column()])
            except ValueError:
                print(f'ValueError: could not convert \'{value}\' of type \'{type(value)}\' to float.')
                return -9_999
            except IndexError:
                print(f'IndexError: either {index.row()} or {index.column()} is out of range.')
                return -9_999
            else:
                return value

    # этот метод позволяет отображать заголовки столбцов и строк таблицы.
    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.las.columns[section]
            if orientation == Qt.Vertical:
                return float(self.las.index[section])

    # этот метод позволяет изменять значения данных в ячейке.  если
    # разрешено редактирование ячеек, то он вызывается представлением
    # автоматически как только завершается редактирование ячейки.
    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        if role == Qt.EditRole:
            try:
                new_value = float(value)
            except ValueError:
                print(f'ValueError: could not convert \'{value}\' of type \'{type(value)}\' to float.')
                return False
            else:
                self.las.iloc[index.row(), index.column()] = new_value
                return True
        return False

    # метод вызывается представлением, чтобы правильно отобразить ячейки
    # в зависимости от действий пользователя.
    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        # помимо базовых сценариев, возвращаем и возможность редактирвоания.
        return Qt.ItemIsEditable | super().flags(index)

    # метод может быть вызван для того, чтобы вставить `count` ячеек
    # перед строкой `row`.
    def insertRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        # в случае, когда названия срок - не просто индексы, а отметки глубин,
        # можно линейно интерполировать их в зависимости от количества строк.
        indices = numpy.linspace(
            self.las.index[row-1],
            self.las.index[row],
            count+2)
        # новые строки, которые будут добавлены к модели данных `self.las`.
        rows = pandas.DataFrame(
            numpy.zeros((count, self.columnCount())),
            columns=self.las.columns,
            index=indices[1:-1])
        try:
            # перед изменением модели в этом методе необходимо вызвать метод
            # `beginInsertRows`.  в случае с моделью списка или таблицы, такой
            # вызов возможен, в случае работы с моделью древа, нужно передать
            # в нее действительный индекс родительского элемента ячейки.
            self.beginInsertRows(QModelIndex(), row, row+count-1)
            # добавляем строки в модель.
            self.las = pandas.concat([self.las.iloc[:row], rows, self.las.iloc[row:]])
            # после изменения модели, нужно вызвать метод `endInsertRows`.
            # как и `endInsertRows`, он позволяет оповестить представление
            # о том, что модель изменилась.
            self.endInsertRows()
        except IndexError:
            print(f'IndexError: could not insert {count} rows at index {row}.')
            return False
        else:
            return True
