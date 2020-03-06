import unittest
import seer_plugin
import plugins.test_plugins

class TestPlugins(unittest.TestCase):
	def test_collect(self):
		plugs = \
		[
			plugins.test_plugins.ActualTestCollector,
			plugins.test_plugins.ActualTestCollector2
		]

		def testing_data_return(deliv, data):
			self.assertEquals(1, data['test'])
			self.assertEquals(64, data['howdy!'])
			deliv.stop()

		delivery = seer_plugin.PluginDelivery(plugs,
			testing_data_return)

		delivery.start()

	def test_init(self):
		test_value = 100

		class TestInitPlugin(seer_plugin.DataCollectorPlugin):
			def init(self):
				self.test = test_value

			def collect(self):
				return {'test': self.test}

		def testing_init(deliv, data):
			self.assertEquals(test_value, data['test'])
			deliv.stop()

		delivery = seer_plugin.PluginDelivery([TestInitPlugin],
			testing_init)

		delivery.start()

	def test_shutdown(self):
		test_value 	= 'test'
		test_list 	= []

		class TestShutdownPlugin(seer_plugin.DataCollectorPlugin):
			def shutdown(self):
				test_list.append(test_value)

		def testing_shutdown(deliv, data):
			deliv.stop()

		delivery = seer_plugin.PluginDelivery([TestShutdownPlugin], 
			testing_shutdown)

		delivery.start()

		self.assertEquals([test_value], test_list)

class TestDelivery(unittest.TestCase):
	def test_init_exception(self):
		test_key = 'test'

		class InitExceptionPlugin(seer_plugin.DataCollectorPlugin):
			def init(self):
				raise Exception

			def collect(self):
				return {test_key: test_key}

		def testing_exception(deliv, data):
			self.assertFalse(test_key in data)
			deliv.stop()

		delivery = seer_plugin.PluginDelivery([InitExceptionPlugin],
			testing_exception)

		delivery.start()

	def test_data_exception(self):
		class DataExceptionPlugin(seer_plugin.DataCollectorPlugin):
			def collect(self):
				raise Exception

		def testing_exception(deliv, data):
			self.assertEquals(1, len(data))
			self.assertEquals(1, data['test'])
			deliv.stop()
			
		delivery = seer_plugin.PluginDelivery([DataExceptionPlugin, plugins.test_plugins.ActualTestCollector],
			testing_exception)

		delivery.start()

	def test_shutdown_exception(self):
		class ShutdownExceptionPlugin(seer_plugin.DataCollectorPlugin):
			def shutdown(self):
				raise Exception

		def testing_exception(deliv, data):
			deliv.stop()
			
		delivery = seer_plugin.PluginDelivery([ShutdownExceptionPlugin],
			testing_exception)

		delivery.start()