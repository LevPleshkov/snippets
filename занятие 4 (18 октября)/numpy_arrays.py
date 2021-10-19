import numpy as np



# 1. создание массивов 'numpy.ndarray'
# из списка объектов
a_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
array_from_list = np.array(a_list)

# `array_from_list` имеет размерность ('numpy.shape'), равную (10, ).
# первое измерение - 10, других измерений нет, т. к. массив одномерный. 
np.shape(array_from_list)

# с заданными значениями.  в функции, создающие массивы с заданными
# значениеми, нужно передать размерность массива в виде кортежа.   
#  - пустой массив из 4 'строк' и 5 'столбцов'
two_d_array = np.empty((4, 5))

#  - заполненный единицами или нулями
two_d_array = np.ones((4, 5))
three_d_array = np.zeros((3, 3, 10))

#  - случайными числами (не все параметры должны быть именваными)
random_array = np.random.uniform(low=0.0, high=3.0, size=(2, 2))

#  - равномерная последовательность чисел (не все параметры должны 
#    быть именваными и обязательными)
linear_array = np.arange(start=0, stop=10, step=1)
linear_array = np.linspace(start=0, stop=10, num=50)  # `num` - кол-во



# 2. поменять размерность массива можно с функцией numpy.reshape
reshaped_array = two_d_array.reshape((5, 4))

# или превратить в одномерный массив
flattened_array = random_array.ravel()



# 3. копировать массивы можно разными способами, но наиболее ясный -
# с помощью метода `copy`, который возвращает копию массива.
copied_array = flattened_array[:]
copied_array = flattened_array.copy()



# 4. индексация (views) - способ получить доступ к элементам массива
for i in range(4):
    for j in range(5):
        # 'традиционный' способ
        print(two_d_array[i][j])
        # с помощью view - через запятую указываются индексы для
        # каждого измерения массива
        print(two_d_array[i, j])

# можно использовать `list comprehension` - списковое включение -
# для более компактной записи вложенных циклов
[[print(two_d_array[i, j]) for j in range(5)] for i in range(4)] 

# первый элемент из каждой строки
two_d_array[:, 0]
# последний элеимент из каждой строки
two_d_array[:, -1]



# 4. удаление 1 и 3 элементов
truncated_array = np.delete(flattened_array, [0, 2])
# добавление строки в конец массива
extended_two_d_array = np.append(two_d_array, [[1, 2, 3, 4, 5]], axis=0)
# добавление столбца между 1 и 2 столбцами - в индекс 1
extended_two_d_array = np.insert(two_d_array, 1, [[1, 2, 3, 4]], axis=1)
# паремтр `axis` в двух предыдущих функциях определяет по какому 
# измерению необходимо провести операцию: 0 - строки, 1 - столбцы
# и т. д. 

# сортировка - метод `numpy.sort`, который возвращает отсортированную
# копию массива (доступны разные методы сортировки)
sorted_array = np.sort(flattened_array, kind='quicksort')

# или методом `ndarray.sort`, который сортирует массив, изменяя его
flattened_array.sort()


# 5. арифметические и алгебраические операции
a_matrix = np.array([
    np.arange(1, 4, 1),
    np.arange(4, 7, 1),
    np.arange(7, 10, 1)
    ])
b_matrix = a_matrix

# строка матрицы
a_vector = np.arange(1, 4, 1)
# столбец матрицы
b_vector = np.reshape(a_vector, (3, 1))

# поэлементное умножение / деление / сложение и т. д.
c_matrix = a_matrix * b_matrix
c_matrix = a_matrix / a_vector

# скалярное прозиведение
c_matrix = a_matrix.dot(4)
c_matrix = a_matrix.dot(a_vector)
c_matrix = a_matrix @ a_vector
c_matrix = a_matrix.dot(b_matrix)
c_matrix = a_matrix @ b_matrix

# векторное произведение
c_matrix = np.cross(a_matrix, b_matrix)
