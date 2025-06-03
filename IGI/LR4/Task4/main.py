#Task4
#Лабораторная работа №4. Работа с файлами, классами, сериализаторами,регулярными выражениями и стандартными библиотеками.
#Version: 1.0
#Dev: Гирилюк Владислав Андреевич
#Date: 05.05.2025

from matplotlib.colors import CSS4_COLORS
import trapezium
import re

if __name__ == "__main__":
     file = "Task4/shape.png"
     while True:
        print("Create Trapezium process")
        while True:    
            try:
                a = float(input("Input A side: "))
                if a < 0: print("Input Error. Value must be positive")
                else: break
            except ValueError:
                print("Input Error")
        while True:    
            try:
                b = float(input("Input B side: "))
                if b < 0 and b >= a: print("Input Error. Value must be positive and less than A side")
                else: break
            except ValueError:
                print("Input Error")
        while True:    
            try:
                h = float(input("Input height: "))
                if b < 0: print("Input Error. Value must be positive")
                else: break
            except ValueError:
                print("Input Error")

        while True:
            color = input("Input color (Examples: 'red', 'blue', '#FF00FF'): ").strip()
            
            if color.lower() in CSS4_COLORS:
                color = color.lower()
                break
            
            if re.match(r'^#[0-9a-f]{6}$', color, flags = re.RegexFlag.I):
                break
            
            print("Incorrecr color! Retry.")        
        name = input("Input name of shape: ")

        shape = trapezium.Trapezium(a, b, h, color, name)
        shape.draw(file)

        while True:    
            c = input("Repeate?[Y/N]: ").upper()
            if c != "N" and c != "Y": print("Unknown command. Retry input")
            else: break
        if c == "N": break