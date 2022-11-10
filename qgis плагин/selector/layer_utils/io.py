from typing import Union
import os

from osgeo import ogr

from qgis.core import QgsVectorFileWriter, QgsVectorLayer
from qgis.PyQt.QtWidgets import QMessageBox


def write_layer_to_gpkg(gpkg_name: str, layer: QgsVectorLayer, out_name: str) -> Union[str, None]:
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteFile
    options.layerName = out_name.replace(' ', '_')
    error, error_string = QgsVectorFileWriter.writeAsVectorFormat(layer, gpkg_name, options)
    if error != QgsVectorFileWriter.NoError:
        return f'Ошибка при записи GeoPackage: {error_string}'
    else:
        return


def create_gpkg(dir: str, name: str) -> Union[str, None]:
    gpkg = os.path.normpath(os.path.join(dir, f'{name}.gpkg'))

    if os.path.exists(gpkg):
        answer = QMessageBox.information(
            None,
            'Внимание!',
            f'GeoPackage с именем {name} уже существует в папке {dir}' + '\n' + 'Перезаписать?',
            QMessageBox.StandartButtons(QMessageBox.Yes | QMessageBox.No)
        )

        if answer == QMessageBox.No:
            return

    driver = ogr.GetDriverByName('GPKG')
    data_source = driver.CreateDataSource(gpkg)

    if not os.path.exists(gpkg):
        del driver
        del data_source
        return
