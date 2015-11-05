import time
import datetime
import os

class TweetCam():
	# Initialise & set up the camera
	def __init__(self, home_path, camera, logging):
		self.home_path = home_path
		self.logging = logging

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

	def get_filename(self, tweet, folder, extension):
		filename = '%smedia/%s/%s.%s' % (self.home_path, folder, tweet['id'], extension)
		return filename


	def capture_photo(self, tweet):
		# Take a picture
		self.logging.info('Taking a picture')
		filename = self.get_filename(tweet, 'images', 'jpg')
		self.camera.capture(filename)
		return filename

	def record_video(self, tweet):
		raw_file = self.get_filename(tweet, 'videos', 'h264')
		processed_file = self.get_filename(tweet, 'videos', 'mp4')

		self.logging.info('Recording video')
		self.camera.start_recording(raw_file)
		time.sleep(5)

		self.logging.info('Stopping recording')
		self.camera.stop_recording()

		self.logging.info('Converting video [%s]' % processed_file)
		os.system('MP4Box -add %s %s' % (raw_file, processed_file))

		self.logging.info('Deleting h264 video')
		os.remove(raw_file)

		return processed_file
