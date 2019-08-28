class FileReader:
	"""Class for reading data from the file"""

	def __init__(self, path):
		self.path = path

	def read(self):
		try:
			with open(self.path, 'r') as f:
				data = f.read()
		except IOError:
			data = ''
		
		return data


if __name__ == '__main__':
	reader = FileReader('example.txt')
	print(reader.read())
