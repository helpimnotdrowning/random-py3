# import all math classes, this is a calculator after all
from math import *
# REPL for interactive calculator
from code import InteractiveConsole

# short helper functions to simplify typing on the REPL

def deg(x):
    ''' short for degrees()'''
    return degrees(x)
    
def rad(x):
    '''short for radians()'''
    return radians(x)
    
# sin, cos and tan in degrees
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
    
# simple 2d shapes classes

class shape:
    '''Does nothing, mainly just here for structure and making inheritence look nice'''
    pass

class circle(shape):
    '''
    Circle class to simplify working with circles.
    Params: radius
    '''
    def __init__(self, radius):
        self.radius = radius
        self.diameter = radius * 2
        
    def area(self):
        return pi * (self.radius ** 2)
        
class rectangle(shape):
    '''
    Rectangle class to simplify working with rectangles.
    Params: length and width
    '''
    def __init__(self, length, width):
        self.length = length
        self.width = width
        
    def area(self):
        return length * width
        
class square(rectangle):
    '''
    Square class to simplify working with square.
    Params: length
    '''
    def __init__(self, length):
        super().__init__(length, length)
        
def cone_volume(radius, height):
    return (1/3) * pi * (radius**2) * height

def cylinder_volume(radius, height):
    return pi * (radius**2) * height

if __name__ == '__main__':
    scope_vars = globals()
    
    # these replacements to match what the default python REPL does
    scope_vars[__name__] = '__console__'
    scope_vars[__doc__] = None
    
    InteractiveConsole(locals=scope_vars).interact('helo welcum to calculator with added stuff :)')
