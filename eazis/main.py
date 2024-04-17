import time

import nltk
#from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize #разбивает на отдельные слова
from nltk.stem.snowball import SnowballStemmer #убирает окончания (словоформы)
from nltk import pos_tag
from datetime import datetime
# подключаем библиотеки
import PySimpleGUI as sg
import pymorphy3

morph = pymorphy3.MorphAnalyzer(lang='ru')
concod_list: list = ['музыка','нота','ритм','такт','инструмент','гитара','фортепиано','пианино','флейта','барабан','музыкант','композитор','дирижёр','темп']

information = '''Доступные расширения для чтения:  TXT, RTF\n
Необходимо ввести путь к файлу, из которого будет считан текст, в соответствующую строку\n
Добавить - добавить морфологическую информацию выбранному слову\n
Редактировать - редактировать морфологическую информацию выбранному слову\n
Удалить - очистить морфологическую информацию выбранного слова\n
Пополнить - добавить в словарь лексему и словоформу слова\n
Обновить - обновить словарь\n
Фильтр - позволяет вывести либо весь словарь, либо только лексемы, либо только словоформы\n
Условия поиска - выводит только те слова, которые соответствуют выбранному условию\n\n
Морфологическая информация - произвольным образом оформленный пользователем текст'''


wordbook: list
wordbook1 = []
# обрабатываем нажатие на кнопку


def txt(f):
    global morph
    text = open(f,"r", encoding="utf-8").read()
    # text_elem = window['-text-']
    # выводим в него текст с новым числом
    # text_elem.update(": {}".format(text))
    nltk.download('omw-1.4')
    stemmer = SnowballStemmer("russian")
    window.FindElement('-out-').Update('')
    print(text)
    #print(sent_tokenize(text))
    text = text.replace(',','').replace(':', '').replace('-','').replace('–', '')
    start1 = datetime.now()
    text = text.replace('.', '').replace('?', '').replace('!', '')
    ending1 = datetime.now()
    # print('Нахождение предложений', ending1-start1)
    start = datetime.now()
    tokens = word_tokenize(text)
    ending = datetime.now()
    print('Нахождение слов', ending - start)
    print('Всего слов: ', len(tokens))
    # print('Разбор предложений и слов', ending1 - start1)
    lemmatized_words = [stemmer.stem(word) for word in tokens]
    global wordbook
    wordbook = [[lemmatized_words[0], 'лексема', 0, '']]
    for words in lemmatized_words:
        for i in range(len(wordbook)):
            if wordbook[i][0] == words:
                wordbook[i][2] += 1
                break
            elif wordbook[i][0] != words and i == len(wordbook) - 1:
                word1 = [words, 'лексема', 1, '']
                wordbook.append(word1)
    tokens = word_tokenize(text)
    stemmed_words = [stemmer.stem(word) for word in tokens]
    for words in stemmed_words:
        for i in range(len(wordbook)):
            if wordbook[i][0] == words and wordbook[i][1] != 'лексема':
                wordbook[i][2] += 1
                break
            elif wordbook[i][0] != words and i == len(wordbook) - 1:
                word1 = [words, 'cловоформа', 1, '']
                wordbook.append(word1)
    wordbook.sort(key=lambda x: x[0])
    i = 0
    for punkt in wordbook:
        print(i, ' - ', punkt)
        i += 1
    # tex = text.split()
    # for w in tex:
    #     pw = morph.parse(w)[0]
    #     o = pw.tag
    #     print(str(w) + ' - ' + str(o))
    # pw = morph.parse('круг')[0]
    # print(pw.tag)
    # match = tex.concordance('текст')
    # print(match)



