import utils
import unittest
import math

class UtilsTest(unittest.TestCase):
    """
    Tests utils functions
    """

    def test_in_to_cm(self):
        """
        Tests that the value is converted correctly
        """
        expected = 25.4
        
        actual = utils.in_to_cm(10)
        self.assertEqual(expected, actual)
    
    def test_calc_focal_length(self):
        """
        Tests that the focal length is calculated properly
        """

        distance = 10
        pixels = 400
        width = 8

        expected = 500

        actual = utils.calc_focal_length(distance, width, pixels)
        self.assertEqual(expected, actual)

    def test_euclidean_distance(self):
        """
        Tests the distance formula
        """

        x1 = 5.0
        y1 = 2.0
        x2 = 12.0
        y2 = 5.0

        expected = 7.612

        actual = utils.euclidean_distance(x1, y1, x2, y2)
        self.assertAlmostEqual(expected, actual, 2)