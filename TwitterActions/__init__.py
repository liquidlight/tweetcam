class TA():
	def __init__(self, home_path, api):
		self.api = api
		self.home_path = home_path

	def upload_media(self, filename) :
		# Upload a file
		file = open(filename, 'rb')
		data = file.read()
		request = self.api.request('media/upload', None, {'media': data})
		return request
