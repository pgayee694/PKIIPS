import seer_plugin
import random
import cv2
import logging

class test_collector(object):
	pass

class actual_test_collector(seer_plugin.data_collector_plugin):
	def init(self):
		logging.info('Initialized!')

	def collect(self):
		return {'test': 1}

	def shutdown(self):
		logging.info('Shutdown!')

class actual_test_collector2(seer_plugin.data_collector_plugin):
	def init(self):
		logging.info('Initialized 2!')

	def collect(self):
		return {'howdy!': 64}

	def shutdown(self):
		logging.info('No more howdy :(')

class camera_collector(seer_plugin.data_collector_plugin):
	def init(self):
		self.video 	= cv2.VideoCapture()
		self.opened = self.video.open(0)
		logging.info('Intialized camera')
		
	def collect(self):
		if self.opened:
			data = self.video.read()

		return {"camera": self.opened}

	def shutdown(self):
		if self.opened:
			self.video.release()