import os

path = r'/Users/levpleshkov/Documents/Курс Автоматизация QGIS/snippets/file reading/csv files'

for dir_path, dir_names, file_names in os.walk(path):
    # dir_path      – путь к директории
    # dir_names     - список имен каждой вложенной директории
    # file_names    - список имен каждого вложенного файла

    # если файлов несколько, можем пробежать по всем с помощью цикла
    for file_name in file_names:
        # чтобы открыть файл, понадобится полный путь к нему, а не имя
        # соединяем путь к папке с путем к файлу
        file_path = os.path.join(dir_path, file_name)

        # открываем файл
        with open(file_path) as file:
            # пустая строка для перезаписи файла
            new_content = ""

            # csv файл состоит из строк, и можно прочитать его построчно
            for line in file:
                # можно проверить, с чего начинается строка и, например, игнорировать ее
                if line.startswith('"'):
                    pass

                # в противном случае, можно, например, заменить в строке символы
                else:
                    line = line.replace(':', '-')

                # и добавить строку для нового файла
                new_content += line

            # после построчного прочтения файла, открываем файл под тем же названием в режиме записи,
            # находясь в той же дирекории, и записываем в него новое содержимое
            with open(file_path, 'w') as new_file:
                new_file.write(new_content)

# в результате, мы будем иметь перезаписанный файл, с внесенными изменениями.