def rtf(f):
    text = open(f, "r", encoding="utf-8-sig").read()
    # text_elem = window['-text-']
    # выводим в него текст с новым числом
    # text_elem.update(": {}".format(text))
    nltk.download('omw-1.4')
    stemmer = SnowballStemmer("russian")
    window.FindElement('-out-').Update('')
    print(text)
    text = text.replace(',','').replace(':', '').replace('-','')
    start1 = datetime.now()
    text = text.replace('.', '')
    ending1 = datetime.now()
    #print('Нахождение предложений', ending1-start1)
    start = datetime.now()
    tokens = word_tokenize(text)
    ending = datetime.now()
    print('Нахождение слов', ending - start)
    print('Всего слов: ', len(tokens))
    tokens = word_tokenize(text)
    lemmatized_words = [stemmer.stem(word) for word in tokens]
    global wordbook
    wordbook = [[lemmatized_words[0], 'лексема', 0, '']]
    for words in lemmatized_words:
        for i in range(len(wordbook)):
            if wordbook[i][0] == words:
                wordbook[i][2] += 1
                break
            elif wordbook[i][0] != words and i == len(wordbook) - 1:
                word1 = [words, 'лексема', 1, '']
                wordbook.append(word1)
    tokens = word_tokenize(text)
    stemmed_words = [stemmer.stem(word) for word in tokens]
    for words in stemmed_words:
        for i in range(len(wordbook)):
            if wordbook[i][0] == words and wordbook[i][1] != 'лексема':
                wordbook[i][2] += 1
                break
            elif wordbook[i][0] != words and i == len(wordbook) - 1:
                word1 = [words, 'cловоформа', 1, '']
                wordbook.append(word1)
    wordbook.sort(key=lambda x: x[0])
    i = 0
    for punkt in wordbook:
        print(i, ' - ', punkt)
        i += 1


def show():
    i = 0
    for punkt in wordbook:
        print(i, ' - ', punkt)
        i += 1


def add():
    global wordbook
    ADD = [[sg.Text('Введите номер слова, которому хотите добавить информацию. Диапазон: 0-'+str(len(wordbook)-1), font='Helvetica 8')], [sg.Input(key='-numb-')],
              [sg.Text('Введите информацию в произвольной форме', font='Helvetica 8')], [sg.Input(key='-info-')], [sg.Button('Сохранить', enable_events=True, key='-save-', font='Helvetica 16')]]
    adding = sg.Window('Добавить информацию', ADD, size=(450, 300))
    while True:
        event, values = adding.read()
        # если нажали на крестик
        if event in (sg.WIN_CLOSED, 'Exit'):
            # выходим из цикла
            break
        elif event == '-save-':
            if int(values['-numb-']) > -1 and int(values['-numb-'])< len(wordbook):
                wordbook[int(values['-numb-'])][3] = values['-info-']
                window.FindElement('-out-').Update('')
                show()
            else:
                err()


def err():
    error = [[sg.Text('Нет такого слова в словаре', size=(100, 40))]]
    Error = sg.Window('Ошибка', error, size=(450, 300))
    while True:
        # получаем события, произошедшие в окне
        event, values = Error.read()
        # если нажали на крестик
        if event in (sg.WIN_CLOSED, 'Exit'):
            # выходим из цикла
            break


def edit():
    global wordbook
    Edit = [[sg.Text('Введите номер слова, которому хотите редактировать информацию. Диапазон: 0-' + str(len(wordbook)-1),
                    font='Helvetica 8')], [sg.Input(key='-numb-')],
           [sg.Button('Ок', enable_events=True, key='-ok-', font='Helvetica 14')],
           [sg.Text('Старая информация:', font='Helvetica 14')], [sg.Text('', key='-old-', font='Helvetica 14')],
            [sg.Input(key='-new-')],
           [sg.Button('Сохранить', enable_events=True, key='-save-', font='Helvetica 14')]]
    editing = sg.Window('Редактировать информацию', Edit, size=(550, 300))
    while True:
        event, values = editing.read()
        # если нажали на крестик
        if event in (sg.WIN_CLOSED, 'Exit'):
            # выходим из цикла
            break
        elif event == '-ok-':
            if int(values['-numb-']) > -1 and int(values['-numb-']) < len(wordbook):
                text_elem = editing['-old-']
                text_elem.update('{}'.format(wordbook[int(values['-numb-'])][3]))
        elif event == '-save-':
            if int(values['-numb-']) > -1 and int(values['-numb-']) < len(wordbook):
                wordbook[int(values['-numb-'])][3] = values['-new-']
                window.FindElement('-out-').Update('')
                show()
            else:
                err()


def delet():
    global wordbook
    Del = [[sg.Text('Ввелите номер слова, которому хотите удалить информацию. Диапазон: 0-' + str(len(wordbook)-1), font='Helvetica 14')],
           [sg.Input(key='-numb-')],
           [sg.Button('Ок', enable_events=True, key='-ok-', font='Helvetica 16')]]
    delete = sg.Window('Удалить информацию', Del, size=(450, 300))
    while True:
        event, values = delete.read()
        # если нажали на крестик
        if event in (sg.WIN_CLOSED, 'Exit'):
            # выходим из цикла
            break
        elif event == '-ok-':
            if int(values['-numb-']) > -1 and int(values['-numb-']) < len(wordbook):
                wordbook[int(values['-numb-'])][3] = ''
                window.FindElement('-out-').Update('')
                show()
            else:
                err()


