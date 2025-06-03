import shape
import shapecolor
import saveable

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np

class Trapezium(shape.Shape, saveable.SaveableMixin):
    def __init__(self, a_side, b_side, height, color, name = "Trapizium"):
        self.a_side = a_side
        self.b_side = b_side
        self.height = height
        self.color = shapecolor.ShapeColor(color)
        self.__name = name

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value):
        self.__name = value
    
    def area(self):
        super().area()
        return (self.a_side+self.b_side) / 2 * self.height
    
    def __format__(self):
        return "{} {} {} {} {} {}".format(self.__name, self.a_side, self.b_side, self.height, self.color, self.area())
    
    def draw(self, savefile = ""):
        offset = (self.a_side - self.b_side) / 2
        
        vertices = np.array([
            [0, 0],
            [self.a_side, 0],
            [self.a_side - offset, self.height],
            [offset, self.height]
        ])
        
        fig, ax = plt.subplots()
        
        trapezium = Polygon(vertices, closed=True, facecolor=self.color.color, edgecolor='black')
        ax.add_patch(trapezium)
        
        ax.set_xlim(-0.5, self.a_side + 0.5)
        ax.set_ylim(-0.5, self.height + 0.5)
        
        ax.set_title(f'{self.__name}\na={self.a_side}, b={self.b_side}, h={self.height}')
        super().draw(savefile)
