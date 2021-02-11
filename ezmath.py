from math import *
import traceback

# short helper functions to simplify typing on the REPL

def deg(x):
    ''' short for degrees()'''
    return degrees(x)
    
def rad(x):
    '''short for radians()'''
    return radians(x)
    
# sin, cos and tan n degrees
# this is because the python.math module works in radians EXCLUSIVELY
# add degree mode pls


def dsin(x):
    '''sin(), but degrees (input and output)'''
    return sin(rad(x))
    
def dcos(x):
    '''cos(), but degrees (input and output)'''
    return cos(rad(x))
    
def dtan(x):
    '''tan(), but degrees (input and output)'''
    return tan(rad(x))
    
# same as above, just for arc/inverted functions

def dasin(x):
    '''asin(), but degrees (input and output)'''
    return deg(asin(x))
    
def dacos(x):
    '''acos(), but degrees (input and output)'''
    return deg(acos(x))
    
def datan(x):
    '''atan(), but degrees (input and output)'''
    return deg(atan(x))
    
# class shape:
    # def __init__(self

class circle:
    def __init__(self, radius):
        self.radius = radius
        self.diameter = radius * 2
        
    def area(self):
        return pi * (self.radius ** 2)
        
    def set_radius(self, radius):
        self.__init__(radius)
        
    def set_diameter(self, diameter):
        self.__init__(diameter / 2)
        
# class rectangle:
    # def

def cone_volume(radius, height):
    return (1/3) * pi * (radius**2) * height

def cylinder_volume(radius, height):
    return pi * (radius**2) * height

if __name__ == '__main__':
    print('helo welcum to calculator with added stuff :)')

    while True:
        eval_math = input('> ')
        try:
            exec(eval_math)
        except Exception as e: 
            traceback.print_exc()
