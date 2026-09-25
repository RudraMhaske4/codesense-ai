import math
import pandas as pd
class Calculator:
    def add(self, a, b):
        return a + b
    def multiply(self, a, b):
        return a * b
def calculate_square(number):
    if number >= 0:
        return number * number
    else:
        return 0
def classify_number(number):
    if number > 0:
        return "Positive"
    elif number < 0:
        return "Negative"
    else:
        return "Zero"
def calculate_circle_area(radius):
    if radius > 0:
        return math.pi * radius * radius
    return 0