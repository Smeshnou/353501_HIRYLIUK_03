#Task1
#Лабораторная работа №4. Работа с файлами, классами, сериализаторами,регулярными выражениями и стандартными библиотеками.
#Version: 1.0
#Dev: Гирилюк Владислав Андреевич
#Date: 04.05.2025

import pickle
import csv
import book


def search(author, library):
    if author in library:
        for book in library[author]:
            print("Название: {}\nГод издания: {}".format(book.name, book.year))
    else:
        print("Неверно введена фамилия автора или книг данного автора нет в нашей библиотеке")

if __name__ == "__main__":
    
    filename = "Task1/library.txt"
    csvfile = "Task1/library.csv"
    library = {"лермонтов": [book.Book("Герой нашего времени", 1839), book.Book("Смерть поэта", 1837), book.Book("Мцыри", 1839)], 
            "толстой": [book.Book("Война и мир", 1867), book.Book("Анна Каренина", 1877), book.Book("Смерть Ивана Ильича", 1866)]}
    
    with open(csvfile, "w", encoding = "utf-8", newline = "") as fl:
        writer = csv.writer(fl, quoting=csv.QUOTE_ALL)
        for author, books in library.items():
            for abook in books:
                writer.writerow([author, abook.name, abook.year])

    with open(filename, "wb") as fl:
        pickle.dump(library, fl)

    while True:
        while True:    
            try:
                fileformat = int(input("Выберите формат файла(вводить число):\n1.txt\n2.csv\nИли введите '0' для выхода из программы\n"))
                if fileformat < 0 or fileformat > 2:
                    print("Input Error.")
                    continue
                break
            except:
                print("Input Error")
        if fileformat == 0:
            break
        surname = input("Введите фамилию интересующего автора: ").lower()


        if fileformat == 1:
            with open(filename, "rb") as fl:
                load_library = pickle.load(fl)

        elif fileformat == 2:
            load_library = {}
            with open(csvfile, "r", encoding = "utf-8") as fl:
                reader = csv.reader(fl)
                rows = list(reader)
                for row in rows:
                    if row[0] in load_library:
                        load_library[row[0]].append(book.Book(row[1], row[2]))
                    else:
                        load_library[row[0]] = []
                        load_library[row[0]].append(book.Book(row[1], row[2]))


        else:
            print("Неверно введен формат файла")
        search(surname, load_library)