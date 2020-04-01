import unittest
import seer_config
import seer_plugin
import plugins.people_count
import cv2

class TestPeopleCountPlugin(unittest.TestCase):
	MODEL_PATH = 'MobileNetSSD_deploy.caffemodel'
	PROTO_PATH = 'MobileNetSSD_deploy.prototxt.txt'

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
		
		plugins.people_count.PeopleCount.find_marker(query, image)
