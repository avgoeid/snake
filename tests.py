import unittest

from main import Directions, Point, Figure, VerticalalLine, HorizontalLine, Area, Snake, FoodCreator

class TestDirections(unittest.TestCase):
    
    def test_opposite(self):
        self.assertRaises(KeyError, Directions.opposite, 123)
        self.assertRaises(KeyError, Directions.opposite, b'we')
        self.assertRaises(KeyError, Directions.opposite, b'')
        
        self.assertEqual(Directions.opposite(b'w'), b's')

class TestPoint(unittest.TestCase):

    def test_init(self):
        self.assertRaises(ValueError, Point, 1, 0, 'sd')
        self.assertRaises(ValueError, Point, 3, -1, 'd')
        self.assertRaises(ValueError, Point, 1, 102, 'd')
        self.assertRaises(ValueError, Point, -5, 102, 'ssd', 'sds')
        self.assertRaises(ValueError, Point, 0, 0, ' ')
        self.assertRaises(ValueError, Point, 0, 0, 6)
        self.assertRaises(ValueError, Point, 'sds')

    def test_repr(self):
        self.assertEqual(str(Point(3, 6, '8')), 'Point(3, 6, 8)')

    def test_move(self):
        self.assertRaises(ValueError, Point(1, 0, 'd').move, 1, Directions.top)
        
    
class TestFigurw(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
