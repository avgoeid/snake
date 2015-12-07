from os import system
from enum import Enum
from time import sleep
from msvcrt import getch, kbhit
from random import randint, choice

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
    
    def is_hit(self, point):
        return self.x == point.x and self.y == point.y
    
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

    def is_hit(self, snake):
        snake_head = snake.get_next_point()
        for point in self.points:
            if snake_head.is_hit(point):
                return True
        else:
            return False

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
    
    def eat(self, food):
        head = self.get_next_point()
        if head.is_hit(food):
            food.symbol = head.symbol
            food.draw()
            self.points.insert(0, food)
            return True
        else:
            return False

    def is_hit_tail(self):
        head = self.get_next_point()
        for point in self.points:
            if head.is_hit(point):
                return True
        else:
            return False
        
    def handle_key(self, key):    
        if key == Directions.top.value:
            self.direction = Directions.top
        elif key == Directions.right.value:
            self.direction = Directions.right
        elif key == Directions.bottom.value:
            self.direction = Directions.bottom
        elif key == Directions.left.value:
            self.direction = Directions.left
    
class FoodCreator:
    
    def __init__(self, area_width, area_height, symbol):
        self.area_width = area_width
        self.area_height = area_height
        self.symbol = symbol
    
    def create_food(self):
        x = randint(3, self.area_width - 3)
        y = randint(3, self.area_height - 3)
        return Point(x, y, self.symbol)
    
def make_game(cols=80, lines=40):

    def game_over(text):
        pass
    
    # set console size
    system('mode con: cols={} lines={}'.format(cols, lines))

    area = Area(1, 1, cols, lines - 2, '#')
    foor_creator = FoodCreator(cols, lines, '$')
    food = foor_creator.create_food()
    snake_head = Point(randint(5, cols - 4), randint(5, lines - 4), '*')
    snake = Snake(snake_head, 3, choice((Directions.top, Directions.right, Directions.bottom, Directions.left)))
    [i.draw() for i in (area, food, snake)]

    while(True):
        # check key press
        if kbhit():
            snake.handle_key(getch())
        if area.is_hit(snake) or snake.is_hit_tail():
            break
        if snake.eat(food):
            food = foor_creator.create_food()
            food.draw()
        sleep(0.2)
        snake.move()
    
if __name__ == '__main__':
    make_game()
