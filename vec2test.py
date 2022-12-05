import unittest
import pixpy as pix

Float2 = pix.Float2
#Int2 = pix.Int2


class TestStringMethods(unittest.TestCase):

    def test_addition(self):
        a = Float2(9, 4)
        b = Float2(3, 2)
        z = 5
        self.assertEqual(a + b, Float2(12, 6))
        self.assertEqual(a + z, Float2(14, 9))
        a += z
        self.assertEqual(a, Float2(14, 9))
        b += a
        self.assertEqual(b, Float2(17, 11))

    def test_multiplication(self):
        a = Float2(2, 4)
        b = Float2(5, 3)
        z = 6
        zf = 0.5
        self.assertEqual(a * b, Float2(10, 12))
        self.assertEqual(a * z, Float2(12, 24))
        a *= z
        self.assertEqual(a, Float2(12, 24))
        b *= a
        self.assertEqual(b, Float2(60, 72))
        self.assertEqual(a * 0.5, Float2(6, 12))
        

    def test_division(self):
        a = Float2(12, 18)
        b = Float2(3, 2)
        z = 6
        self.assertEqual(a / b, Float2(4, 9))
        self.assertEqual(a / z, Float2(2, 3))
        a /= z
        self.assertEqual(a, Float2(2, 3))
        b = Float2(30, 90)
        b /= a
        self.assertEqual(b, Float2(15, 30))

    def test_equality(self):
    
         f0 = Float2(2.2, 4.1)
         f1 = Float2(2, 4)
    
         self.assertNotEqual(f0, f1)
         self.assertNotEqual(f0, (2,4))
         self.assertEqual(f1, (2,4))
         self.assertEqual(f0, (2.2,4.1))


if __name__ == '__main__':
    unittest.main()
