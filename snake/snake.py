__author__ = 'holovenkom'

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

    OPPOSITE = {
            top: bottom,
            right: left,
            bottom: top,
            left: right,
        }

    def opposite(direction):        
        return Directions.OPPOSITE.value[direction]

class Point:

    def __init__(self, *args):
        args_len = len(args)
        if args_len == 1 and isinstance(args[0], Point):
            self.x, self.y, self.symbol = args[0].x, args[0].y, args[0].symbol
        elif args_len == 3:
            self.x, self.y, self.symbol = args
        else:
            raise ValueError('Must be Point or int, int, symbol.')

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        if isinstance(x, int) and 0 <= x <= 100:
            self.__x = x
        else:
            raise ValueError('Must be int.')

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        if isinstance(y, int) and 0 <= y <= 100:
            self.__y = y
        else:
            raise ValueError('Must be int.')

    @property
    def symbol(self):
        return self.__symbol

    @symbol.setter
    def symbol(self, symbol):
        if isinstance(symbol, str) and len(symbol) == 1 and symbol != ' ':
            self.__symbol = symbol
        else:
            raise ValueError('Must be one symbol.')
    
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
        self.__symbol = ' '
        self.draw()

    def is_hit(self, point):
        return self.x == point.x and self.y == point.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.symbol == other.symbol
    
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
        if key == Directions.opposite(self.direction.value):
            pass
        elif key == Directions.top.value:
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

def make_game(cols=40, lines=20):

    X_CENTER = cols // 2
    Y_CENTER = lines // 2

    def print_text(text_lines):
        # find display center
        system('cls')
        x = X_CENTER
        y = Y_CENTER - len(text_lines) // 2
        for text in text_lines:
            print('\033[{};{}H{}'.format(y, x - len(text) // 2, text))
            y += 1
        while True:
            if getch() == b'\r':
                system('cls')
                break

    # set console size
    system('mode con: cols={} lines={}'.format(cols, lines))

    # greetings
    print_text(
        ['**SNAKE**',
         '*' * 9,
         'w - up   ',
         'd - right',
         's - down',
         'a - left',
         '',
         'press ENTER']
    )

    # lines - 2 , because going beyond screen
    area = Area(1, 1, cols, lines - 2, '#')

    foor_creator = FoodCreator(cols, lines, '$')
    food = foor_creator.create_food()

    snake_head = Point(X_CENTER, Y_CENTER, '*')
    snake = Snake(snake_head, 3, choice((Directions.top, Directions.right, Directions.bottom, Directions.left)))

    [i.draw() for i in (area, food, snake)]

    game_speed = 0.3

    score = 0

    while(True):
        # check is key press
        if kbhit():
            snake.handle_key(getch())

        if area.is_hit(snake) or snake.is_hit_tail():
            print_text(
                ['THE END',
                 '',
                 'score - %r' % score,
                 '',
                 'press ENTER',]
                )
            break

        if snake.eat(food):
            score += 25
            food = foor_creator.create_food()
            food.draw()
            game_speed -= 0.015

        sleep(game_speed)
        snake.move()
    system('mode con: cols={} lines={}'.format(80, 25))
    
if __name__ == '__main__':
    make_game()
