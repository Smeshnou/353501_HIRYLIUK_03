#Task5
#Лабораторная работа №4. Работа с файлами, классами, сериализаторами,регулярными выражениями и стандартными библиотеками.
#Version: 1.0
#Dev: Гирилюк Владислав Андреевич
#Date: 05.05.2025

import numpy as np
import mynumpy as mnp

if __name__ == "__main__":
    while True:
        while True:    
            try:
                n = int(input("Input row count: "))
                if n < 0: print("Input Error. Value must be positive")
                else: break
            except ValueError:
                print("Input Error")
        while True:    
            try:
                m = int(input("Input column count: "))
                if m < 0: print("Input Error. Value must be positive")
                else: break
            except ValueError:
                print("Input Error")

        A = np.random.randint(-100, 100, size=(n, m))
        print("Matrix:")
        print(A)
        summin = np.sum(A[0])
        for str in A:
            summin = min(summin, np.sum(str))
        print("Minimum sum of row: {}".format(summin))

        print("Numpy mean {}".format(np.mean(A)))
        print("MyNumpy mean {}".format(mnp.MyNumPy.mean(A.flatten().tolist())))
        print("Numpy median {}".format(np.median(A)))
        print("MyNumpy median {}".format(mnp.MyNumPy.median(A.flatten().tolist())))
        
        print("Numpy mean {}".format(np.var(A)))
        print("MyNumpy mean {}".format(mnp.MyNumPy.var(A.flatten().tolist())))
        print("Numpy mean {}".format(np.std(A)))
        print("MyNumpy mean {}".format(mnp.MyNumPy.std(A.flatten().tolist())))
















        mask = np.array([], dtype=np.int64)
        for i in range(n):
            for j in range(m):
                mask = np.append(mask, i+j)

        
        mask = mask.reshape(n, m)
        even_elements = A[mask % 2 == 0]
        odd_elements = A[mask % 2 == 1]
        if len(even_elements) == len(odd_elements):
            correlation = np.corrcoef(even_elements, odd_elements)[0, 1]
            print("Numpy Pearson correlation coefficients {}".format(correlation))
            print("MyNumpy Pearson correlation coefficients {}".format(mnp.MyNumPy.corrcoef(even_elements, odd_elements)))
        else:
            print("Lengths of arrays is different")

        while True:    
            c = input("Repeate?[Y/N]: ").upper()
            if c != "N" and c != "Y": print("Unknown command. Retry input")
            else: break
        if c == "N": break