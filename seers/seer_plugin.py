import seer_config

import queue
import time
import logging

class data_collector_plugin(object):
	"""
	An abstract class that describes the behaviour
	of a data collector plugin. These plugins
	will be dynamically loaded when the seer application
	runs.
	"""

	def __init__(self):
		self.logger = logging.getLogger()
		# Custom time step to query this plugin. This will be the amount of milliseconds
		# between calls to collect.
		self.time_step = seer_config.default_time_step

	def init(self):
		"""
		Called once the plugin has been created and
		before data has been requested to collect.
		This can be used to intialize variables before
		the data collection step.
		"""
		pass

	def shutdown(self):
		"""
		Called when the seer application shutdowns. Meant
		to clean up any resources that this plugin uses.
		"""
		pass

	def collect(self):
		"""
		Called every time step to collect data. Must
		return a map consisting of named data. This data
		will eventually be delivered to the Delphi system.
		"""
		return {}

def plugin_collection(plug_class, message_queue, stop_token):
	"""
	This function is to be used to loop collection of the given plugin
	until the given stop token tells the loop to stop.

	Parameters:
		plug_class (type): A class type of data collector plugin

		message_queue (queue.Queue): A queue for sending collection data through
									 to the delivery system

		time_step (int): An amount of milliseconds to wait between asking for collection
						 information

		stop_token (ctypes.c_bool): A boolean value to check whether to stop collecting data
									and shutdown
	"""
	plug = plug_class()
	plug.init()
	while not stop_token.is_set():
	
		data = plug.collect()
		while True:
			if stop_token.is_set():
				break
			try:
				message_queue.put(data, True, seer_config.data_collection_timeout)
				break
			except queue.Full:
				pass
		time.sleep(plug.time_step / 1000)

	plug.shutdown()