"""
The SEER component.

This is the entry point into the seer component.
It starts by gathering all the plugins under the plugins folder and runs
each one in a different thread. As they run, the delivery system will occasionally
iterate through each plugin to gather whatever data they currently have in queue.
This data is then packged up into a JSON format and then sent to an API endpoint
of the Delphi component.
"""

import seer_plugin
import seer_config

import sys
import logging
import requests
import json

# This is where to put plugins
PLUGINS = \
[
]

logging.basicConfig(level=seer_config.logging_level, format='[%(levelname)s] %(asctime)s (%(module)s): %(message)s')
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

http_session	= requests.Session()
timeout			= None if seer_config.data_collection_timeout is None else seer_config.data_collection_timeout / 1000
url				= '{}:{}{}'.format(seer_config.delphi_address, seer_config.delphi_port, seer_config.delphi_endpoint)

# Since Python lambdas suck, I need to make
# a function. Capturing variables such
# as http_session and url.
def http_send_data(delivery_system, data):
	try:
		r = http_session.post(url, data=json.dumps(data))
		if r.status_code != 200:
			logging.error(f'Error sending delivery. Status code: {r.status_code}')
			delivery_system.stop()
	except requests.exceptions.ConnectionError as e:
		logging.error(f'Error connecting to delphi: {e}')
		delivery_system.stop()

if len(PLUGINS) == 0:
	logging.error('No plugins loaded!')
	sys.exit(1)

delivery = seer_plugin.PluginDelivery(PLUGINS, 
	http_send_data, seer_config.data_collection_timeout, 
	seer_config.data_collection_queue_size)

delivery.start()