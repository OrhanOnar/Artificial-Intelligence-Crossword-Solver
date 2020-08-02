import Tkinter
import json
import re
import string
import random
import time
import sys
from Tkinter import *
import Pmw, sys
import PySimpleGUI27 as sg



boyut = [[sg.Text('Boyut Seciniz')],         #GUI
         [sg.Text('Row Sayisi', size=(15, 1)), sg.InputText(size=(15,1)), ],
         [sg.Text('Col Sayisi', size=(15, 1)), sg.InputText(size=(15,1)), ],
         [sg.Submit('BULMACA OLUSTUR')]]

window2 = sg.Window('Boyut Belirle', boyut)

event, values = window2.read()

en = int(values[0])
boy = int(values[1])

header = [[sg.Text('Harf Girilmesini Istemediginiz\nKutucuklara "*" Karakterini Giriniz')], #GUI
    [sg.Button('OLUSTURULAN BULMACAYI COZ')]]

input_rows = [[sg.Input(size=(4, 4), pad=(0, 0)) for col in range(en)] for row in range(boy)]

layout = input_rows + header

window = sg.Window('KARE BULMACA', layout, font='Courier 12')
event, values = window.read()

satiratla = 0
basayaz = str(en) + ' ' + str(boy) + '\n'
yazilacak = '?'

dosyaismi = str(boy) + str(en) + '.txt'
print dosyaismi

with open(dosyaismi, 'w') as f:  #Dosya oku
    f.writelines(basayaz)
    for say in range(en * boy):
        satiratla = satiratla + 1
        s = values[say]
        if s == '':
            yazilacak = '?'
        elif s == '*':
            yazilacak = '*'

        if satiratla == en:
            print >> f, yazilacak
            satiratla = 0
        else:
            f.writelines(yazilacak)














def ciktiVer():  #terminale basma metodu
    data = [["  " for x in range(width)] for x in range(height)]

    for word in yatayKelimeler:
        for letter in range(word[2]):
            data[word[0]].pop(word[1] + letter)
            data[word[0]].insert(word[1] + letter, "[]")

    for word in dikeyKelimeler:
        for letter in range(word[2]):
            data[word[0] + letter].pop(word[1])
            data[word[0] + letter].insert(word[1], "[]")

    for word in words:
        if word[0] == 'a':
            x = yatayKelimeler[word[1]][0]
            y = yatayKelimeler[word[1]][1]
            for num, letter in enumerate(word[2]):
                data[x].pop(y + num)
                data[x].insert(y + num, letter.upper() + ' ')
        if word[0] == 'd':
            x = dikeyKelimeler[word[1]][0]
            y = dikeyKelimeler[word[1]][1]
            for num, letter in enumerate(word[2]):
                data[x + num].pop(y)
                data[x + num].insert(y, letter.upper() + ' ')

    print '  ',
    for i in range(width):
        if i + 1 < 10:
            print i + 1, '',
        else:
            print i + 1,
    print
    for i in range(height):
        if i + 1 < 10:
            print '', i + 1,
        else:
            print i + 1,
        for col in data[i]:
            print col,
        print




def SatirSutun(rows):   #Satir ve Sutuna 1 2 3 4 ... seklinde yazar
    cols = []
    for i in range(len(rows[0])):
        cols.append("")
    for row in rows:
        for col, char in enumerate(row):
            cols[col] += char
    return cols




def TahtayiOku(rows):   #kullanicinin girdigi TABLOYU OKUR WORD arrayine KAYDEDER
    words = []
    for num, row in enumerate(rows):
        nextWordIndex = row.find('?')
        while nextWordIndex != -1:
            try:
                nextWordEnd = row.index('*', nextWordIndex)

            except ValueError:
                nextWordEnd = len(row)
            length = nextWordEnd - nextWordIndex
            if length > 1:
                words.append([num, nextWordIndex, length])
            nextWordIndex = row.find('?', nextWordEnd)
    return words






def eslestir(cols, it=0):  # kisitlari saglayan kelime return eder
    it = 0
    if cols[0] == 1: #uzunluk 1 ise direk True return et
        return True
    reg = []
    for i in range(cols[0]):   #
        reg.append('\w')
    length = cols.pop(0)  #cols lenghtini bulur daha verimli cols.length kullanabilirdik
    for item in cols:  #hepsini 1 sola kaydir
        reg[item[0]] = item[1]      #hepsini 1 sola kaydir
    while it < len(dict[length]):
        rand = random.randrange(0, len(dict[length]))  # uyan kelimelerden birisini rasgele verebilirsin hepsi sartlari sagliyor
        word = re.match(''.join(reg), dict[length][rand], re.U | re.I) #re.U unicode matching, re.I IgnoreCase ,eslestir
        if word:
            return [word.group(0), rand]  #word group(0) uyanlarin hepsi demek, onlarin isinden rasgele birisini returnh et
        it += 1
    return False








def ConstraintsBul(pointer):   # BULMACANIN siyah NOKTALARINA D verir BEYAZ NOKTALARINA A VERIR
    ori, index = pointer[0], pointer[1]
    constraints = []
    if ori == 'a':
        constraints.append(yatayKelimeler[index][2])
        for lap in kesisenKelimeler:
            if lap[0] == index:
                hpos = lap[1]
                vind = lap[2]
                vpos = lap[3]
                for word in words:
                    if word[0] == 'd' and word[1] == vind:
                        constraints.append([hpos, word[2][vpos]])  #dikeyin yatay ile kesisme durumu
                        break
    elif ori == 'd':
        constraints.append(dikeyKelimeler[index][2])
        for lap in kesisenKelimeler:
            if lap[2] == index:
                hind = lap[0]
                hpos = lap[1]
                vpos = lap[3]
                for word in words:
                    if word[0] == 'a' and word[1] == hind:
                        constraints.append([vpos, word[2][hpos]]) #dikeyin yatayla kesisme durumu
                        break
    return constraints





