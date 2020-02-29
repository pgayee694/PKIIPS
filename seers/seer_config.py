import configparser
import logging

configuration = configparser.ConfigParser()
configuration.read('seer_config.ini')

general_ini					= 'general'
logging_level				= logging.getLevelName(configuration[general_ini].get('logging', fallback='DEBUG'))

delphi_ini					= 'delphi'
delphi_address				= configuration[delphi_ini].get('address')
delphi_port					= configuration[delphi_ini].get('port')
delphi_endpoint				= configuration[delphi_ini].get('endpoint')


plugin_ini					= 'plugin'
default_time_step			= configuration[plugin_ini].getint('default-time-step', fallback=100)
data_collection_timeout		= configuration[plugin_ini].getint('date-collection-timeout', fallback=None)
data_collection_queue_size	= configuration[plugin_ini].getint('data-collection-queue-size', fallback=1)