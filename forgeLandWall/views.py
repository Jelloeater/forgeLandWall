import datetime
from forgeLandWall.controler import webControl

__author__ = 'Jesse'


class JSON(webControl):
	@classmethod
	def getMessages(cls, self):
		"""Handles all text JSON GET requests
		GETS should be in the format server/raw/numberOfPostsToGetViaJSON"""
		output = ['']

		path = self.environ['PATH_INFO']
		path = str(path)
		if path is not "/":	path = path.split('/')

		# MAIN PROCESSING HERE!
		numberToGet = int(path[2])
		output.append(cls.getJSON(numberToGet))  # Calls controller

		output_len = sum(len(line) for line in output)
		status = '200 OK'
		response_headers = [('Content-type', 'text/text'), ('Content-Length', str(output_len))]
		self.start(status, response_headers)
		# TODO Add query output?
		yield ''.join(output)

	@classmethod
	def putMessages(cls, self):
		"""Handles all text JSON PUT requests
		PUT should be in the format create=x, edit=x, delete=x """
		output = ['']

		try:
			request_body_size = int(self.environ.get('CONTENT_LENGTH', 0))
		except ValueError:
			request_body_size = 0
		request_body = self.environ['wsgi.input'].read(request_body_size)

		cls.postSplitter(request_body)
		output.append('Request Received')

		output_len = sum(len(line) for line in output)
		status = '200 OK'
		response_headers = [('Content-type', 'text/text'), ('Content-Length', str(output_len))]
		self.start(status, response_headers)
		# TODO Add query output?
		yield ''.join(output)


class HTMLHelper(webControl):
	@staticmethod
	def getHeader():
		output = ['<pre>']
		output.append("ForgeLand Message Board: ")
		output.append(' <a href="/">View/Create</a>')
		output.append(' <a href="/edit">Edit</a>')
		output.append(' <a href="/delete">Delete</a> <hr>')
		return output

	@staticmethod
	def getForm(formType, output):
		if formType == "create":
			output.append('<form method="post">CREATE<input type="text" name="create"><input type="submit"></form>')
		if formType == "edit":
			output.append('<form method="post">CREATE<input type="text" name="edit"><input type="submit"></form>')
		if formType == "delete":
			output.append('<form method="post">CREATE<input type="text" name="delete"><input type="submit"></form>')
		return output

	@classmethod
	def getMessages(cls, output):
		msgList = cls.getMessagesFromDB()

	@staticmethod
	def getFooter(output):
		str(datetime.datetime.now().replace(microsecond=0))
		output.append('<hr>Retrieved @ ' + str(datetime.datetime.now().replace(microsecond=0)))
		return output


class HTTP(HTMLHelper):
	"""Handles all web and text requests over HTTP"""
	@staticmethod
	def GET_MainIndex(self):
		""" HTML for create new message view + POST controller"""
		output = HTMLHelper.getHeader()

		output = HTMLHelper.getForm("create", output)

		# command=create&input=someTextHere
		# If we detect input, do this
		if self.environ['REQUEST_METHOD'] == 'POST':
			try:
				request_body_size = int(self.environ.get('CONTENT_LENGTH', 0))
			except ValueError:
				request_body_size = 0

			request_body = self.environ['wsgi.input'].read(request_body_size)
			# FIXME Call Controller.webControl.POSTSplitter
			print(request_body)
			# TODO If POST = update
			# show form data as received by POST:
			output.append('<h1>FORM DATA</h1>')
			output.append(request_body)

		output = HTMLHelper.getFooter(output)
		output_len = sum(len(line) for line in output)
		status = '200 OK'
		response_headers = [('Content-type', 'text/html'), ('Content-Length', str(output_len))]
		self.start(status, response_headers)
		yield ''.join(output)

	@staticmethod
	def GET_edit(self):
		output = HTMLHelper.getHeader()

		output = HTMLHelper.getForm("edit", output)

		output = HTMLHelper.getFooter(output)

		# FIXME Call Controller.webControl.POSTSplitter
		output_len = sum(len(line) for line in output)
		status = '200 OK'
		response_headers = [('Content-type', 'text/html'), ('Content-Length', str(output_len))]
		self.start(status, response_headers)
		yield ''.join(output)

	@staticmethod
	def GET_delete(self):
		output = HTMLHelper.getHeader()

		output = HTMLHelper.getForm("delete", output)

		output = HTMLHelper.getFooter(output)
		# FIXME Call Controller.webControl.POSTSplitter
		output_len = sum(len(line) for line in output)
		status = '200 OK'
		response_headers = [('Content-type', 'text/html'), ('Content-Length', str(output_len))]
		self.start(status, response_headers)
		yield ''.join(output)

	@staticmethod
	def notFound(self):
		status = '404 Not Found'
		response_headers = [('Content-type', 'text/plain')]
		self.start(status, response_headers)
		yield "Not Found\n"
