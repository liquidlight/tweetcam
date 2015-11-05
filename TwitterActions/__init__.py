import os
import sys

class TA():
	_PHOTO_HASHTAGS = ['snap']

	def __init__(self, home_path, api, logging):
		self.api = api
		self.home_path = home_path
		self.logging = logging

	def check_status(self, request):
		print request.text
		if request.status_code < 200 or request.status_code > 299:
			print(request.status_code)
			print(request.text)
			sys.exit(0)

	def is_photo(self, tweet):
		e = tweet['entities']
		photo = False
		if e['hashtags']:
			for hashtag in e['hashtags']:
				if any(hashtag['text'] in s for s in self._PHOTO_HASHTAGS):
					photo = True

		return photo

	def upload_image(self, filename):
		# Upload a file
		file = open(filename, 'rb')
		data = file.read()

		self.logging.info('Uploading picture')
		request = self.api.request('media/upload', None, {'media': data})
		self.logging.info('Picture request: ' + request.json())
		return request

	def upload_video(self, filename):
		# Upload a video
		bytes_sent = 0
		total_bytes = os.path.getsize(filename)
		file = open(filename, 'rb')

		# Initial request
		request = self.api.request('media/upload', {'command':'INIT', 'media_type':'video/mp4', 'total_bytes':total_bytes})
		self.check_status(request)

		media_id = request.json()['media_id']
		segment_id = 0

		# Chunk and upload video
		while bytes_sent < total_bytes:
			chunk = file.read(4*1024*1024)

			request = self.api.request('media/upload', {'command':'APPEND', 'media_id':media_id, 'segment_index':segment_id}, {'media':chunk})
			self.check_status(request)

			segment_id = segment_id + 1
			bytes_sent = file.tell()

			print('[' + str(total_bytes) + ']', str(bytes_sent))

		request = self.api.request('media/upload', {'command':'FINALIZE', 'media_id':media_id})
		self.check_status(request)

		return request
