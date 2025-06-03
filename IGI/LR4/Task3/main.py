#Task3
#Лабораторная работа №4. Работа с файлами, классами, сериализаторами,регулярными выражениями и стандартными библиотеками.
#Version: 1.0
#Dev: Гирилюк Владислав Андреевич
#Date: 05.05.2025

import Taylor
import numpy as np
import math
import matplotlib.pyplot as plt

if __name__ == "__main__":
    while True:
        while True:    
            try:
                x = float(input("Input x, |x|<1: "))
                if abs(x) > 1: print("Input Error. Value of 'x' from -1 to 1 not including -1 and 1")
                else: break
            except ValueError:
                print("Input Error")
        while True:    
            try:
                eps = float(input("Input eps: "))
                if eps < 0:
                    print("Input Error. Epsilon is positive")
                    continue
                break
            except:
                print("Input Error")

        T = Taylor.Taylor(x, eps)
        print("{:<10} {:<10} {:<20} {:<20} {:<10}".format("x", "n", "F(x)", "Math F(x)", "eps"))
        print("{:<10} {:<10} {:<20} {:<20} {:<10}".format(x, T.n, T.f, math.log(1 + x), eps))
        print(T)
        x = np.arange(-1+eps, 1, eps)
        y = np.array([], "float64")

        for x_i in x:
            y = np.append(y, Taylor.Taylor(x_i, eps).f)

        fig, ax = plt.subplots()

        ax.grid(True)
        ax.set_xlabel("x")
        ax.set_ylabel("F(x)")
        ax.set_title("Taylor")
        ax.plot(x, y, "r", linewidth = 3, label = "Taylor")
        ax.text(-1, 0, "График приближенного вычисления\nс помощью ряда Тейлора\nс точностью eps = {}".format(eps))
        ax.annotate("Точка (0, 0)", xy = (0, 0), xytext = (0.1, -1), arrowprops = dict(facecolor = "black", shrink = 0.05))
        ax.plot(x, np.log(1 + x), "b", linewidth = 3, label = "log(1+x)")
        ax.legend()

        plt.savefig("Task3/my_image.png")
        plt.show()



        while True:    
            c = input("Repeate?[Y/N]: ").upper()
            if c != "N" and c != "Y": print("Unknown command. Retry input")
            else: break
        if c == "N": break