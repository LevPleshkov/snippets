import os
from typing import Union
from qgis.core import (
    QgsProject,
    QgsMapSettings,

    QgsMapRendererParallelJob,
    QgsLayoutExporter,
    QgsReadWriteContext,

    QgsRectangle,
    QgsUnitTypes,

    QgsPrintLayout,
    QgsLayoutItemMap,
    QgsLayoutPoint,
    QgsLayoutSize,
    QgsLayoutItemLabel,
)

from qgis.PyQt.QtWidgets import QFileDialog
from qgis.PyQt.QtGui import QColor, QFont
from qgis.PyQt.QtCore import QSize
from qgis.PyQt.QtXml import QDomDocument


def ask_for_folder(init_folder: str = '/') -> Union[str, None]:
    out_path = QFileDialog.getExistingDirectory(None, 'Output folder', init_folder, QFileDialog.ShowDirsOnly)
    return out_path if out_path else QgsProject.instance().homePath()


def export_map_canvas(layer):
    folder_path = ask_for_folder()
    file_path = os.path.join(folder_path, 'example.png')

    settings = QgsMapSettings()
    settings.setLayers([layer])
    settings.setBackgroundColor(QColor(255, 255, 255))
    settings.setOutputSize(QSize(800, 600))
    settings.setExtent(layer.extent())

    renderer = QgsMapRendererParallelJob(settings)

    def save():
        img = renderer.renderedImage()
        img.save(file_path, 'png')

    renderer.finished.connect(save)
    renderer.start()


def export_with_layout(iface):
    project = QgsProject.instance()
    layout_name = "Example Layout"

    layouts = project.layoutManager().printLayouts()
    for layout in layouts:
        if layout.name() == layout_name:
            project.layoutManager().removeLayout(layout)

    layout = QgsPrintLayout(project)
    layout.initializeDefaults()
    layout.setName(layout_name)
    project.layoutManager().addLayout(layout)

    map_item = QgsLayoutItemMap(layout)
    map_item.setRect(20, 20, 20, 20)
    map_settings = QgsMapSettings()
    map_settings.setLayers([iface.activeLayer()])
    rect = QgsRectangle(iface.mapCanvas().extent())
    map_settings.setExtent(rect)
    map_item.setExtent(rect)
    map_item.attemptMove(QgsLayoutPoint(5, 5, QgsUnitTypes.LayoutMillimeters))
    map_item.attemptResize(QgsLayoutSize(200, 200, QgsUnitTypes.LayoutMillimeters))
    layout.addLayoutItem(map_item)

    layout.refresh()

    folder_path = ask_for_folder()
    file_path = os.path.join(folder_path, 'example.pdf')

    exporter = QgsLayoutExporter(layout)
    exporter.exportToPdf(file_path, QgsLayoutExporter.PdfExportSettings())


def export_with_template(iface):
    project = QgsProject.instance()
    layout_name = "Example Layout"

    layouts = project.layoutManager().printLayouts()
    for layout in layouts:
        if layout.name() == layout_name:
            project.layoutManager().removeLayout(layout)

    with open(r'/Users/levpleshkov/Desktop/test.qpt') as file:
        template_file = file.read()

    layout = QgsPrintLayout(project)
    layout.initializeDefaults()
    layout.setName(layout_name)
    project.layoutManager().addLayout(layout)

    document = QDomDocument()
    document.setContent(template_file)

    items = layout.loadFromTemplate(document, QgsReadWriteContext(), False)

    title = QgsLayoutItemLabel(layout)
    title.setText('Example layout creation')
    title.setFont(QFont('Arial', 24))
    title.adjustSizeToText()
    layout.addLayoutItem(title)

    iface.openLayoutDesigner(layout)
