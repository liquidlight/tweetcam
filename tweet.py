#!/usr/bin/env python
_HOME_PATH = '/home/pi/tweet/'
_PHOTO_TWEETS = [
	'Looking good [[user]]!',
	'Very nice shoes [[user]]!'
]
_VIDEO_TWEETS = [
	'Here is your #graffcam short [[user]]',
	'Enjoy your film [[user]]'
]
_DEBUG = False

# Import modules
from TwitterAPI import TwitterAPI
import ConfigParser
import picamera
import random
import logging
import datetime

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

# Set up the logging
now = datetime.datetime.now()
logfile_name = _HOME_PATH + 'logs/' + str(now.year) + '-' + str(now.isocalendar()[1]) + '.log'
logging.basicConfig(filename = logfile_name, level = logging.INFO, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

script_main = logging.getLogger('main')
script_graffcam = logging.getLogger('graffcam')
script_ta = logging.getLogger('ta')

# Initialise the camera
camera = picamera.PiCamera()

# Get the last mention
last_mention_id = config.get('mentions', 'last_id')
script_main.info('Last status ID: %s' % last_mention_id)

# Get all the mentions since the last mention
script_main.info('Get metions with last mention ID of: %s' % last_mention_id)
mentions = api.request('statuses/mentions_timeline', {'since_id': last_mention_id}).json()


if mentions :

	# Reverse the mentions (so oldest first)
	for item in reversed(mentions):

		# Set the last id to that tweet
		last_mention_id = item['id']
		script_main.info('Original mention: %s' % item['text'])

		# Make a user
		user = item['user']
		username = user['screen_name']

		# Initialise custom classes
		graffcam = Graffcam(_HOME_PATH, camera, script_graffcam)
		ta = TA(_HOME_PATH, api, script_ta)

		# If the tweet contains a photo trigger hashtag
		if ta.is_photo(item):
			script_main.info('Tweet is a photo [%s]' % item['id'])
			media = graffcam.capture_photo(username)
			media_upload = ta.upload_image(media)
			status_pick = _VIDEO_TWEETS
		else:
			script_main.info('Tweet is a video [%s]' % item['id'])
			media = graffcam.record_video(username)
			media_upload = ta.upload_video(media)
			status_pick = _VIDEO_TWEETS

		# Build the status and send
		status = random.choice(status_pick)
		status = status.replace('[[user]]', '@%s' % (username))
		script_main.info('Posting status: %s' % status)

		if _DEBUG == False:
			if media_upload.status_code > 199 or media_upload.status_code < 300:
				post = api.request('statuses/update', {'status': status, 'in_reply_to_status_id': item['id'], 'media_ids': media_upload.json()['media_id']})
				script_main.info('Posted to %s with code %s]' % (username, post.status_code))
		else:
			print 'Original tweet: %s' % (item['text'])
			print 'Status: %s [media: %s] ' % (status, media)

	# Update the last ID
	if _DEBUG == False:
		config.set('mentions', 'last_id', last_mention_id)
		with open(_HOME_PATH + '_config.cfg', 'w') as f:
			config.write(f)