def bulmacaCoz(init=0, offset=False):
    myOrder = order[:]
    delOrder = []
    delWords = {}
    while len(myOrder) > 0:
        if offset:
            prev = words.pop()
            kelime = eslestir(ConstraintsBul(myOrder[0]), prev[3] + 1) # prev[3] kelime tutulan yer,offset varsa  offsetten sonraki kelimeye gec ordan basla
            offset = False
        elif not vars().has_key('new'):
            new = True
            kelime = eslestir(ConstraintsBul(myOrder[0]), init)  #init durumu icin constaints check et
        else:
            if delWords.has_key((myOrder[0][0], myOrder[0][1])):  #kelime eslesmeyenler listesindeyse
                kelime = eslestir(ConstraintsBul(myOrder[0]), delWords[(myOrder[0][0], myOrder[0][1])] + 1)  #bir daha dene +1 offsetli
            else:
                kelime = eslestir(ConstraintsBul(myOrder[0])) # tekrar kelime bul
        if kelime == False:  #olmuyorsa pointeri ileri tasi yeni kelime gerekiyor
            pointer = 0
            const = myOrder[pointer]
            while kelime == False:  #uygun kelime bulunana kadar
                try:
                    move = words.pop()
                except IndexError:
                    continue
                delWords[(move[0], move[1])] = move[3]
                for tup in delOrder:
                    if tup[0] == move[0] and tup[1] == move[1]:
                        myOrder.append(tup)
                        break
                    if delWords.has_key((myOrder[0][0], myOrder[0][1])):  #kelime olmuyorsa
                        kelime = eslestir(ConstraintsBul(myOrder[0]), delWords[(myOrder[0][0], myOrder[0][1])] + 1) #tekar eslestir cagir
                    else:
                        kelime = eslestir(ConstraintsBul(myOrder[0]))        # tekrar kelime bul
            words.append([myOrder[pointer][0], myOrder[pointer][1], kelime[0], kelime[1]])  # bulunan kelimeyi ekle
            delOrder.append(myOrder.pop(pointer))  #eklenen kelimeyi delOrder'a ekle
            if disp:
                ciktiVer()
            continue
        words.append([myOrder[0][0], myOrder[0][1], kelime[0], kelime[1]]) # aramaya gerek kalmadan kelime bulundu, ekle
        delOrder.append(myOrder.pop(0))   # eklenen kelimeyi delOrder'a ekle
        if disp:
            ciktiVer()






ekrana = False
dict = []
f = open('words.json')
dict = json.load(f)
print'Sozluk Basariyla Okundu'
while True:
    read = False
    while read == False:
        try:
            file = open(dosyaismi, 'r')
            rows = file.read().splitlines()
            file.close()
            width = int(rows[0].split(" ")[0])
            height = int(rows[0].split(" ")[1])
            del rows[0]
        except IOError:
            print 'Dosya Okumasi Basarisiz Oldu.'
            continue
        else:
            read = True

    yatayKelimeler = TahtayiOku(rows)
    cols = SatirSutun(rows)
    dikeyKelimeler = TahtayiOku(cols)
    for elem in dikeyKelimeler:
        elem[0], elem[1] = elem[1], elem[0]  # sol ust 0 0 olsun diye

    kesisenKelimeler = []
    for hindex, htuple in enumerate(yatayKelimeler):
        for hpos in range(htuple[2]):
            for vindex, vtuple in enumerate(dikeyKelimeler):
                for vpos in range(vtuple[2]):
                    if htuple[0] == vtuple[0] + vpos and htuple[1] + hpos == vtuple[1]:
                        kesisenKelimeler.append([hindex, hpos, vindex, vpos]) #kesisen kelime bulundu

    words = []
    ciktiVer()

    read = False
    while read == False:
        try:
            file = open('answers.txt', 'w')
        except IOError:
            print 'Dosya okumasi Basarisiz'
            continue
        else:
            read = True
    disp = False

    sols = 0
    t = 0
    order = []
    order1 = []
    order2 = []
    for i in range(len(yatayKelimeler)):
        order1.append(['a', i])
    for i in range(len(dikeyKelimeler)):
        order2.append(['d', i])
    order = []
    while True:
        try:
            order.append(order1.pop(0))
            order.append(order2.pop(0))
        except IndexError:
            break
    if len(order1) > 0:
        order.extend(order1)  #uyan yatay kelimeleri ekle
    if len(order2) > 0:
        order.extend(order2)  #uyan dikey kelimeleri ekle
    for init in range(5):   #100 cozum yeterli
        sols = sols + 1
        print  'Cozum', sols
        temp = time.time()
        bulmacaCoz()
        t += time.time() - temp
        sys.stdout = file
        print 'Cozum', sols
        ciktiVer()
        sys.stdout = sys.__stdout__
        file.flush()
        ciktiVer()
        if t > 15: #15 saniye arama yeterli
            break
    print t
    sys.stdout = file
    print t
    sys.stdout = sys.__stdout__

    file.close()

    filename = 'answers.txt'            #sonuclari GUI ile ekrana bas
    root = Tk()
    top = Frame(root);
    top.pack(side='top')
    text = Pmw.ScrolledText(top,
                            borderframe=5,
                            vscrollmode='dynamic',
                            hscrollmode='dynamic',
                            labelpos='n',
                            label_text='file %s' % filename,
                            text_width=60,
                            text_height=en+2,
                            text_wrap='none',
                            )
    text.pack()

    text.insert('end', open(filename, 'r').read())
    Button(top, text='Quit', command=root.destroy).pack(pady=15)
    root.mainloop()



