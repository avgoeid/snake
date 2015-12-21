import unittest

from main import Directions, Point, Figure

class TestDirections(unittest.TestCase):
    
    def test_opposite(self):
        self.assertRaises(KeyError, Directions.opposite, 123)
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
        
        point  = Point(1, 0, 'd')
        point.move(1, Directions.bottom)
        self.assertEqual(point, Point(1, 1, 'd'))
    
    def test_clear(self):
        point = Point(3, 56, '6')
        point.clear()
        self.assertEqual(point.symbol, ' ')
    
    def test_is_hit(self):
        self.assertTrue(Point(1, 2, '8').is_hit(Point(1, 2, 'j')))
    
    def test_equal(self):
        self.assertEqual(Point(1, 67, '4'), Point(1, 67, '4'))
    
class TestFigure(unittest.TestCase):
    
    def test_init(self):
        self.assertFalse(Figure().points)
        self.assertRaises(TypeError, Figure, 3)
    
    def test_points(self):
        with self.assertRaises(ValueError):
            figure = Figure()
            figure.points = [3]
 
if __name__ == '__main__':
    unittest.main()
