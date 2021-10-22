# coding: utf-8

import geopandas as gpd
import matplotlib.pyplot as plt


# путь к папке с шейп-файлами наиболее крупных объектов мировой карты (континенты, оеканы, реки, внутренние воды).
data_path = r'............/world map'

# путь каждому шейп-файлу.
coastline_path = data_path + r'/ne_110m_coastline/ne_110m_coastline.shp'
land_path = data_path + r'/ne_110m_land/ne_110m_land.shp'
ocean_path = data_path + r'/ne_110m_ocean/ne_110m_ocean.shp'
lakes_path = data_path + r'/ne_110m_lakes/ne_110m_lakes.shp'
rivers_path = data_path + r'/ne_110m_rivers_lake_centerlines/ne_110m_rivers_lake_centerlines.shp'

# функция `read_file()` позволяет прочитывать данные из основных
#  файлов геоданных и возвращает объект `GeoDataFrame`, унаследованный
# от `DataFrame` pandas.  GeoDataFrame содержит столбец ('GeoSeries`)
# с геометрическими объектами: полигоны, линии, точки.
coastline = gpd.read_file(coastline_path)
land = gpd.read_file(land_path)
oceans = gpd.read_file(ocean_path)
lakes = gpd.read_file(lakes_path)
rivers = gpd.read_file(rivers_path)

# GeoDataFrame наследует интерфейс DataFrame.
lakes.head()

# функция `to_file()` позволяет записывать / конвертировать файлы
# в основные форматы геоданных.  аргумент `driver=` принимает
# строку с названием формата.
coastline.to_file(data_path + '/coastline.json', driver='GeoJSON')

# объект GeoDataFrame может содержать несколько GeoSeries с геометриями,
# каждый из которых может иметь свою систему координат.  чтобы увидеть,
# какая система координат задана активной геометрии, можно обратиться
# к атрибуту `crs`.  активной одновременно может быть только
# одна GeoSeries, и все геометрические методы GeoDataFrame будут
# применены только к этой GeoSeries.
lakes.crs

# чтобы установить систему координат, можно воспользоваться методом
# `set_crs`.  если система координат уже задана, можно репроецировать
# геометрии в другую методом `to_crs`.  аргументы этих методов:
#  - crs - объект pyproj.CRS,
#  - epsg - код системы координат,
#  - inplace - позволяет не копировать объект, а изменить текущий,
#  - allow_override - позволяет заменить текущую систему координат.
lakes = lakes.to_crs(3857)

# новая система координат.
lakes.crs

# репроецируем другие два геодатафрейма.
land.to_crs(epsg=3857, inplace=True)
rivers.to_crs(epsg=3857, inplace=True)

# после проецирования из географической в прямоугольную систему
# коориданат, можно выполнить простейшие преобразования, например,
#  - рассчитать площадь полигональных геометрий
land['area'] = land.area
lakes['area'] = lakes.area

#  - длину линейных и полигональных геометрий
rivers['length'] = rivers.length

#  - буффер у объектов любого типа
rivers['buffer'] = rivers.buffer(500_000)

# для визуализации геодатафреймов, можно обратиться к методам `plot`,
# и `explore` (при работе в jupyter notebooks).  метод `plot` принимает
# всевозможные параметры для настройки отображения карты при помощи
# библиотеки matplotlib.
# oceans.plot()
# oceans.explore()

# для того, чтобы буфферы рек, не выходили за пределы суши, возможно
# модифицироват геометрию так с помощью метода `overlay`.  метод
# принимает ссылку на другой геодатафрейм, и возвращает ссылку на
# модифицированный геодатафрейм.  параметры:
#  - right - другой геодатафрейм,
#  - how - способ пересечения (union, intersection, difference,
#    symmetrical difference)
#  - keep_geom_type - вернуть такие же геометрические объекты, как
#    те, что есть в геодатафрейме или нет,
#  - make_valid - произвести попытку восстановления некорретных
#    геометрий.
rivers.set_geometry('buffer')
rivers = rivers.overlay(land, 'intersection')

# для более точной настройки отображения, удобнее создать объекты
# Figure и Axes явным образом и добавить на них нужные геометрии.
fig, axes = plt.subplots(figsize=(8, 6))
axes.set_title('World Map')
axes.set_ylim(-1.5e7, 2e7)

# для того, чтобы добавить геометрию в область отрисовки,
# в методе `plot` нужно передать объект `Axes`, в котором
# будет построена карта.
land['geometry'].plot(ax=axes, color='orange', alpha=0.3)
rivers['geometry'].plot(ax=axes, color='#0099FF')
rivers['buffer'].plot(ax=axes, color='#0055AA', alpha=0.2)
lakes['geometry'].plot(ax=axes, color='#0099FF')

# при работе не в jupyter notebooks, нужно явно вызвать визуализацию.
plt.show()
