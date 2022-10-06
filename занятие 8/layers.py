data_dir = os.path.join(os.path.expanduser('~'),
    'Documents',
    'Курс QGIS & Python',
    'Perm Krai',
    'shape_files')
file_name = 'territory.shp'

path = os.path.join(data_dir, file_name)
iface.addVectorLayer(path, 'perm_territory', 'ogr')

layer = iface.activeLayer()
layer.setName('perm_territory')



# метод `mapLayers` возвращает словарь из всех слоев проекта,
# в котором ключ - строка с названием и id слоя, а значение - 
# объект типа `QgsVectorLayer`, или друго типа слоя.
for layer in QgsProject.instance().mapLayers().values():
    print(layer.name())


# метод `layers` возвращает список объектов всех
# видимых на карте слоев.
for layer in iface.mapCanvas().layers():
    print(layer.name())


# метод `layers` возвращает список объектов всех
# выбранных в списке слоев.
for layer in iface.layerTreeView().selectedLayers():
    print(layer.name())


# метод `getFeatures` - итератор, возвращающий 
# объекты типа `QgsFeature` - элемент, соответствуюзий строке
# таблицы атрибутов.
for f in layer.getFeatures():
    # с помощью `[]` можно обращаться к атрибутам элемента.
    print(f['name'])