def faq():
    FAQ = [[sg.Text(information,size=(100,40))]]
    helping = sg.Window('FAQ', FAQ, size=(650, 400))
    while True:
        # получаем события, произошедшие в окне
        event, values = helping.read()
        # если нажали на крестик
        if event in (sg.WIN_CLOSED, 'Exit'):
            # выходим из цикла
            break


def filtr(f1=True, f2=True):
    global wordbook
    global wordbook1
    wordbook1.clear()
    if f1 == True and f2 == False:
        i = 0
        print('\n\n')
        for punkt in wordbook:
            if punkt[1] == 'лексема':
                wordbook1.append(punkt)
                print(i, ' - ', punkt)
                i += 1
    elif f1 == False and f2 == True:
        i = 0
        print('\n\n')
        for punkt in wordbook:
            if punkt[1] == 'cловоформа':
                wordbook1.append(punkt)
                print(i, ' - ', punkt)
                i += 1
    else:
        i = 0
        for punkt in wordbook:
            wordbook1.append(punkt)
            print(i, ' - ', punkt)
            i += 1
        window.FindElement('-out-').Update('')
        show()


def find(f=''):
    global wordbook
    global wordbook1
    wordbook1.clear()
    if f == 'Вхождения(1-3)':
        i = 0
        for punkt in wordbook:
            if punkt[2] > 0 and punkt[2] < 4:
                wordbook1.append(punkt)
                print(i, ' - ', punkt)
                i += 1
        window.FindElement('-out-').Update('')
        show()
    elif f == 'Вхождения(4+)':
        i = 0
        for punkt in wordbook:
            if punkt[2] > 3:
                wordbook1.append(punkt)
                print(i, ' - ', punkt)
                i += 1
        window.FindElement('-out-').Update('')
        show()
    elif f == 'Первая буква(А-Н)':
        i = 0
        for punkt in wordbook:
            if punkt[0][0] >= 'а' and punkt[0][0] <= 'н':
                wordbook1.append(punkt)
                print(i, ' - ', punkt)
                i += 1
        window.FindElement('-out-').Update('')
        show()
    elif f == 'Первая буква(О-Я)':
        i = 0
        for punkt in wordbook:
            if punkt[0][0] >= 'о' and punkt[0][0] <= 'я':
                wordbook1.append(punkt)
                print(i, ' - ', punkt)
                i += 1
        window.FindElement('-out-').Update('')
        show()


def sav():
    global wordbook
    f = open('wordbook.txt', "w", encoding="utf-8")
    for punkt in wordbook:
        f.write(str(punkt)+'\n')


def last():
    window.FindElement('-out-').Update('')
    text = open('wordbook.txt', "r", encoding="utf-8").read()
    print(text)

def addword():
    global wordbook
    newword = [[sg.Text('Введите слово', font='Helvetica 8')], [sg.Input(key='-w-')],
           [sg.Button('Сохранить', enable_events=True, key='-save-', font='Helvetica 16')]]
    NW = sg.Window('Пополнить', newword, size=(450, 300))
    while True:
        event, values = NW.read()
        # если нажали на крестик
        if event in (sg.WIN_CLOSED, 'Exit'):
            # выходим из цикла
            break
        elif event == '-save-':
            nltk.download('omw-1.4')
            stemmer = SnowballStemmer("russian")
            tokens = word_tokenize(str(values['-w-']))
            lemmatized_words = [stemmer.stem(word) for word in tokens]
            wordbook.append([lemmatized_words[0], 'лексема', 1, ''])
            stemmed_words = [stemmer.stem(word) for word in tokens]
            wordbook.append([stemmed_words[0], 'cловоформа', 1, ''])
            wordbook.sort(key=lambda x: x[0])
            window.FindElement('-out-').Update('')
            show()


