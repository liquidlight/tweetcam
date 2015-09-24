import os
import sys

class TA():
	def __init__(self, home_path, api):
		self.api = api
		self.home_path = home_path

	def check_status(self, request):
		if request.status_code < 200 or request.status_code > 299:
			print(request.status_code)
			print(request.text)
			sys.exit(0)

	def upload_image(self, filename):
		# Upload a file
		file = open(filename, 'rb')
		data = file.read()
		request = self.api.request('media/upload', None, {'media': data})
		return request

	def upload_video(self, filename):
		nbytes = os.path.getsize(filename)
		file = open(filename, 'rb')
		data = file.read()

		print '[status: Starting Upload]'
		request = self.api.request('media/upload', {'command':'INIT', 'media_type':'video/mp4', 'total_bytes': nbytes})
		self.check_status(request)

		media_id = request.json()['media_id']
		request = self.api.request('media/upload', {'command':'APPEND', 'media_id': media_id, 'segment_index':0}, {'media': data})
		self.check_status(request)

		print '[status: Finalising Upload]'
		request = self.api.request('media/upload', {'command':'FINALIZE', 'media_id': media_id})
		self.check_status(request)

		return request
