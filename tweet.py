#!/usr/bin/env python
_HOME_PATH = '/home/pi/tweet/'

# Import modules
from TwitterAPI import TwitterAPI
import ConfigParser
import picamera

# Custom Classes
from Photo import Graffcam
from TwitterActions import TA

# Load config file
config = ConfigParser.RawConfigParser()
config.read(_HOME_PATH + '_config.cfg')

# Set up API
api = TwitterAPI(
	config.get('twitter', 'consumer_key'),
	config.get('twitter', 'consumer_secret'),
	config.get('twitter', 'access_token_key'),
	config.get('twitter', 'access_token_secret')
)

camera = picamera.PiCamera()

# Get the last mention
last_mention_id = config.get('mentions', 'last_id')

# Get all the mentions since the last mention
mentions = api.request('statuses/mentions_timeline', {'since_id': last_mention_id}).json()

if mentions :

	for item in reversed(mentions):
		# Set the last id to that tweet
		last_mention_id = item['id']

		# Make a user
		user = item['user']

		# Take a picture
		graffcam = Graffcam(_HOME_PATH, camera)
		media = graffcam.capture_photo(user)

		# Upload the media
		media_upload = TA(_HOME_PATH, api).upload_media(media)

		# Build the status and send
		status = 'Hello @%s - here is a nice picture' % (user['screen_name'])

		if media_upload.status_code == 200:
			media_id = media_upload.json()['media_id']
			r = api.request('statuses/update', {'status':status, 'media_ids': media_id})
			print r.json()

	config.set('mentions', 'last_id', last_mention_id)

	# Write the data
	with open(_HOME_PATH + '_config.cfg', 'w') as f:
	  config.write(f)
