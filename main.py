from os import system
from enum import Enum
from time import sleep
from msvcrt import getch, kbhit
from random import randint, choice, shuffle, randrange

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
        
    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

class Figure:

    def __init__(self):
        self.__points = list()

    def draw(self):
        [point.draw() for point in self.points]

    def is_points(self, points):
        for point in points:
            if not isinstance(point, Point):
                return False
        else:
            return True
    
    @property
    def points(self):
        return self.__points
    
    @points.setter
    def points(self, points):
        if not self.is_points(points):
                raise ValueError('Must be Points list.')
        else:
            self.__points = points
            
    def clear(self):
        self.__points.clear()
        
    def add(self, points):
        if not self.is_points(points):
                raise ValueError('Must be Points list.')
        else:
            self.__points.extend(points)
        
    def kill_clone_points(self):
        self.__points = list(set(self.__points))
        
    def __getitem__(self, key):
        return self.__points[key]
        
    def __setitem__(self, key, value):
        if isinstance(value, Point):
            self.__points[key] = value
        else:
            raise ValueError('Must be Points list.')
        
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
        self.symbol = symbol
        self.width = right_bottom_x - left_top_x
        self.height = right_bottom_y - left_top_y
 
    def is_hit(self, snake):
        snake_head = snake.get_next_point()
        for point in self.points:
            if snake_head.is_hit(point):
                return True
        else:
            return False
    
    def make_maze(self, step=10):
        w = round(self.width / step)
        h = round(self.height / step)
        vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
        ver = [["|  "] * w + ['|'] for _ in range(h)] + [[]]
        hor = [["+--"] * w + ['+'] for _ in range(h + 1)]
        
        def walk(x, y):
            vis[y][x] = 1
     
            d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
            shuffle(d)
            for (xx, yy) in d:
                if vis[yy][xx]: continue
                if xx == x: hor[max(y, yy)][x] = "+  "
                if yy == y: ver[y][max(x, xx)] = "   "
                walk(xx, yy)
     
        walk(randrange(w), randrange(h))
        
        for line_number in range(1, len(hor) - 1):
            for item_number in range(len(hor[line_number])):
                if hor[line_number][item_number] == "+--":
                    x_left = item_number * step
                    x_right = (item_number + 1) * step
                    y = line_number * step
                    line = HorizontalLine(x_left, x_right, y, self.symbol)
                    self.add(line.points)
    
        for line_number in range(len(ver) ):
            for item_number in range(1, len(ver[line_number]) - 1):
                if ver[line_number][item_number] == "|  ":
                    x = item_number * step
                    y_bottom = line_number * step
                    y_top = (line_number + 1) * step
                    line = VerticalalLine(x, y_bottom, y_top, self.symbol)
                    self.add(line.points)
    
        self.kill_clone_points()
    
class Snake(Figure):

    def __init__(self, head, tail_symbol, length, direction):
        super().__init__()
        self.direction = direction
        self.head_symbol = head.symbol
        self.tail_symbol = tail_symbol
        for i in range(1, length):
            self.points.append(Point(head.x, head.y, tail_symbol).move(i, self.direction))
        self.points.append(head.move(length, self.direction))

    def move(self):
        head = self.get_next_point()
        tail = self.points.pop(0)
        after_head = self.points[-1] 
        after_head.symbol = self.tail_symbol
        self.points.append(head)
        tail.clear()
        head.draw()
        after_head.draw()

    def get_next_point(self):
        return Point(self.points[-1]).move(1, self.direction)
        
    def eat(self, food):
        head = self.get_next_point()
        if head.is_hit(food):
            food.symbol = head.symbol
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

    def create_food(self, snake, area):
        while(True):
            x = randint(2, self.area_width - 2)
            y = randint(2, self.area_height - 2)
            if (Point(x, y, snake.head_symbol) not in snake.points and 
                Point(x, y, snake.tail_symbol) not in snake.points and
                Point(x, y, area.symbol) not in area.points):
                return Point(x, y, self.symbol)

def make_game(cols=40, lines=23, step=10):
    
    # find display center
    x_center = cols // 2
    y_center = lines // 2
    is_pause = False
    step = step

    def print_center_text(text_lines):
        # clear screen
        system('cls')        
        x = x_center
        y = y_center - len(text_lines) // 2
        for text in text_lines:
            print('\033[{};{}H{}'.format(y, x - len(text) // 2, text))
            y += 1
        while True:
            if getch() == b'\r':
                system('cls')
                break

    def print_low_text(text_lines):
        print('\033[{};{}H{}'.format(lines - 1, x_center - len(text_lines) // 2, text_lines))
    
    # set console size
    system('mode con: cols={} lines={}'.format(cols, lines))

    # greetings
    print_center_text(
        ['*** SNAKE ***',
         '*' * 13,
         '',
         'w - UP   ',
         'd - RIGHT',
         's - DOWN',
         'a - LEFT',
         'space - PAUSE',
         '',
         'press ENTER']
    )
    
    game_speed = 0.2

    score = 0
    
    print_low_text('SCORE - {}'.format(score))
    
    # lines - 3 , because going beyond screen
    area = Area(1, 1, cols, lines - 3, '#')
    area.make_maze(step)

    snake_head_x = choice(range(round(step // 2), cols, step))
    snake_head_y = choice(range(round(step // 2), lines - 3, step))
    # find good direction
    top = snake_head_y - max([point.y for point in area.points if point.x == snake_head_x and point.y < snake_head_y])
    bottom = min([point.y for point in area.points if point.x == snake_head_x and point.y > snake_head_y]) - snake_head_y
    left = snake_head_x - max([point.x for point in area.points if point.y == snake_head_y and point.x < snake_head_x])
    right = min([point.x for point in area.points if point.y == snake_head_y and point.x > snake_head_x]) - snake_head_x
    longer_way = max(top, bottom, left, right)
    good_direction = {top:Directions.top, bottom:Directions.bottom, left:Directions.left, right:Directions.right}
    # creat sneak randomly
    snake_head = Point(snake_head_x, snake_head_y, 'o')
    snake = Snake(snake_head, '*', 3, good_direction[longer_way])
    
    foor_creator = FoodCreator(cols, lines - 3, '$')
    food = foor_creator.create_food(snake, area)
    
    [i.draw() for i in (area, food, snake)]

    while(True):
        # check is key press
        if kbhit():
            pressed_key = getch()
            if pressed_key == b' ':
                is_pause = not is_pause
            if not is_pause:
                print_low_text(' ' * 15)
                print_low_text('SCORE - {}'.format(score))
                snake.handle_key(pressed_key)
            else:
                print_low_text(' ' * 15)
                print_low_text('*** PAUSE ***')

        if not is_pause:
            if area.is_hit(snake) or snake.is_hit_tail():
                print_center_text(
                    ['THE END',
                     '',
                     'SCORE - {}'.format(score),
                     '',
                     'press ENTER',]
                    )
                break

            if snake.eat(food):
                score += 25
                food = foor_creator.create_food(snake, area)
                food.draw()
                game_speed -= game_speed * 0.05
                print_low_text('SCORE - {}'.format(score))

            sleep(game_speed)
            snake.move()
    
    # set default console size
    system('mode con: cols={} lines={}'.format(80, 25))
    
if __name__ == '__main__':
    make_game()
