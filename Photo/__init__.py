import time
import datetime

class Graffcam():
	# Initialise & set up the camera
	def __init__(self, home_path, camera):
		self.home_path = home_path

		self.camera = camera
		self.camera.resolution = (1280, 720)
		self.camera.framerate = 30
		time.sleep(2)

		self.camera.sharpness = 0
		self.camera.contrast = 0
		self.camera.brightness = 50
		self.camera.saturation = 0
		self.camera.ISO = 0
		self.camera.video_stabilization = True
		self.camera.exposure_compensation = 0
		self.camera.exposure_mode = 'auto'
		self.camera.meter_mode = 'average'
		self.camera.awb_mode = 'auto'
		self.camera.image_effect = 'none'
		self.camera.color_effects = None
		self.camera.rotation = 0
		self.camera.hflip = False
		self.camera.vflip = False
		self.camera.crop = (0.0, 0.0, 1.0, 1.0)

	def get_filename(self, user, folder):
		filename = '%smedia/%s/%s-%s' % (self.home_path, folder, user['screen_name'], datetime.datetime.now())
		return filename


	def capture_photo(self, user):
		# Take a picture
		filename = self.get_filename(user, 'images') + '.jpg'
		self.camera.capture(filename)
		return filename

	def record_video(self, user):
		filename = self.get_filename(user)
		camera.start_recording('video.h264')
		sleep(5)
		camera.stop_recording()
