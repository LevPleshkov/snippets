# доступ к активному слою.
cities = iface.activeLayer()

# параметры для применения инструмента.  в этом примере используется 
# инструмент 'Reproject Layer'.  открыв его в QGIS, можно увидеть, 
# какие необходимо указать параметры для его запуска.
reprojection_params = {
    'INPUT': cities,
    'TARGET_CRS': 'EPSG:32639',
    'OUTPUT': 'memory:'}

# функции `run` и `runAndLoadResults` позволяют запустить инструмент 
# и возвращают результат его применения, но последняя еще и 
# добавляет результат в качестве слоя на карту.
outout = processing.runAndLoadResults(
    'qgis:reprojectlayer',
    reprojection_params
    )

# не используя GUI QGIS для того, чтобы узнать, какие параметры
# доступны для того, или иного алгоритма, можно вызвать его
# документацию.
processing.algorithmHelp('qgis:reprojectlayer')

# чтобы получить полный список алгоритмов, можно вывести их id 
# и названия.  ВНИМАНИЕ - это может занять какое-то время.
for alg in QgsApplication.processingRegistry().algorithms():
    print(alg.id(), ':', alg.displayName())
