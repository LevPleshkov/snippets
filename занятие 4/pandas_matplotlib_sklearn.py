import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from scipy.signal import savgol_filter

# атрибут `rcParams` позволяет задавать заранее некоторые
# общие параметры для всех последующих графических построений.
plt.rcParams['figure.figsize'] = (50, 3)

# путь к файлу с измерениями акустического сигнала.
file_path = r'signals.csv'

# `pandas` умеет читать различные форматы файлов и создает
# из их содержимого объект `DataFrame`, который состоит из
# объектов `Series` - столбцов с названием и данными.
signal_df = pd.read_csv(file_path)

# посмотреть датафрейм в виде начала или окончания таблицы
# можно с помощью методов `head` и `tail`. другие методы 
# позволяют получить статистику, получить доступ по индексам. 
signal_df.head()
signal_df.tail()

# посколько в csv-файле не содержалось строки с названиями колонок,
# можно добавить их к датарейму. 
signal_df.columns = ['time', 'channel_1', 'channel_2']

# перед построением потребуется немного подготовить исходные данные.
# обратиться к столбцу датафрейма можно по его названию - либо как 
# к атрибуту (в первом пункте), либо как к элементу словаря (во втором
# пункте).  у `Series` есть метод `to_numpy`, возвращающий значения
# в виде массива `ndarray`. 
# 1) центрируем их относительно среднего значения
signal_df.channel_1 = [n - np.mean(signal_df.channel_1.to_numpy()) for n in signal_df.channel_1.to_numpy()]
# 2) "нормализуем"
signal_df.channel_1 = [n / np.max(signal_df['channel_1'].to_numpy()) for n in signal_df.channel_1.to_numpy()]
# 3) сгладим
signal_df.channel_1 = savgol_filter(signal_df.channel_1, 21, 3)


# выполним быстрое преобразование Фурье для того, чтобы получить АЧХ
# сигнала.  модуль `scipy.signal.windows` содержит несколько
# оконных функций, которые можно применить для БПФ.
window = sp.signal.windows.flattop(len(signal_df.channel_1))
# на основе шага дискретизации (разница времен) рассчитаем
# частоты спектральной характеристики.  `numpy` содержит
# готовые функции для БПФ.  `rfft` - real fast Fourier transform,
# или действительная часть спектра БПФ.  `rfftfreq` - частоты спектра.
freqs = np.fft.rfftfreq(len(signal_df.channel_1), signal_df.time[1] - signal_df.time[0])
# рассчитаем амплитуды спектра.
amps = np.fft.rfft(signal_df.channel_1 * window)
# и спектральную фунцию мощности, power density spectrum.
pds = amps ** 2


# для демонстрации простоты работы с модулем `scikit-klearn`,
# выполним кластеризацию методом k-средних исходного сигнала.
# для этого создадим объект с заданными параметрами: число кластеров,
# случайную инициализацию цетроидов кластеров, сколько раз алгоритм
# будет выолняться и т. д. 
kmeans = KMeans(
    n_clusters=3, init='random', n_init=10,
    max_iter=300, tol=1e-04, random_state=0
)
# вызвав метод `fit_predict` с параметрами в виде массива `ndarray`,
# состоящего из значений сигнала, запишем полученные значения кластеров
# в новый столбец (новую `Series`) датафрейма. 
signal_df['k_means'] = kmeans.fit_predict(
    signal_df.channel_1.to_numpy().reshape(-1, 1)
)


# подсобная функция для вывода на экран графиков 
# с помощью 'matplotlib', содержащих любые из полученных 
# выше массивов информации.
def plot_signal(time, values, xlim=None, ylim=None, xlog=False, ylog=False):
    # метод возвращает ссылку на единственный график (объект `Axes`), 
    # который будет содержаться в области отрисовки (объект `Figure`).
    # с помощью метода `subplots` можно получить ссылки на несколько 
    # объектов `Axes`, если нужно разместить на рисунке несколько графиков.
    axes = plt.subplot()
    # `Axes` обладает множеством методов для настройки шрифтов, подписей
    # осей, выбора цены деления и прочего. 
    axes.tick_params(labelsize=10)
    axes.grid(True, which='both')

    if xlim:
        axes.set_xlim(xlim)
    if ylim:
        axes.set_ylim(ylim)
    if xlog:
        axes.set_xscale('log')
    if ylog:
        axes.set_yscale('log')

    # метод `plot` строит график в виде линии.  другие методы (такие
    # как `scatter`, `loglog`, `hist` и др.) позволяют строить другие
    # всевозможные типы диаграмм, растровых и контурных 
    # карт (не географических).
    axes.plot(time, values)
    # для вывода на экран в отдельном окне.  этого не требуется 
    # при работе в Jupyter Notebooks.
    plt.show()


if __name__ == '__main__':
    # исходный сигнал
    plot_signal(signal_df.time, signal_df.channel_1)
    
    # спектр
    plot_signal(freqs, amps, ylim=(10e-6, 10e4))  #, xlog=True, ylog=True)

    # значения кластеров
    plot_signal(signal_df.time, signal_df.k_means)
