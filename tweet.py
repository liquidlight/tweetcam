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
		username = user['screen_name']

		# Take a picture
		graffcam = Graffcam(_HOME_PATH, camera)
		#media = graffcam.capture_photo(username)
		media = graffcam.record_video(username)

		# Upload the media
		#media_upload = TA(_HOME_PATH, api).upload_image(media)
		media_upload = TA(_HOME_PATH, api).upload_video(media)

		# Build the status and send
		status = 'Hello @%s - here is a nice video' % (username)
		print '[status: Posting]'
		if media_upload.status_code > 199 or media_upload.status_code < 300:
			r = api.request('statuses/update', {'status': status, 'in_reply_to_status_id': item['id'], 'media_ids': media_upload.json()['media_id']})
			print r.json()

	config.set('mentions', 'last_id', last_mention_id)

	#Write the data
	with open(_HOME_PATH + '_config.cfg', 'w') as f:
	 config.write(f)
