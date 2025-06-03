#Task2
#Лабораторная работа №4. Работа с файлами, классами, сериализаторами,регулярными выражениями и стандартными библиотеками.
#Version: 1.0
#Dev: Гирилюк Владислав Андреевич
#Date: 04.05.2025

import os
import re
from collections import Counter
from zipfile import ZipFile

if __name__ == "__main__":
    filename = "Task2/text.txt" 
    zipfile = "Task2/zipfile.txt"
    resultfile = "Task2/resultfile.txt"
    with open(filename, "r", encoding = "utf-8") as fl:
        text = fl.read()
    
    mails = re.findall(r"\w(?:\w|-)+@\w+\.\w+", text)
    print(mails)

    addressee = [s[6:] for s in re.findall(r"кому: [^\n]+", text)]
    print(addressee)

    newtext = re.sub(r'\$v_\(((?:(?!_)\w))\)\$', r'v[\1]', text)
    print(newtext)

    words = [s for s in re.findall(r'\b[a-zа-я]+\b', text, flags = re.RegexFlag.I) if len(s) % 2 == 1]
    print(words)
    
    iwords = re.findall(r'\bi[a-zа-я]+', text, flags = re.RegexFlag.I)
    min = None
    if iwords:
        min = iwords[0]
        for w in iwords:
            if len(min) > len(w):
                min = w
    print(min) 

    dwords = Counter(re.findall(r'\b[a-zа-я]+\b', text, flags = re.RegexFlag.I))
    duplicates = [word for word, count in dwords.items() if count > 1]
    print("Повторяющиеся слова:", duplicates)

    with open(zipfile, "w", encoding = "utf-8") as fl:
        fl.write("Emails:\n")
        for m in mails:
            fl.write(m + "\n")
        
        fl.write("Addressees:\n")
        for a in addressee:
            fl.write(a + "\n")

        fl.write("New text:\n")
        fl.write(newtext + "\n")

        fl.write("Words:\n")
        for w in words:
            fl.write(w + "\n")

        fl.write("Iword:\n")
        fl.write(min + "\n")

        fl.write("Duplicate words:\n")
        for w in duplicates:
            fl.write(w + "\n")

    os.chdir('Task2')
    with ZipFile("Task2.zip", "w") as myzip:
        myzip.write("zipfile.txt")
        info = myzip.getinfo("zipfile.txt")
        print(info)
    os.chdir('..')



    dot = len(re.findall(r"\S\.\s", text))
    ep = len(re.findall(r"\S\!\s", text))
    qm = len(re.findall(r"\S\?\s", text))

    sen = [s for s  in re.split(r"(\.|\!|\?)\s", text) if s != "." and s != "!" and s != "?"]
    length = 0.
    count_word = 0
    for s in sen:
        for w in re.findall(r'\b[a-zа-я]+\b', s, flags = re.RegexFlag.I):
            count_word = count_word + 1
            length = length + len(w)
    avgsen = length / len(sen)
    avgword = length / count_word

    smile_count = len(re.findall(r'(?:\:|\;)\-*(?:\(|\)|\[|\])+', text))

    with open(resultfile, "w", encoding = "utf-8") as fl:
        fl.write("Количество предложений: {}\n" \
        "Повествовательных: {}\n" \
        "Побудительных: {}\n" \
        "Вопросительных: {}\n".format(dot+ep+qm, dot, ep, qm)) 
        fl.write("Средняя длина предложений: {}\n" \
        "Средняя длина слов: {}\n" \
        "Количество смайликов: {}\n".format(avgsen, avgword, smile_count)) 