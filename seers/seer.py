class data_collector_plugin(object):
	def __init__(self):
		pass

	def init(self):
		pass

	def shutdown(self):
		pass

	def collect(self):
		return {}

import plugins
import threading
import time
import queue
import ctypes

def plugin_collection(plug_class, message_queue, time_step, stop_token):
	plug = plug_class()
	plug.init()
	while True:
		if stop_token.value:
			break
	
		data = plug.collect()
		while True:
			if stop_token.value:
				break
			try:
				message_queue.put(data, True, .2)
				break
			except queue.Full:
				pass
		time.sleep(time_step / 1000)

	plug.shutdown()

if __name__ == '__main__':
	# This information can be inside some sort of configuration file
	TIME_STEP_MS				= 100
	DATA_COLLECTION_TIMEOUT_MS	= 100
	QUEUE_SIZE 					= 1
	
	plugs 		= plugins.gather_plugins()
	queues 		= [queue.Queue(QUEUE_SIZE) for _ in range(len(plugs))]
	threads		= []
	stop_token	= ctypes.c_bool()

	for plug, q in zip(plugs, queues):
		thread = threading.Thread(target=plugin_collection, args=(plug, q, TIME_STEP_MS, stop_token))
		thread.start()
		threads.append(thread)

	try:
		while True:
			delivery_data = {}
			for q in queues:
				try:
					collection_data = q.get(True, None if DATA_COLLECTION_TIMEOUT_MS is None else (TIME_STEP_MS + DATA_COLLECTION_TIMEOUT_MS) / 1000)
				except queue.Empty:
					continue

				delivery_data.update(collection_data)

			print(delivery_data)
	except KeyboardInterrupt:
		stop_token.value = True

	for thread in threads:
		thread.join()