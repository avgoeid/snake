from os import system
from enum import Enum
from time import sleep
from msvcrt import getch, kbhit

from colorama import init


init()

class Directions(Enum):
    
    top = b'w'
    right = b'd'
    bottom = b's'
    left = b'a'

class Point:
    
    def __init__(self, *args):
        args_len = len(args)
        if args_len == 1:
            self.x, self.y, self.symbol = args[0].x, args[0].y, args[0].symbol
        elif args_len == 3:
            self.x, self.y, self.symbol = args
        else:
            message = 'Must be Point argument or x, y, symbol : {}'.format(args)
            raise ValueError(message)
    
    def move(self, offset, direction):
        if direction == Directions.top:
            self.y -= offset
        elif direction == Directions.bottom:
            self.y += offset
        elif direction == Directions.left:
            self.x -= offset
        elif direction == Directions.right:
            self.x += offset
        return self
    
    def draw(self):
        print('\033[{};{}H{}'.format(self.y, self.x, self.symbol))
    
    def clear(self):
        self.symbol = ' '
        self.draw()

    def __repr__(self):
        return 'Point({}, {}, {})'.format(self.x, self.y, self.symbol)

class Figure:
    
    def __init__(self):
        self.points = list()
    
    def draw(self):
        [point.draw() for point in self.points]    

class VerticalalLine(Figure):
    
    def __init__(self, x, y_bottom, y_top, symbol):
        self.points = [Point(x, y, symbol) for y in range(y_bottom, y_top + 1)]
        
class HorizontalLine(Figure):
    
    def __init__(self, x_left, x_right, y, symbol):
        self.points = [Point(x, y, symbol) for x in range(x_left, x_right + 1)]

class Area(Figure):
    
    def __init__(self, left_top_x, left_top_y, right_bottom_x, right_bottom_y, symbol):
        top = HorizontalLine(left_top_x, right_bottom_x, left_top_y, symbol)
        bottom = HorizontalLine(left_top_x, right_bottom_x, right_bottom_y, symbol)
        left = VerticalalLine(left_top_x, left_top_y + 1, right_bottom_y - 1, symbol)
        right = VerticalalLine(right_bottom_x, left_top_y + 1, right_bottom_y - 1, symbol)
        self.points = top.points + left.points + bottom.points + right.points

class Snake(Figure):

    def __init__(self, tail, length, direction):
        super().__init__()
        self.direction = direction
        for i in range(length):
            self.points.append(Point(tail).move(i, self.direction))
    
    def move(self):
        tail = self.points.pop(0)
        head = self.get_next_point()
        self.points.append(head)
        tail.clear()
        head.draw()
    
    def get_next_point(self):
        return Point(self.points[-1]).move(1, self.direction)
        
        
    
def set_console_size(cols, lines):
    system('mode con: cols={} lines={}'.format(cols, lines))                

    
if __name__ == '__main__':
    set_console_size(80, 40)
    Area(1, 1, 80, 38, '#').draw()
    s1 = Snake(Point(5, 6, '@'), 7, Directions.right)
    s1.draw()
    '''for _ in range(10):
        s1.move()
        sleep(0.3)
    '''
    while(True):
        if kbhit():
            key = getch()
            if key == Directions.top.value:
                s1.direction = Directions.top
            elif key == Directions.right.value:
                s1.direction = Directions.right
            elif key == Directions.bottom.value:
                s1.direction = Directions.bottom
            elif key == Directions.left.value:
                s1.direction = Directions.left
        sleep(0.3)
        s1.move()
    #input()