def concor():
    global morph
    cont = [[sg.Text('Введите слово', font='Helvetica 8')], [sg.Input(key='-w-')],
            [sg.Text('Введите число симоволов контекста', font='Helvetica 8')], [sg.Input(key='-ls-')],
            [sg.Text('Введите число нахождений вхождений', font='Helvetica 8')], [sg.Input(key='-ll-')],
            [sg.Button('Ввод', enable_events=True, key='-inp-', font='Helvetica 8')]]
    concr = sg.Window('Конкордансные списки', cont, size=(450, 300))
    while True:
        event, values = concr.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            # выходим из цикла
            break
        elif event == '-inp-':
            listw = []
            nltk.download('omw-1.4')
            stemmer = SnowballStemmer("russian")
            window.FindElement('-out-').Update('')
            i = 1
            j = 1
            start = datetime.now()
            while len(listw) < int(values['-ll-']) and j < 10:
                while j <= 10:
                    file = str(j)+".txt"
                    text = open(file, "r", encoding="utf-8").read()
                    #cent = sent_tokenize(text)
                    while not text == '':
                        ind = text.find(values['-w-'])
                        word = ''



                        stri=''
                        if ind != -1:



                            ind1 = ind
                            if values['-w-'].find(' ') == -1:
                                while not text[ind1] == ' ':
                                    word = word + text[ind1]
                                    ind1 += 1
                                word = word.replace(',', '').replace('.', '').replace('!', '').replace('?', '')
                                pw = morph.parse(word)[0]
                                pwe = str(pw.tag).replace('NOUN','им.сущ').replace('ADJF','им.прил(полное)')\
                                    .replace('ADJS','им.прил(краткое)').replace('VERB','гл(лич.ф)').replace('INFN','гл(инф)')\
                                    .replace('ADVB','начерие').replace('PRTF','прич(полное)').replace('PRTS','прич(краткое)')\
                                    .replace('GRND','деепр').replace('NUMR','числ').replace('nomn','И.п').replace('gent','Р.п')\
                                    .replace('datv','Д.п').replace('accs','В.п').replace('ablt','Т.п').replace('loct','П.п')\
                                    .replace('sing','ед.ч').replace('plur','мн.ч').replace('masc','м.р')\
                                    .replace('femn','ж.р').replace('neut','ср.р').replace('anim','одуш').replace('inan','неодуш')\
                                    .replace('Qual','качеств').replace('','')
                                mor = word + ' - ' + pwe
                            else:
                                word1 = ''
                                word2 = ''
                                ind2 = values['-w-'].find(' ')
                                for w in range(ind1, ind1+ind2):
                                    word1 += text[w]
                                for w in range(ind1+ind2+1, ind1+len(values['-w-'])):
                                    word2 += text[w]
                                word1 = word1.replace(',', '').replace('.', '').replace('!', '').replace('?', '')
                                pw1 = morph.parse(word1)[0]
                                pwe1 = str(pw1.tag).replace('NOUN','им.сущ').replace('ADJF','им.прил(полное)')\
                                    .replace('ADJS','им.прил(краткое)').replace('VERB','гл(лич.ф)').replace('INFN','гл(инф)')\
                                    .replace('ADVB','начерие').replace('PRTF','прич(полное)').replace('PRTS','прич(краткое)')\
                                    .replace('GRND','деепр').replace('NUMR','числ').replace('nomn','И.п').replace('gent','Р.п')\
                                    .replace('datv','Д.п').replace('accs','В.п').replace('ablt','Т.п').replace('loct','П.п')\
                                    .replace('sing','ед.ч').replace('plur','мн.ч').replace('masc','м.р')\
                                    .replace('femn','ж.р').replace('neut','ср.р').replace('anim','одуш').replace('inan','неодуш')\
                                    .replace('Qual','качеств').replace('','')
                                mor1 = word1 + ' - ' + pwe1
                                word2 = word2.replace(',', '').replace('.', '').replace('!', '').replace('?', '')
                                pw2 = morph.parse(word2)[0]
                                pwe2 = str(pw2.tag).replace('NOUN','им.сущ').replace('ADJF','им.прил(полное)')\
                                    .replace('ADJS','им.прил(краткое)').replace('VERB','гл(лич.ф)').replace('INFN','гл(инф)')\
                                    .replace('ADVB','начерие').replace('PRTF','прич(полное)').replace('PRTS','прич(краткое)')\
                                    .replace('GRND','деепр').replace('NUMR','числ').replace('nomn','И.п').replace('gent','Р.п')\
                                    .replace('datv','Д.п').replace('accs','В.п').replace('ablt','Т.п').replace('loct','П.п')\
                                    .replace('sing','ед.ч').replace('plur','мн.ч').replace('masc','м.р')\
                                    .replace('femn','ж.р').replace('neut','ср.р').replace('anim','одуш').replace('inan','неодуш')\
                                    .replace('Qual','качеств').replace('','')
                                mor2 = word2 + ' - ' + pwe2



                            if ind-int(values['-ls-'])>=0:
                                if not ind+len(str(values['-w-']))+int(values['-ls-'])>=len(text):
                                    for s in range (ind-int(values['-ls-']), ind+len(str(values['-w-']))+int(values['-ls-'])):
                                        stri += text[s]
                                else:
                                    for s in range(ind - int(values['-ls-']), len(text)):
                                        stri += text[s]
                            elif ind-int(values['-ls-'])<0:
                                if not ind + len(str(values['-w-'])) + int(values['-ls-']) >= len(text):
                                    for s in range(0, ind + len(str(values['-w-'])) + int(values['-ls-'])):
                                        stri += text[s]
                                else:
                                    for s in text:
                                        stri += text[s]
                            if values['-w-'].find(' ') == -1:
                                addw = stri + '\n' + str(mor)
                            else:
                                addw = stri + '\n' + str(mor1) + '\n' + str(mor2)

                            listw.append(addw)
                            cut = ind + len(str(values['-w-'])) + int(values['-ls-'])
                            text = text[cut:]
                        else:
                            text=''
                    j += 1


            end = datetime.now()
            window.FindElement('-out-').Update('')
            f = open('concor.txt', "w", encoding="utf-8" )
            print('Время: ' + str(end-start))
            if len(listw) >= int(values['-ll-']):
                for i in range(0, int(values['-ll-'])):
                    f.write(str(i + 1) + "." + listw[i] + '\n')
                    print(str(i+1)+ "." + listw[i])

            else:
                print("Вхождений во всех текстах меньше введённого")
                f.write("Вхождений во всех текстах меньше введённого" + '\n')
                for i in range(0, len(listw)):
                    f.write(str(i + 1) + "." + listw[i] + '\n')
                    print(str(i+1)+ "." + listw[i])





