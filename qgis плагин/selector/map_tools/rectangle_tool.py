from qgis.PyQt import QtCore, QtGui

from qgis.core import QgsGeometry, QgsRectangle, QgsPointXY
from qgis.gui import QgsMapTool, QgsRubberBand, QgsMapMouseEvent, QgsMapCanvas

from .text_canvas_item import QgsTextCanvasItem


class RectangleMapTool(QgsMapTool):

    def __init__(self, canvas: QgsMapCanvas) -> None:
        super().__init__(canvas)

        self.rubber_band = QgsRubberBand(canvas, True)
        self.rubber_band.setWidth(1)

        self.rect_centre: QgsPointXY = None
        self.geometry: QgsGeometry = None
        self.label = QgsTextCanvasItem(canvas, is_real_coords=True)

        self.area_limit = 10_000_000
        self.is_drawing = False

    def canvasPressEvent(self, event: QgsMapMouseEvent) -> None:
        # self.clean()
        if not self.is_drawing:
            self.is_drawing = True
            self.rect_centre = self.toMapCoordinates(event.pos())
            self.label.setPos(self.toMapCoordinates(event.pos()))
            self.label.size = 5
            self.label.setEnabled(True)
        else:
            self.is_drawing = False
        #     self.rect_centre = None
        #     self.label.setText(None)
        #     self.label.setEnabled(False)

    def canvasMoveEvent(self, event: QgsMapMouseEvent) -> None:
        if self.is_drawing:
            cursor_pos: QgsPointXY = self.toMapCoordinates(event.pos())

            half_width = abs(self.rect_centre.x() - cursor_pos.x())
            half_height = abs(self.rect_centre.y() - cursor_pos.y())

            if half_width * half_height * 4 <= self.area_limit:
                x_min, y_min = self.rect_centre.x() - half_width, self.rect_centre.y() - half_height
                x_max, y_max = self.rect_centre.x() + half_width, self.rect_centre.y() + half_height

                rectangle = QgsRectangle(x_min, y_min, x_max, y_max)
                rect_geometry = QgsGeometry.fromRect(rectangle)

                self.label.setText(f'{rect_geometry.area():.2f} кв. м')

                self.rubber_band.reset()
                self.rubber_band.setToGeometry(rect_geometry, None)
                self.geometry = rect_geometry

    def canvasReleaseEvent(self, event: QgsMapMouseEvent) -> None:
        if self.is_drawing:
            self.is_drawing = False

            if self.geometry:
                self.rubber_band.addGeometry(self.geometry)
                self.label.setText(f'{self.geometry.area():.2f} кв. м')

    def clean(self) -> None:
        self.rubber_band.reset()
        self.geometry = None
        self.rect_centre = None
        self.label.setText('')
        self.is_drawing = False

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == QtCore.Qt.Key_Escape:
            self.clean()

