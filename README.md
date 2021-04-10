# JP_script_scanner
## Русский
Средство с интерфейсом командной строки для сканирования скриптов японских программ и получения данных о словах и кандзи в них.
**До использования установите (см. последний раздел).**

На текущий момент может:
- показать общее количество уникальных слов;
- вывести найденные слова в словарных формах;
- отсортировать имеющиеся слова по частотам;
- показать общее количество уникальных кандзи;
- вывести имеющиеся кандзи;
- отсортировать имеющиеся кандзи по частотам;
- отсортировать кандзи по спискам (дзёё, дзиммэйё, хёгайдзи, N1-5);
- вывести принадлежность каждого кандзи.

## English
CLI tool for Japanese programs script scanning and words/kanji data in them obtaining.
**Install before usage (see the last paragraph).

Currently with this tool you can:
- show unique words number;
- output presented words in dictionary forms;
- sort the words by frequency;
- show unique kanji number;
- output presented kanji;
- sort presented kanji by frequency;
- sort presented kanji by lists (jouyou, jinmeijou, hyougaiji, N1-5);
- output each kanji list affilation.

# Usage
## Русский
- Запустите main.py с помощью Python 3.
- Введите папку, в которой содержатся скрипты (относительный или абсолютный путь к ней) *(папка по умолчанию in_files)*.
- Введите название кодировки (shift-jis, cp932, utf-8, utf-16 и так далее) скриптов.
- Введите название основы выходных файлов статистики.
- Введите название файла (в UTF-8) пользовательского списка слов для исключения *(для примера см. non-spoiler-list.txt)*.
- Введите название файла (в UTF-8) пользовательского списка кандзи для исключения *(аналогично non-spoiler-list.txt)*.
- *Отведайте вкусных французских булок да выпей же чаю*, пока программа работает.

## English
- Run main.py with Python 3.
- Enter the script folder (relative or absolute path) *(default folder is in_files)*.
- Enter the the name of scripts encoding (shift-jis, cp932, utf-8, utf-16 etc).
- Enter the base name of output statistics files.
- Enter the user bad words list name (file mush be in UTF-8) *(see non-spoiler-list.txt for reference)*.
- Enter the user bad kanji list name (file mush be in UTF-8) *(format is the same as in non-spoiler-list.txt)*.
- Wait for program running. You may want to go somewhere and watch *the quick brown fox jumps over the lazy dog*.

# Installation
## Русский
- Установите (https://www.python.org/downloads/)[Python].

## English
