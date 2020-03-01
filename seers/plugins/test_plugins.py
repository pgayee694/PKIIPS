"""
These plugins are both used as example plugins
to learn from as well as used in unit tests.
"""

import seer_plugin
import cv2
import logging

class ActualTestCollector(seer_plugin.DataCollectorPlugin):
	def init(self):
		logging.info('Initialized!')

	def collect(self):
		return {'test': 1}

	def shutdown(self):
		logging.info('Shutdown!')

class ActualTestCollector2(seer_plugin.DataCollectorPlugin):
	def init(self):
		logging.info('Initialized 2!')

	def collect(self):
		return {'howdy!': 64}

	def shutdown(self):
		logging.info('No more howdy :(')

class CameraCollector(seer_plugin.DataCollectorPlugin):
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