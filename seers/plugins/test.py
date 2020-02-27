from seer import data_collector_plugin
import random

class test_collector(object):
	pass

class actual_test_collector(data_collector_plugin):
	def init(self):
		print("Initialized!")

	def collect(self):
		return {'test': 1}

	def shutdown(self):
		print("Shutdown!")

class actual_test_collector2(data_collector_plugin):
	def init(self):
		print("Initialized 2!")

	def collect(self):
		return {'howdy!': 64}

	def shutdown(self):
		print("No more howdy :(")

class camera_collector(data_collector_plugin):

	def init(self):
		import cv2
		self.video 	= cv2.VideoCapture()
		self.opened = self.video.open(0)
		print("Intialized camera")
		
	def collect(self):
		if self.opened:
			data = self.video.read()

		return {"camera": self.opened}

	def shutdown(self):
		if self.opened:
			self.video.release()

# class camera_collector2(data_collector_plugin):
# 	def init(self):
# 		import cv2
# 		self.video 	= cv2.VideoCapture()
# 		self.opened = self.video.open(0)
		
# 	def collect(self):
# 		if self.opened:
# 			data = self.video.read()

# 		return {"camera2": self.opened}

# 	def shutdown(self):
# 		if self.opened:
# 			self.video.release()