from qgis.PyQt.QtCore import Qt, QRectF, QPoint
from qgis.PyQt.QtGui import QFont

from qgis.gui import QgsMapCanvasItem


class QgsTextCanvasItem(QgsMapCanvasItem):

    def __init__(self, canvas, size=18, is_real_coords=False, font=QFont('Arial', 10, QFont.Bold)) -> None:
        super().__init__(canvas)
        self.__canvas = canvas
        self.__point = None
        self.__text = None
        self.angle = None
        self.size = size
        self.is_real_coords = is_real_coords
        self.font = font
        self.width = None
        self.height = None

    def paint(self, painter, option=None, widget=None):
        if not self.__point or not self.__text:
            return

        try:
            if self.font:
                font = self.font
            else:
                font = painter.font()

            real_width = None
            real_height = None

            if self.is_real_coords:
                size = self.size / self.__canvas.mapUnitsPerPixel() * 72 / 96
                if self.width and self.height:
                    real_width = self.width / self.__canvas.mapUnitsPerPixel()
                    real_height = self.height / self.__canvas.mapUnitsPerPixel()
            else:
                size = self.size

            font.setPointSize(size * 10)
            painter.setFont(font)

            if real_width and real_height:
                painter.drawText(QRectF(self.__point.x()), self.__point.y() - real_height, real_width, real_height, \
                Qt.TextDontClip, self.__text)
            else:
                painter.drawText(self.__point, self.__text)
        except:
            pass

    def setText(self, text):
        self.__text = text
        self.update()

    def setTextRect(self, width, height):
        self.width = width
        self.height = height

    def text(self):
        return self.__text

    def setPos(self, point):
        if self.is_real_coords:
            p = self.__canvas.getCoordinateTransform().transform(point)
            self.__point = QPoint(int(p.x()), int(p.y()))
        else:
            self.__point = point
