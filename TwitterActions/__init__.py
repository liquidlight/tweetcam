class TA():
	def __init__(self, api):
		self.api = api

	def upload_media(self, filename) :
		# Upload a file
		file = open(filename, 'rb')
		data = file.read()
		request = self.api.request('media/upload', None, {'media': data})
		return request
