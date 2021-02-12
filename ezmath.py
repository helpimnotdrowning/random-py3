from math import *
import traceback
import inspect

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
    
class shape:
    pass

class circle(shape):
    def __init__(self, radius):
        self.radius = radius
        self.diameter = radius * 2
        
    def area(self):
        return pi * (self.radius ** 2)
        
class rectangle(shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width
        
    def area(self):
        return length * width

class square(rectangle):
    def __init__(self, length):
        super().__init__(length, length)

def cone_volume(radius, height):
    return (1/3) * pi * (radius**2) * height

def cylinder_volume(radius, height):
    return pi * (radius**2) * height

def Convert(tup, di): 
    for a, b in tup: 
        di.setdefault(a, []).append(b) 
    return di 
      
# Driver Code     
tups = ''
dictionary = {} 
print (Convert(tups, dictionary)) 


from code import InteractiveConsole

if __name__ == '__main__':
    print('helo welcum to calculator with added stuff :)')
    print('this prints the result of anything you put in, including the None returned by print()')

    while True:
        # header = "Welcome to REPL! We hope you enjoy your stay!"
        # footer = "Thanks for visiting the REPL today!"
        # scope_vars = {"answer": 42}
        # InteractiveConsole(locals=scope_vars).interact(header, footer)
        
        eval_math = input('> ')
        try:
            print(exec(eval_math))
        except Exception as e: 
            traceback.print_exc()
