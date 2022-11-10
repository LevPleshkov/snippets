import math

from qgis.PyQt import QtCore, QtGui

from qgis.core import QgsGeometry, QgsRectangle, QgsPointXY
from qgis.gui import QgsMapTool, QgsRubberBand, QgsMapMouseEvent, QgsMapCanvas

from .text_canvas_item import QgsTextCanvasItem


class RectangleMapTool(QgsMapTool):

    def __init__(self, canvas: QgsMapCanvas) -> None:
        super().__init__(canvas)

        self.rubber_band = QgsRubberBand(canvas, True)

        self.rubber_band.setWidth(1)

        self.label = QgsTextCanvasItem(canvas, is_real_coords=True)

        self.rect_centre: QgsPointXY = None
        self.geometry: QgsGeometry = None

        # quarter of max area
        self.area_limit = 25_000_000

        self.done_drawing = False

    def canvasPressEvent(self, event: QgsMapMouseEvent) -> None:
        if self.geometry:
            self.clean()
        else:
            self.rect_centre = self.toMapCoordinates(event.pos())
            self.label.setPos(self.toMapCoordinates(event.pos()))
            self.label.size = 5
            self.label.setEnabled(True)

    def canvasMoveEvent(self, event: QgsMapMouseEvent) -> None:
        if not self.done_drawing and self.rect_centre:
            cursor_pos: QgsPointXY = self.toMapCoordinates(event.pos())

            half_width = abs(self.rect_centre.x() - cursor_pos.x())
            half_height = abs(self.rect_centre.y() - cursor_pos.y())

            area_criteria = self.area_limit - half_width * half_height
            if area_criteria < 0:
                return

            # snap rectangle to max area
            if area_criteria < 500_000:
                r = half_width / half_height
                half_width = math.sqrt(self.area_limit * r)
                half_height = math.sqrt(self.area_limit / r)

            x_min, y_min = self.rect_centre.x() - half_width, self.rect_centre.y() - half_height
            x_max, y_max = self.rect_centre.x() + half_width, self.rect_centre.y() + half_height

            rectangle = QgsRectangle(x_min, y_min, x_max, y_max)
            rect_geometry = QgsGeometry.fromRect(rectangle)

            self.label.setText(self.area_string())

            self.rubber_band.reset()
            self.rubber_band.setToGeometry(rect_geometry, None)

            self.geometry = rect_geometry

    def canvasReleaseEvent(self, event: QgsMapMouseEvent) -> None:
        if self.geometry:
            self.done_drawing = True
            self.rubber_band.addGeometry(self.geometry)
            self.label.setText(self.area_string())

    def clean(self) -> None:
        self.done_drawing = False
        self.rect_centre = None
        self.geometry = None
        self.rubber_band.reset()
        self.label.setEnabled(False)
        self.label.setText(None)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == QtCore.Qt.Key_Escape:
            self.clean()

    def area_string(self):
        if self.geometry:
            return f'{self.geometry.area()*1e-6:.2f} кв. км'
