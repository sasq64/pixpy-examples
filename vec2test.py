import unittest
import pixpy as pix

Vec2 = pix.Vec2
#Vec2i = pix.Vec2i


class TestStringMethods(unittest.TestCase):

    def test_addition(self):
        a = Vec2(9, 4)
        b = Vec2(3, 2)
        z = 5
        self.assertEqual(a + b, Vec2(12, 6))
        self.assertEqual(a + z, Vec2(14, 9))
        a += z
        self.assertEqual(a, Vec2(14, 9))
        b += a
        self.assertEqual(b, Vec2(17, 11))

    def test_multiplication(self):
        a = Vec2(2, 4)
        b = Vec2(5, 3)
        z = 6
        zf = 0.5
        self.assertEqual(a * b, Vec2(10, 12))
        self.assertEqual(a * z, Vec2(12, 24))
        a *= z
        self.assertEqual(a, Vec2(12, 24))
        b *= a
        self.assertEqual(b, Vec2(60, 72))
        self.assertEqual(a * 0.5, Vec2(6, 12))
        

    def test_division(self):
        a = Vec2(12, 18)
        b = Vec2(3, 2)
        z = 6
        self.assertEqual(a / b, Vec2(4, 9))
        self.assertEqual(a / z, Vec2(2, 3))
        a /= z
        self.assertEqual(a, Vec2(2, 3))
        b = Vec2(30, 90)
        b /= a
        self.assertEqual(b, Vec2(15, 30))

    def test_equality(self):
    
         f0 = Vec2(2.2, 4.1)
         f1 = Vec2(2, 4)
    
         self.assertNotEqual(f0, f1)
         self.assertNotEqual(f0, (2,4))
         self.assertEqual(f1, (2,4))
         self.assertEqual(f0, (2.2,4.1))


if __name__ == '__main__':
    unittest.main()
