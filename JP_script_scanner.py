import random
import os
import MeCab
import kanji_lists

class JP_script_scanner:
    bad_words = ['',
                 'よう',
                 'から',
                 'じゃ',
                 'って',
                 'っと',
                 'なぁ',
                 'さぁ',
                 'ゃっ',
                 'ボリュ',
                 'ねぇ',
                 'あっ',
                 'じゃあ',
                 'はっ',
                 'れる',
                 'たい',
                 'あッ',
                 'はぁ',
                 'のに',
                 'とか',
                 'まぁ',
                 'られる',
                 'てる',
                 'せる',
                 'じゃん',
                 'たり',
                 'ちゃう',
                 'しまう',
                 ]
    bad_kanji = []
    def __init__(self, iner, encoding, new_bad_words, new_bad_kanji):
        self._mode = -1
        self._iner = iner
        try:
            self._test_iner()
        except:
            print(self._iner, "is not exist!")
        self._encoding = encoding
        # cp932, shift-jis, utf-8
        self._new_bad_words = self.bad_words
        self._new_bad_words.extend(new_bad_words)
        self._new_bad_kanji = self.bad_kanji
        self._new_bad_kanji.extend(new_bad_kanji)
    def kanji_data_to_file(self, toer):
        self._add_kanji_data_from_files(toer)
    def word_data_to_file(self, toer):
        self._add_word_data_from_files(toer)

    def _test_iner(self):
        if (os.path.isfile(self._iner)):
            self._mode = 0
        elif (os.path.isdir(self._iner)):
            self._mode = 1
        else:
            raise FileExistsError(self._iner, "is not exist!")
    def _add_kanji_data_from_files(self, toer):
        symbols = []
        freq = []
        count = 0
        jo_count = 0
        jin_count = 0
        hyo_count = 0
        n5_count = 0
        n4_count = 0
        n3_count = 0
        n2_count = 0
        n1_count = 0

        technical = 0
        file_array = []
        if (self._mode == -1):
            self._test_iner()
        if (self._mode == 0):
            file_array.append(self._iner)
        elif (self._mode == 1):
            for root, dirs, files in os.walk(self._iner):
                for file in files:
                    file_array.append(root + os.sep + file)
        else:
            raise Exception("Wrong mode!")
        aller = len(file_array)


        definer = int(aller // 100.)
        if (definer == 0):
            definer = 1

        for i in file_array:
            count = self._add_kanji_data_from_file(i, symbols, freq, count)
            technical += 1
            if ((technical % definer) == 0):
                print("Текущий прогресс по кандзи/Current kanji progress: " + str(technical * 100 / aller) + "%.")

        count = self._bad_filter(symbols, freq, count, self._new_bad_kanji)

        kanji = symbols.copy()
        typer = []
        leveller = []

        joyo = []
        jinmeyou = []
        hyougaiji = []
        n5 = []
        n4 = []
        n3 = []
        n2 = []
        n1 = []

        all_freq = 0
        joyo_freq = 0
        jinmeyou_freq = 0
        hyougaiji_freq = 0
        n5_freq = 0
        n4_freq = 0
        n3_freq = 0
        n2_freq = 0
        n1_freq = 0

        for i in range(len(kanji)):
            zlo_string = ''
            all_freq += freq[i]
            if kanji[i] in kanji_lists.JOYO:
                joyo_freq += freq[i]
                joyo.append(kanji[i])
                jo_count += 1
                zlo_string = 'ДЗЁ:Ё:/JOUYOU. '
            elif kanji[i] in kanji_lists.JINMEIYO:
                jinmeyou_freq += freq[i]
                jinmeyou.append(kanji[i])
                jin_count += 1
                zlo_string = 'ДЗИММЭЙЁ:/JINMEIYOU. '
            else:
                hyougaiji_freq += freq[i]
                hyougaiji.append(kanji[i])
                hyo_count += 1
                zlo_string = 'ХЁ:ГАЙДЗИ/HYOUGAIJI. '
            dobro_string = ''
            if kanji[i] in kanji_lists.JLPT.N5:
                n5_freq += freq[i]
                n5.append(kanji[i])
                n5_count += 1
                dobro_string = 'N5.'
            elif kanji[i] in kanji_lists.JLPT.N4:
                n4_freq += freq[i]
                n4.append(kanji[i])
                n4_count += 1
                dobro_string = 'N4.'
            elif kanji[i] in kanji_lists.JLPT.N3:
                n3_freq += freq[i]
                n3.append(kanji[i])
                n3_count += 1
                dobro_string = 'N3.'
            elif kanji[i] in kanji_lists.JLPT.N2:
                n2_freq += freq[i]
                n2.append(kanji[i])
                n2_count += 1
                dobro_string = 'N2.'
            elif kanji[i] in kanji_lists.JLPT.N1:
                n1_freq += freq[i]
                n1.append(kanji[i])
                n1_count += 1
                dobro_string = 'N1.'
            typer.append(zlo_string)
            leveller.append(dobro_string)
        out_file = open(toer, mode='w', encoding="utf-8")
        out_file.write('=== Частотные ряды кандзи/Kanji frequency row:\n\n')
        out_file.write('У — уникальные/U — unique.\nЧ — частотные/F — frequent.\n')
        out_file.write('== Дзё:ё - дзиммэйё: - хё:гайдзи./Jouyou - jinmeiyou - hyougaiji.\n')
        out_file.write('У/U: ' + str(round(jo_count/count*100, 2)) + '% - ' + str(round(jin_count/count*100, 2)) +
                       '% - ' + str(round(hyo_count/count*100, 2)) + '%.\n')
        out_file.write('Ч/F: ' + str(round(joyo_freq/all_freq*100, 2)) + '% - ' +
                       str(round(jinmeyou_freq/all_freq*100, 2)) + '% - ' +
                       str(round(hyougaiji_freq/all_freq*100, 2)) + '%.\n')
        out_file.write('== N5 - N4 - N3 - N2 - N1.\n')
        out_file.write('У/U: ' + str(round(n5_count/count*100, 2)) + '% - ' + str(round(n4_count/count*100, 2)) + '% - ' +
                       str(round(n3_count/count*100, 2)) + '% - ' + str(round(n2_count/count*100, 2)) + '% - ' +
                       str(round(n1_count/count*100, 2)) + "%.\n")
        out_file.write('Ч/F: ' + str(round(n5_freq/all_freq*100, 2)) + '% - ' + str(round(n4_freq/all_freq*100, 2)) +
                       '% - ' + str(round(n3_freq/all_freq*100, 2)) + '% - ' +
                       str(round(n2_freq/all_freq*100, 2)) + '% - ' + str(round(n1_freq/all_freq*100, 2)) + "%.")

        out_file.write('\n\n=== Уникальные кандзи/Unique kanji (У/U ' + str(count) + ")"
                        " {Ч/F " + str(all_freq) + "}:\n\n")
        for i in range(len(symbols)):
            out_file.write(symbols.pop(random.randint(0, len(symbols) - 1)))
        out_file.write('\n\n=== Уникальные дзё:ё:-кандзи/Unique jouyou kanji'
                        ' [У/U ' + str(jo_count) + ' ~' + str(round(jo_count/count*100, 2)) + '%]'
                        ' {Ч/F ' + str(joyo_freq) + " ~" + str(round(joyo_freq/all_freq*100, 2)) + "%}:\n\n")
        for i in range(len(joyo)):
            out_file.write(joyo.pop(random.randint(0, len(joyo) - 1)))
        out_file.write('\n\n=== Уникальные дзиммэйё::-кандзи/Unique jinmeiyou kanji'
                        ' [У/U ' + str(jin_count) + ' ~' + str(round(jin_count/count*100, 2)) + '%]'
                        ' {Ч/F ' + str(jinmeyou_freq) + " ~" + str(round(jinmeyou_freq/all_freq*100, 2)) + "%}:\n\n")
        for i in range(len(jinmeyou)):
            out_file.write(jinmeyou.pop(random.randint(0, len(jinmeyou) - 1)))
        out_file.write('\n\n=== Уникальные хё:гайдзи/Unique hyougaiji'
                        ' [У/U ' + str(hyo_count) + ' ~' + str(round(hyo_count/count*100, 2)) + '%]'
                        ' {Ч/F ' + str(hyougaiji_freq) + " ~" + str(round(hyougaiji_freq/all_freq*100, 2)) + "%}:\n\n")
        for i in range(len(hyougaiji)):
            out_file.write(hyougaiji.pop(random.randint(0, len(hyougaiji) - 1)))
        out_file.write('\n\n=== Уникальные N5-кандзи/Unique N5 kanji'
                        ' [У/U ' + str(n5_count) + ' ~' + str(round(n5_count/count*100, 2)) + '%]'
                        ' {Ч/F ' + str(n5_freq) + " ~" + str(round(n5_freq/all_freq*100, 2)) + "%}:\n\n")
        for i in range(len(n5)):
            out_file.write(n5.pop(random.randint(0, len(n5) - 1)))
        out_file.write('\n\n=== Уникальные N4-кандзи/Unique N4 kanji'
                        ' [У/U ' + str(n4_count) + ' ~' + str(round(n4_count/count*100, 2)) + '%]'
                        ' {Ч/F ' + str(n4_freq) + " ~" + str(round(n4_freq/all_freq*100, 2)) + "%}:\n\n")
        for i in range(len(n4)):
            out_file.write(n4.pop(random.randint(0, len(n4) - 1)))
        out_file.write('\n\n=== Уникальные N3-кандзи/Unique N3 kanji'
                        ' [У/U ' + str(n3_count) + ' ~' + str(round(n3_count/count*100, 2)) + '%]'
                        ' {Ч/F ' + str(n3_count) + " ~" + str(round(n3_freq/all_freq*100, 2)) + "%}:\n\n")
        for i in range(len(n3)):
            out_file.write(n3.pop(random.randint(0, len(n3) - 1)))
        out_file.write('\n\n=== Уникальные N2-кандзи/Unique N2 kanji'
                        ' [У/U ' + str(n2_count) + ' ~' + str(round(n2_count/count*100, 2)) + '%]'
                        ' {Ч/F ' + str(n2_freq) + " ~" + str(round(n2_freq/all_freq*100, 2)) + "%}:\n\n")
        for i in range(len(n2)):
            out_file.write(n2.pop(random.randint(0, len(n2) - 1)))
        out_file.write('\n\n=== Уникальные N1-кандзи/Unique N1 kanji'
                        ' [У/U ' + str(n1_count) + ' ~' + str(round(n1_count/count*100, 2)) + '%]'
                        ' {Ч/F ' + str(n1_freq) + " ~" + str(round(n1_freq/all_freq*100, 2)) + "%}:\n\n")
        for i in range(len(n1)):
            out_file.write(n1.pop(random.randint(0, len(n1) - 1)))
        out_file.write('\n\n=== Кандзи по частоте/Kanji\'s frequency:\n')
        for i in range(len(kanji)):
            most = 0
            index = -1
            for j in range(len(kanji)):
                if (freq[j] > most):
                    most = freq[j]
                    index = j
            out_file.write("\n" + str(i + 1) + ". " + kanji.pop(index) + " — " + str(most) + ". " + typer.pop(index) + leveller.pop(index))
            freq.pop(index)
        out_file.close()
        print(count)
    def _add_kanji_data_from_file(self, fromer, symbols, freq, count):
        in_file = open(fromer, mode='r', encoding=self._encoding)
        symb = in_file.read(1)
        while (symb != ''):
            try:
                freq[symbols.index(symb)] += 1
            except:
                if ((ord(symb) >= 0x4E00) and (ord(symb) < 0x9FC0)):
                    count += 1
                    symbols.append(symb)
                    freq.append(1)
            symb = in_file.read(1)
        in_file.close()
        return count

    def _add_word_data_from_files(self, toer):
        symbols = []
        freq = []
        count = 0

        technical = 0
        file_array = []
        if (self._mode == -1):
            self._test_iner()
        if (self._mode == 0):
            file_array.append(self._iner)
        elif (self._mode == 1):
            for root, dirs, files in os.walk(self._iner):
                for file in files:
                    file_array.append(root + os.sep + file)
        else:
            raise Exception("Wrong mode!")
        aller = len(file_array)


        definer = int(aller // 100.)
        if (definer == 0):
            definer = 1

        for i in file_array:
            count = self._add_word_data_from_file(i, symbols, freq, count)
            technical += 1
            if ((technical % definer) == 0):
                print("Текущий прогресс по словам/Current words progress: " + str(technical * 100 / aller) + "%.")
        k = 0
        while (k < len(symbols)):
            if (not (self._is_good_word(symbols[k]))):
                symbols.pop(k)
                freq.pop(k)
                count -= 1
                continue
            k += 1
        count = self._bad_filter(symbols, freq, count, self._new_bad_words)

        out_file = open(toer, mode='w', encoding="utf-8")
        out_file.write('=== Уникальные слова/Unique words (' + str(count) + "):\n\n")
        word = symbols.copy()
        for i in range(len(symbols)):
            out_file.write(symbols.pop(random.randint(0, len(symbols) - 1)))
            if (i >= (len(word)-1)):
                out_file.write('.')
            else:
                out_file.write('; ')
        out_file.write('\n\n=== Слова по частоте/Words frequency:\n')
        for i in range(len(word)):
            most = 0
            index = -1
            for j in range(len(word)):
                if (freq[j] > most):
                    most = freq[j]
                    index = j
            out_file.write("\n" + str(i + 1) + ". " + word.pop(index) + " — " + str(most) + ".")
            freq.pop(index)
        out_file.close()
        print(count)

    def _add_word_data_from_file(self, fromer, symbols, freq, count):
        tagger = MeCab.Tagger("-Odump")
        in_file = open(fromer, mode='r', encoding=self._encoding)
        new_line = in_file.readline()
        while (new_line != ''):
            new_line = self._prepare_line(new_line)
            if (not (self._is_japanese(new_line))):
                new_line = in_file.readline()
                continue
            many_words = []

            zlo = tagger.parse(new_line).split('\n')
            zlo.pop(-1)
            zlo.pop(-1)
            zlo.pop(0)
            for i in range(len(zlo)):
                zlo[i] = zlo[i].split(' ')
                second_res = zlo[i][2].split(',')[-3]
                many_words.append(second_res)

            for word in many_words:
                if (not (self._is_japanese(word))):
                    continue
                try:
                    freq[symbols.index(word)] += 1
                except:
                    count += 1
                    symbols.append(word)
                    freq.append(1)
            new_line = in_file.readline()
        in_file.close()
        del tagger
        return count
    def _prepare_line(self, liner):
        delete_these = '」〜！？）　…「『』。、一（―□“”↑↓'
        new_liner = ''
        if True:
            new_liner = liner.rstrip().lstrip()
            new_liner.replace('ー', 'ー')
            for j in delete_these:
                new_liner = new_liner.replace(j, '^')
        return new_liner
    def _is_japanese(self, liner):
        if (len(liner) == len(liner.encode('cp932'))):
            return False
        else:
            return True
    def _is_good_word(self, liner):
        if (len(liner) == 1):
            if ((ord(liner) >= 0x4E00) and (ord(liner) < 0x9FC0)):
                return True
            else:
                return False
        return True
    def _bad_filter(self, symbols, freq, count, bad_table):
        for i in bad_table:
            try:
                zlo = symbols.index(i)
                symbols.pop(zlo)
                freq.pop(zlo)
                count -= 1
            except:
                continue
        return count
