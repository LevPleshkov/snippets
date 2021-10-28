from PyQt5.QtWidgets import QApplication, QTableView
from persistent_slider import PersistentSlider
from table_model_view import LasTableModel


def persistent_slider():
    return PersistentSlider()


def las_table():
    model = LasTableModel('table_model_view/example.las')
    model.insertRows(5, 4)
    table = QTableView()
    table.setModel(model)
    table.resize(600, 600)
    return table


if __name__ == '__main__':
    app = QApplication([])
    # widget = PersistentSlider()
    widget = las_table()
    widget.show()
    app.exec()

