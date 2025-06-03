import math

class MyNumPy:
    @staticmethod
    def array(lst):
        return lst.copy()
    
    @staticmethod
    def values(arr):
        return arr.copy()
    
    @staticmethod
    def zeros(n):
        return [0.0] * n
    
    @staticmethod
    def ones(n):
        return [1.0] * n
    
    @staticmethod
    def arange(start, stop=None, step=1):
        if stop is None:
            start, stop = 0, start
        return [float(i) for i in range(int(start), int(stop), int(step))]
    
    @staticmethod
    def get_item(arr, index):
        return arr[index]
    
    @staticmethod
    def get_slice(arr, start=None, stop=None, step=None):
        return arr[start:stop:step]
    
    @staticmethod
    def add(arr1, arr2):
        return [a + b for a, b in zip(arr1, arr2)]
    
    @staticmethod
    def subtract(arr1, arr2):
        return [a - b for a, b in zip(arr1, arr2)]
    
    @staticmethod
    def multiply(arr1, arr2):
        return [a * b for a, b in zip(arr1, arr2)]
    
    @staticmethod
    def divide(arr1, arr2):
        return [a / b for a, b in zip(arr1, arr2)]
    
    @staticmethod
    def sqrt(arr):
        return [math.sqrt(x) for x in arr]
    
    @staticmethod
    def power(arr, exponent):
        return [x**exponent for x in arr]
    
    @staticmethod
    def mean(arr):
        return sum(arr) / len(arr)
    
    @staticmethod
    def median(arr):
        sorted_arr = sorted(arr)
        n = len(sorted_arr)
        if n % 2 == 1:
            return sorted_arr[n//2]
        else:
            return (sorted_arr[n//2 - 1] + sorted_arr[n//2]) / 2
    
    @staticmethod
    def corrcoef(x, y):
        if len(x) != len(y):
            raise ValueError("Массивы должны быть одинаковой длины")
        
        n = len(x)
        mean_x = MyNumPy.mean(x)
        mean_y = MyNumPy.mean(y)
        
        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / n
        std_x = MyNumPy.std(x)
        std_y = MyNumPy.std(y)
        
        return cov / (std_x * std_y)
    
    @staticmethod
    def var(arr):
        mean = MyNumPy.mean(arr)
        return sum((x - mean) ** 2 for x in arr) / len(arr)
    
    @staticmethod
    def std(arr):
        return math.sqrt(MyNumPy.var(arr))