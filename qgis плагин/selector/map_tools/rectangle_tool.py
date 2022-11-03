from qgis.core import QgsGeometry
from qgis.gui import QgsMapTool, QgsRubberBand, QgsMapMouseEvent, QgsMapCanvas


class RectangelMapTool(QgsMapTool):

    def __init__(self, canvas: QgsMapCanvas) -> None:
        super().__init__(canvas)
        # self.canvas = canvas
        self.rubber_band = QgsRubberBand(canvas, True)
        self.rubber_band.setWidth(1)

        self.rect_centre = None
        self.geometry = None

    def canvasPressEvent(self, event: QgsMapMouseEvent) -> None:
        if self.rect_centre:
            self.rect_centre = None
            self.clean()
        else:
            self.rect_centre = self.toMapCoordinates(event.pos())

    def canvasMoveEvent(self, event: QgsMapMouseEvent) -> None:
        if self.rect_centre:
            cursor_pos = self.toMapCoordinates(event.pos())
            radius = self.rect_centre.distance(cursor_pos)

            self.rubber_band.reset()

            rect_geometry = QgsGeometry.fromRect(
                QgsGeometry.fromPointXY(self.rect_centre).buffer(radius, 50).boundingBox()
            )

            self.rubber_band.setToGeometry(rect_geometry, None)

            self.geometry = rect_geometry

            print(rect_geometry.area())

    def canvasReleaseEvent(self, event: QgsMapMouseEvent) -> None:
        if self.geometry:
            self.rubber_band.addGeometry(self.geometry)

    def clean(self) -> None:
        self.rubber_band.reset()
        self.geometry = None
