# SETUP: Import classes
from TwitterAPI import TwitterAPI
import ConfigParser
import datetime
import picamera
import logging
import random
import json
import time
import os

# SETUP: Import Custom Classes
from Photo import Graffcam
from TwitterActions import TA

class GraffCam:

	def __init__(self):
		self.camera = picamera.PiCamera()

		# SETUP: Include config file
		self.config = ConfigParser.RawConfigParser()
		self._HOME_PATH = os.path.dirname(os.path.abspath(__file__)) + '/'
		self.config.read(self._HOME_PATH + '_config.cfg')
		self._DEBUG_MODE = self.config.get('setup', 'debug_mode')

		# SETUP: TwitterAPI (https://github.com/geduldig/TwitterAPI)
		self.api = TwitterAPI(
			self.config.get('twitter_api', 'consumer_key'),
			self.config.get('twitter_api', 'consumer_secret'),
			self.config.get('twitter_api', 'access_token_key'),
			self.config.get('twitter_api', 'access_token_secret')
		)

		# SETUP: Logging
		now = datetime.datetime.now()
		logfile_name = self._HOME_PATH + 'logs/' + str(now.year) + '-' + str(now.isocalendar()[1]) + '.log'
		logging.basicConfig(filename = logfile_name, level = logging.INFO, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		self.script_main = logging.getLogger('main')
		self.script_graffcam = logging.getLogger('graffcam')
		self.script_ta = logging.getLogger('ta')

	def GetMentions(self):
		last_mention_id = self.config.get('tweets', 'last_mention_id')
		mentions = self.api.request('statuses/mentions_timeline', {'since_id': last_mention_id}).json()
		return mentions

	def GetStream(self):
		stream = self.api.request('user')
		return stream

	def ActionTweet(self, tweet):
		print '[New Tweet] ' + tweet['text']

		# Initialise the camera
		script_main = self.script_main
		script_graffcam = self.script_graffcam
		script_ta = self.script_ta


		last_mention_id = tweet['id']

		# Make a user
		user = tweet['user']
		username = user['screen_name']

		if username != self.config.get('setup', 'twitter_username'):

			start_status = random.choice(json.loads(self.config.get('tweet_text', 'preperation')))
			start_status = start_status.replace('[[user]]', '@%s' % (username))
			start_post = self.api.request('statuses/update', {'status': start_status, 'in_reply_to_status_id': tweet['id']})
			time.sleep(5)

			#Initialise custom classes
			graffcam = Graffcam(self._HOME_PATH, self.camera, script_graffcam)
			ta = TA(self._HOME_PATH, self.api, script_ta)

			# If the tweet contains a photo trigger hashtag
			if ta.is_photo(tweet):
				media = graffcam.capture_photo(username)
				media_upload = ta.upload_image(media)
				status_pick = self.config.get('tweet_text', 'photo')
			else:
				media = graffcam.record_video(username)
				media_upload = ta.upload_video(media)
				status_pick = self.config.get('tweet_text', 'video')

			# Build the status and send
			status = random.choice(json.loads(status_pick))
			status = status.replace('[[user]]', '@%s' % (username))

			if self._DEBUG_MODE == 'False':
				if media_upload.status_code > 199 or media_upload.status_code < 300:
					post = self.api.request('statuses/update', {'status': status, 'in_reply_to_status_id': tweet['id'], 'media_ids': media_upload.json()['media_id']})
			else:
				print 'Original tweet: %s' % (tweet['text'])
				print 'Status: %s [media: %s] ' % (status, media)
		else:
			print 'Tweet by Graffcam, not actioning anything'
		# Update the last ID
		if self._DEBUG_MODE == 'False':
			self.config.set('tweets', 'last_mention_id', last_mention_id)
			with open(self._HOME_PATH + '_config.cfg', 'w') as f:
				self.config.write(f)
