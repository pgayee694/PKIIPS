import unittest
from unittest.mock import MagicMock, patch
import sys

# Can't install RPi on non-pi's, so need to do some import shenanigans with mocks
rpi_mock = MagicMock(name='rpi')
sys.modules['RPi'] = rpi_mock

import utils

class UtilsTest(unittest.TestCase):
    """
    Tests utils functions
    """

    def gpio_input_side_eff(self, num):
        ret = self.gpio_input_counter % 2
        self.gpio_input_counter += 1
        return ret

    def setUp(self):

        self.gpio_input_counter = 0

        # Set up time mock
        time_patcher = patch('utils.time')
        self.mock_time = time_patcher.start()
        self.addCleanup(time_patcher.stop)
        self.mock_time.time.side_effect = [10, 5, 10]

        # Set up RPI.GPIO mock
        rpi_mock.GPIO.input.side_effect = [0, 1, 1, 0]

    def tearDown(self):
        pass

    def test_find_next_node(self):
        """
        Tests that the pins are called correctly and that we get the distance
        to the next node correctly
        """

        actual_dist = 85750 # (10-5) * 34300 / 2
        distance = utils.find_next_node()
        self.assertEqual(rpi_mock.GPIO.input.call_count, 4)
        self.assertEqual(self.mock_time.time.call_count, 3)
        self.assertEqual(distance, actual_dist)
