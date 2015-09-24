import time
import datetime
import os

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
		self.camera.video_stabilization = False
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

	def get_filename(self, user, folder, extension):
		filename = '%smedia/%s/%s-%s.%s' % (self.home_path, folder, user, int(time.time()), extension)
		filename.replace(' ', '-')
		return filename


	def capture_photo(self, user):
		# Take a picture
		filename = self.get_filename(user, 'images', 'jpg')
		self.camera.capture(filename)
		return filename

	def record_video(self, user):
		raw_file = self.get_filename(user, 'videos', 'h264')
		processed_file = self.get_filename(user, 'videos', 'mp4')
		print '[status: Recording]'
		self.camera.start_recording(raw_file)
		time.sleep(5)
		print '[status: Stopping]'
		self.camera.stop_recording()

		print '[status: Converting]'
		os.system('MP4Box -add %s %s' % (raw_file, processed_file))
		print '[status: Deleting]'
		os.remove(raw_file)
		return processed_file
