#! /usr/bin/env python3
import string
"""
    Occupancy class
    x: x coordinate on grid map [0, 1, 2, ..., 99]
    y: y coordinate on grid map [0, 1, 2, ..., 99]
    occupied: boolean value of the occupancy [1 = occupied, 0 = not occupied]
"""

class Ocuppancy:
    def __init__(self, x,y,occupied):
        self.x = x 
        self.y = y
        self.occupied = occupied
    
    def encode(self):
        return str.encode(f"{self.x} {self.y},{self.occupied}", "utf-8")
    
    def __str__(self):
        return f"{[{self.x},{self.y}], {self.occupied}}"