# что будет внутри окна
# первым описываем кнопку и сразу указываем размер шрифта
layout = [[sg.Button('Считать txt', enable_events=True, key='-read1-', font='Helvetica 14'), sg.Input(key='-input1-'),
           sg.Push(), sg.Button(' ? ', enable_events=True, key='-faq-', font='Helvetica 14')],
        [sg.Button('Считать rtf', enable_events=True, key='-read2-', font='Helvetica 14'), sg.Input(key='-input2-')],
        [sg.Button('Добавить', enable_events=True, key='-add-', font='Helvetica 14'),
        sg.Button('Редактировать', enable_events=True, key='-edit-', font='Helvetica 14'),
        sg.Button('Удалить', enable_events=True, key='-del-', font='Helvetica 14'),
         sg.Button('Пополнить', enable_events=True, key='-addword-', font='Helvetica 14')],
          [sg.Button('Фильтр', enable_events=True, key='-filtr-', font='Helvetica 14'),
           sg.Checkbox('Лексемы', default=True, key='f1'), sg.Checkbox('Словоформы', default=True, key='f2')],
          [sg.Text('Условие', font='Helvetica 14'),
           sg.InputCombo(('Вхождения(1-3)','Вхождения(4+)','Первая буква(А-Н)','Первая буква(О-Я)'), key='var'),
           sg.Button('Поиск', enable_events=True, key='-find-', font='Helvetica 14')],
          [sg.Button('Предыдущий', enable_events=True, key='-last-', font='Helvetica 14'),
            sg.Button('Контекст', enable_events=True, key='-concr-', font='Helvetica 14'),
           sg.Push(), sg.Button('Сохранить', enable_events=True, key='-sav-', font='Helvetica 14')],
          [sg.Output(size=(100, 40),key='-out-')]]

# рисуем окно
window = sg.Window('Лабораторная №1', layout, size=(750, 600))
nltk.download('omw-1.4')
# запускаем основной бесконечный цикл
while True:
     # получаем события, произошедшие в окне
    event, values = window.read()
     # если нажали на крестик
    if event in (sg.WIN_CLOSED, 'Exit'):
        # выходим из цикла
        break
    # если нажали на кнопку
    if event == '-read1-':
        # запускаем связанную функцию
        txt(values['-input1-'])
        # show()
    elif event == '-read2-':
        rtf(values['-input2-'])
    elif event == '-add-':
        add()
    elif event == '-edit-':
        edit()
    elif event == '-del-':
        delet()
    elif event == '-faq-':
        faq()
    elif event == '-filtr-':
        filtr(window['f1'].get(), window['f2'].get())
    elif event == '-find-':
        find(window['var'].get())
    elif event == '-last-':
        last()
    elif event == '-sav-':
        sav()
    elif event == '-addword-':
        addword()
    elif event == '-concr-':
        concor()
#
# # закрываем окно и освобождаем используемые ресурсы
# window.close()





