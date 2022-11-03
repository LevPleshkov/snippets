import os.path
from dataclasses import dataclass

from qgis.core import QgsLayerTreeLayer, QgsVectorLayer


@dataclass
class LayerInfo:
    source: str
    source_layer: str
    node_name: str
    style: str
    visible: bool = False


def create_layer_from_gpkg(src, src_layer, layer_name, crs) -> QgsVectorLayer:
    layer_source = f'{src}|layername={src_layer}'
    qgis_layer = QgsVectorLayer(layer_source, layer_name, 'ogr')
    qgis_layer.setCrs(crs)
    if qgis_layer.isValid():
        return qgis_layer
    else:
        print('Layer is not valid')


def set_layer_style(layer: QgsVectorLayer, style_name, style_path) -> None:
    style_path = os.path.join(style_path, style_name)
    layer.loadNamedStyle(style_path, True)
    layer.triggerRepaint()


def set_layer_node_visibility(node: QgsLayerTreeLayer, visible: bool) -> None:
    node.setItemVisibilityChecked(visible)
