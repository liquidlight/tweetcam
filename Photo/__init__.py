import time
import datetime

class Graffcam():
	# Initialise & set up the camera
	def __init__(self, camera):
		self.camera = camera
		self.camera.resolution = (1280, 720)
		self.camera.framerate = 30
		time.sleep(2)
		self.camera.shutter_speed = self.camera.exposure_speed
		self.camera.exposure_mode = 'off'
		g = self.camera.awb_gains
		self.camera.awb_mode = 'off'
		self.camera.awb_gains = g

	def capture_photo(self, user):
		# Take a picture
		filename = './media/images/%s-%s.jpg' % (user['screen_name'], datetime.datetime.now())
		self.camera.capture(filename)
		return filename
