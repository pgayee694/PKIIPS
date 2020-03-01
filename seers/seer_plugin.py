import seer_config

import queue
import time
import logging
import threading

class DataCollectorPlugin(object):
	"""
	An abstract class that describes the behaviour
	of a data collector plugin. These plugins
	will be dynamically loaded when the seer application
	runs.
	"""

	def __init__(self):
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

		stop_token (threading.Event): A boolean value to check whether to stop collecting data
									and shutdown
	"""
	plug = plug_class()
	try:
		plug.init()
	except Exception as e:
		logging.error(f"Exception thrown from initializing '{plug_class.__name__}': {e}")
		return

	while not stop_token.is_set():
		try:
			data = plug.collect()
		except Exception as e:
			logging.error(f"Exception thrown by collecting data from '{plug_class.__name__}': {e}")
			return

		while True:
			if stop_token.is_set():
				break
			try:
				message_queue.put(data, True, seer_config.data_collection_timeout)
				break
			except queue.Full:
				pass
		time.sleep(plug.time_step / 1000)

	try:
		plug.shutdown()
	except Exception as e:
		logging.error(f"Exception thrown from shutting down '{plug_class.__name__}': {e}")

class PluginDelivery(object):
	"""
	Class that handles running plugins and delivering the data.

	Data is delivered to the given send_func function when data
	is retrieved from all plugins at a given time. This function
	must take in the delivery object that called it and the data object.
	"""
	def __init__(self, plugins, send_func, timeout=1000, queue_size=1):
		"""
		Initializes a PluginDelivery

		Parameters:
			plugins (list: DataCollectorPlugin): List of plugins

			send_func (function): Function to be called when data
								  has been collected from all plugins. Must take in
								  two arguments:
								  	1. This delivery object
									2. The data dictionary

			timeout (int): A timeout in milliseconds to wait for data from a plugin

			queue_size (int): The size to make the data queues for each plugin
		"""
		self.plugins		= plugins
		self.send_func		= send_func
		self.queue_size		= queue_size
		self.timeout		= timeout
		self.__threads		= []
		self.__stop_token	= threading.Event()

	@property
	def timeout(self):
		"""
		Returns the current plugin data collection timeout
		"""
		return self.__timeout

	@timeout.setter
	def timeout(self, value):
		"""
		Sets the plugin data collection timeout

		Parameters:
			value (int): Timeout in milliseconds
		"""
		self.__timeout = None if value is None else value / 1000

	def start(self):
		"""
		Starts collecting data from the given plugins
		"""
		self.reset()
		for plug in self.plugins:
			q		= queue.Queue(self.queue_size)
			thread 	= threading.Thread(target=plugin_collection, args=(plug, q, self.__stop_token), daemon=True)
			thread.start()
			self.__threads.append((thread, q))

		try:
			while not self.is_stopped() and self.__check_threads():
				data = self.__grab_data()
				self.send_func(self, data) # Calling upon our send_func instance variable
		except KeyboardInterrupt:
			self.stop()

	def reset(self):
		"""
		Resets the state of the delivery system to start fresh again
		"""
		self.stop()
		self.__threads 		= []
		self.__stop_token	= threading.Event()

	def stop(self):
		"""
		Stops all running plugins
		"""
		self.__stop_token.set()
		for thread, _ in self.__threads:
			thread.join(3)

	def __grab_data(self):
		"""
		Collects data from all running plugins.
		Returns a dictionary of all the results from
		the plugins.
		"""
		delivery_data = {}
		for _, q in self.__threads:
			try:
				collection_data = q.get(True, self.__timeout)
			except queue.Empty:
				continue
		
			delivery_data.update(collection_data)

		return delivery_data

	def __check_threads(self):
		"""
		Removes any threads and its corresponding queue if the plugin
		is no longer running.

		Returns True if there are still plugins running, False otherwise.
		"""
		self.__threads[:] = [(thread, q) for thread, q in self.__threads if thread.is_alive()]

		return len(self.__threads) > 0

	def is_stopped(self):
		"""
		Return True if plugins were told to stop, False otherwise.
		"""
		return self.__stop_token.is_set()