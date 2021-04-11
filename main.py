# By Tester.
# testertesterovtesterovich@yandex.ru

from JP_script_scanner import JP_script_scanner
import os

default_folder = 'in_files'

def chasen_testing_func():
    import MeCab
    stringer = "決まった形がなく　次々と形を変える"
    tagger = MeCab.Tagger("-Ochasen")  # -Oyomi, #-Ochasen, #-Odump, #-Owakati,
    dobro = []
    zlo = tagger.parse(stringer).split('\n')
    if (zlo[-1] == ''):
        zlo.pop(-1)
    if (zlo[-1] == 'EOS'):
        zlo.pop(-1)
    for i in zlo:
        try:
            dobro.append(i.split('\t')[2])
        except:
            dobro.append(i.split('\t')[0])
            print(i)
    print(zlo)
    print(dobro)
    exit()

def dump_testing_func():
    import MeCab
    stringer = "決まった形がなく　次々と形を変える"
    tagger = MeCab.Tagger("-Odump")  # -Oyomi, #-Ochasen, #-Odump, #-Owakati,
    dobro = []
    resulter = tagger.parse(stringer).split('\n')
    resulter.pop(0)
    resulter.pop(-1)
    resulter.pop(-1)
    for i in range(len(resulter)):
        resulter[i] = resulter[i].split(' ')
        #print(resulter[i])
        #first_res = resulter[i][1]
        second_res = resulter[i][2].split(',')[7]
        dobro.append(second_res)
    print(dobro)
    exit()

def testing_func():
    name = 'test'
    bad_words = []
    bad_kanji = []
    in_folder = default_folder
    encoding = 'utf-8'
    scannow = JP_script_scanner(in_folder, encoding, bad_words, bad_kanji)
    scannow.kanji_data_to_file('{}_KANJI.txt'.format(name))
    scannow.word_data_to_file('{}_WORDS.txt'.format(name))
    del scannow
    exit()

if __name__ == '__main__':
    #dump_testing_func()

    if (not (os.path.isdir(default_folder))):
        os.makedirs(default_folder, exist_ok=True)
    in_folder = input('Введите папку скриптов (по умолчанию {0})/\n'
                      'Enter the script folder (default: {0}): '.format(default_folder))
    if (not (os.path.isdir(in_folder))):
        print('Нет такой папки. Используем папку по-умолчанию.../'
              '\nThere is no such folder. Using default folder...')
        in_folder = default_folder
    encoding = input('Введите название кодировки (shift-jis, cp932, utf-8, utf-16 и так далее.../'
                     '\nEnter the encoding name (shift-jis, cp932, utf-8, utf-16 etc...): ')
    name = input('Введите основу выходного названия статистики/\n'
                 'Enter the base of output data name: ')
    bad_words_file = input('Введите название файла (UTF-8) списка слов для исключения/\n'
                           'Enter the bad words list file (UTF-8) name: ')
    bad_kanji_file = input('Введите название файла (UTF-8) списка кандзи для исключения/\n'
                           'Enter the bad kanji (UTF-8) list file name: ')
    bad_words = []
    bad_kanji = []
    try:
        if (not (os.path.isfile(bad_words_file))):
            raise FileNotFoundError("No such file.")
        bad_worder = open(bad_words_file, 'r', encoding='utf-8')
        while True:
            new_line = bad_worder.readline()
            if (new_line == ''):
                break
            bad_words.append(new_line.rstrip().lstrip())
        bad_worder.close()
    except:
        print('Ошибка загрузки файла слов для исключения/\n'
              'Error of loading bad words list.')
    try:
        if (not (os.path.isfile(bad_kanji_file))):
            raise FileNotFoundError("No such file.")
        bad_kanjier = open(bad_kanji_file, 'r', encoding='utf-8')
        while True:
            new_line = bad_kanjier.readline()
            if (new_line == ''):
                break
            bad_kanji.append(new_line.rstrip().lstrip())
        bad_kanjier.close()
    except:
        print('Ошибка загрузки файла кандзи для исключения/\n'
              'Error of loading bad kanji list.')

    scannow = JP_script_scanner(in_folder, encoding, bad_words, bad_kanji)
    scannow.kanji_data_to_file('{}_KANJI.txt'.format(name))
    scannow.word_data_to_file('{}_WORDS.txt'.format(name))
    del scannow
