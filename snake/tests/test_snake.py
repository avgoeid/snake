import unittest

from ..snake import Directions, Point, Figure, VerticalalLine, HorizontalLine, Area, Snake, FoodCreator

class TestDirections(unittest.TestCase):
    
    def test_opposite(self):
        self.assertRaises(KeyError, Directions.opposite, 123)
        self.assertEqual(Directions.opposite(b'w'), b's')

class TestPoint(unittest.TestCase):

    def test_init(self):
        self.assertRaises(ValueError, Point, 1, 0, 'sd')
        self.assertRaises(ValueError, Point, 3, -1, 'd')
        self.assertRaises(ValueError, Point, 1, 102, 'd')
        self.assertRaises(ValueError, Point, 0, 0, ' ')
        self.assertRaises(ValueError, Point, 0, 0, 6)
        self.assertRaises(ValueError, Point, -3245, 0, 6)
        self.assertRaises(ValueError, Point, 'sds')

    def test_repr(self):
        self.assertEqual(str(Point(3, 6, '8')), 'Point(3, 6, 8)')
    
    def test_equal(self):
        self.assertTrue(Point(1, 45, 'r') == Point(1, 45, 'r'))
    
    def test_clear(self):
        point = Point(4, 5, 'f')
        point.clear()
        self.assertTrue(point.symbol == ' ')
    
    def test_move(self):
        point = Point(1, 0, 'd')
        self.assertRaises(ValueError, point.move, 1, Directions.top)
        point.move(1, Directions.bottom)
        self.assertTrue(point == Point(1, 1, 'd'))
    
class TestFigurw(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
