import numpy as np

def func(var):
    return var ** 2

def funk(size):
    return np.random.random(size=size)

def defunc():
    return "Yeah, no."

class Person:
    def __init__(self, name):
        self.name = name
        
    def say_hi(self):
        return f"Hi, {self.name}!"
    
    def secret_name(self):
        return self.name[::-1]