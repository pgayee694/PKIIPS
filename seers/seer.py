"""
The SEER component.

This is the entry point into the seer component.
It starts by gathering all the plugins under the plugins folder and runs
each one in a different thread. As they run, the delivery system will occasionally
iterate through each plugin to gather whatever data they currently have in queue.
This data is then packged up into a JSON format and then sent to an API endpoint
of the Delphi component.
"""

import plugins
import seer_plugin
import seer_config

import threading
import queue
import sys
import logging
import requests

logging.basicConfig(level=seer_config.logging_level, format='[%(levelname)s] %(asctime)s (%(module)s): %(message)s')
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

http_session	= requests.Session()
timeout			= None if seer_config.data_collection_timeout is None else seer_config.data_collection_timeout / 1000
url				= '{}:{}{}'.format(seer_config.delphi_address, seer_config.delphi_port, seer_config.delphi_endpoint)

plugs = plugins.gather_plugins()
if len(plugs) == 0:
	logging.error('No plugins loaded!')
	sys.exit(1)

queues 		= [queue.Queue(seer_config.data_collection_queue_size) for _ in range(len(plugs))]
threads		= []
stop_token	= threading.Event()

for plug, q in zip(plugs, queues):
	thread = threading.Thread(target=seer_plugin.plugin_collection, args=(plug, q, stop_token), daemon=True)
	thread.start()
	threads.append(thread)

try:
	while True:
		delivery_data = {}
		for q in queues:
			try:
				collection_data = q.get(True, timeout)
			except queue.Empty:
				continue

			delivery_data.update(collection_data)

		try:
			r = http_session.post(url, data=delivery_data)
			if r.status_code != 200:
				logging.error(f'Error sending delivery. Status code: {r.status_code}')
				stop_token.set()
				break
		except requests.exceptions.ConnectionError as e:
			logging.error(f'Error connecting to delphi: {e}')
			stop_token.set()
			break
except KeyboardInterrupt:
	stop_token.set()

logging.info('Shutting down data components...')
for thread in threads:
	thread.join(3)