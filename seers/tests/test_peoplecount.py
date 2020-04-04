import unittest
from unittest.mock import patch
import imutils.video
import seer_config
import seer_plugin
import plugins.people_count
import cv2
import utils
import numpy as np


class TestPeopleCountPlugin(unittest.TestCase):
	MODEL_PATH = 'MobileNetSSD_deploy.caffemodel'
	PROTO_PATH = 'MobileNetSSD_deploy.prototxt.txt'
	FILE_STREAM_PATH = 'tests/test_vid.mp4'

	def setUp(self):
		self.videoStreamMock = patch('plugins.people_count.imutils.video.VideoStream',return_value=imutils.video.FileVideoStream(TestPeopleCountPlugin.FILE_STREAM_PATH))
		self.videoStreamMock.start()

	def tearDown(self):
		self.videoStreamMock.stop()

	def test_collect(self):
		seer_config.configuration[plugins.people_count.PeopleCount.INI][plugins.people_count.PeopleCount.MODEL_INI]		= TestPeopleCountPlugin.MODEL_PATH
		seer_config.configuration[plugins.people_count.PeopleCount.INI][plugins.people_count.PeopleCount.PROTOTXT_INI]	= TestPeopleCountPlugin.PROTO_PATH

		def testing_collect(deliv, data):
			count_data = data.get(plugins.people_count.PeopleCount.COUNT_KEY)
			self.assertIsInstance(count_data, int)
			deliv.stop()

		delivery = seer_plugin.PluginDelivery([plugins.people_count.PeopleCount],
			testing_collect, timeout=None)

		delivery.start()

	def test_init_missing_model(self):
		seer_config.configuration[plugins.people_count.PeopleCount.INI][plugins.people_count.PeopleCount.MODEL_INI] = ''

		def testing_init(deliv, data):
			self.assertFalse(plugins.people_count.PeopleCount.COUNT_KEY in data)
			deliv.stop()

		delivery = seer_plugin.PluginDelivery([plugins.people_count.PeopleCount],
			testing_init, timeout=5000)

		delivery.start()

	def test_init_missing_prototxt(self):
		seer_config.configuration[plugins.people_count.PeopleCount.INI][plugins.people_count.PeopleCount.PROTOTXT_INI] = ''

		def testing_init(deliv, data):
			self.assertFalse(plugins.people_count.PeopleCount.COUNT_KEY in data)
			deliv.stop()

		delivery = seer_plugin.PluginDelivery([plugins.people_count.PeopleCount],
			testing_init, timeout=5000)

		delivery.start()
	
	def test_find_marker(self):
		query = cv2.imread('./assets/queries/pi3.jpg', cv2.IMREAD_GRAYSCALE)
		image = cv2.imread('./assets/test/find_marker/case_side.jpg', cv2.IMREAD_GRAYSCALE)
		expected = [(1800, 1950), (1500, 2830)] # estimations based off where the raspi is in case_side.jpg
		
		actual = plugins.people_count.PeopleCount.find_marker(query, image)
		self.assertTrue(0 <= utils.euclidean_distance(expected[0][0], expected[0][1], actual[0][0], actual[0][1]) <= 250) # upper left coord
		self.assertTrue(0 <= utils.euclidean_distance(expected[1][0], expected[1][1], actual[1][0], actual[1][1]) <= 250) # lower right coord
