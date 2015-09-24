#!/usr/bin/python

# Import modules
from TwitterAPI import TwitterAPI
import ConfigParser
import time
import datetime
import picamera

# Load config file
config = ConfigParser.RawConfigParser()
config.read('_config.cfg')

# Set up API
api = TwitterAPI(
	config.get('twitter', 'consumer_key'),
	config.get('twitter', 'consumer_secret'),
	config.get('twitter', 'access_token_key'),
	config.get('twitter', 'access_token_secret')
)

# Get the last mention
last_mention_id = config.get('mentions', 'last_id')

# Gett al the mentions since the last mention
mentions = api.request('statuses/mentions_timeline', {'since_id': last_mention_id}).json()

if mentions :

	# Initialise & set up the camera
	camera = picamera.PiCamera()
	camera.resolution = (1280, 720)
	camera.framerate = 30
	time.sleep(2)
	camera.shutter_speed = camera.exposure_speed
	camera.exposure_mode = 'off'
	g = camera.awb_gains
	camera.awb_mode = 'off'
	camera.awb_gains = g


	for item in reversed(mentions):
		# Set the last id to that tweet
		last_mention_id = item['id']

		# Make a user
		user = item['user']

		# Take a picture
		filename = './media/images/%s-%s.jpg' % (user['screen_name'], datetime.datetime.now())
		camera.capture(filename)

		# Upload a file
		file = open(filename, 'rb')
		data = file.read()
		r = api.request('media/upload', None, {'media': data})
		print vars(r)

		# Build the status and send
		status = 'Hello @%s - here is a nice picture' % (user['screen_name'])

		if r.status_code == 200:
			media_id = r.json()['media_id']
			r = api.request('statuses/update', {'status':status, 'media_ids': media_id})
			print vars(r)

	config.set('mentions', 'last_id', last_mention_id)

	# Write the data
	with open('_config.cfg', 'w') as f:
	   config.write(f)
