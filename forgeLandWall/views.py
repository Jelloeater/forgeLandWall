import datetime
from forgeLandWall.controler import webControl
from forgeLandWall.models import messageModel


__author__ = 'Jesse'

import logging


class JSON(webControl):
	""" Forwards all JSON related HTTP requests to controller methods"""
	@classmethod
	def getMessages(cls, self):
		"""Handles text JSON GET requests
		GETS should be in the format server/raw/numberOfPostsToGetViaJSON"""
		logging.debug("getMessages")
		output = ['']
		path = self.environ['PATH_INFO']
		path = str(path)
		if path is not "/":	path = path.split('/')

		# MAIN PROCESSING HERE!
		numberToGet = int(path[2])
		logging.debug('Number To Get:' + str(numberToGet))
		output.append(cls.getJSONmsgs(numberToGet))  # Calls controller

		output_len = sum(len(line) for line in output)
		status = '200 OK'
		response_headers = [('Content-type', 'text/text'), ('Content-Length', str(output_len))]
		self.start(status, response_headers)
		yield ''.join(output)

	@classmethod
	def getMessage(cls, self):
		"""Handles all text JSON GET requests
		GETS should be in the format /msg/indexToGet"""
		logging.debug("getSingleMessage")
		output = ['']
		path = self.environ['PATH_INFO']
		path = str(path)
		if path is not "/": path = path.split('/')

		# MAIN PROCESSING HERE!
		indexToGet = int(path[2])
		logging.debug('Index To Get:' + str(indexToGet))
		output.append(str(webControl.getSingleMsg(indexToGet)))  # Calls controller

		output_len = sum(len(line) for line in output)
		status = '200 OK'
		response_headers = [('Content-type', 'text/text'), ('Content-Length', str(output_len))]
		self.start(status, response_headers)
		yield ''.join(output)

	@classmethod
	def POST_Messages(cls, self):
		"""Handles all text JSON PUT requests
		PUT should be in the format create=message, edit=index+message=newmessage, delete=index """
		logging.debug('JSON PUTs')
		output = ['']

		try:
			request_body_size = int(self.environ.get('CONTENT_LENGTH', 0))
		except ValueError:
			request_body_size = 0
		request_body = self.environ['wsgi.input'].read(request_body_size)

		if request_body_size != 0:
			cls.postControl(request_body)
			output.append('Request Received')
			# FIXME Should reply with url of index for create
		else:
			output.append('Empty Request')
			logging.warning('Empty Request Body')


		output_len = sum(len(line) for line in output)
		status = '200 OK'
		response_headers = [('Content-type', 'text/text'), ('Content-Length', str(output_len))]
		self.start(status, response_headers)
		yield ''.join(output)

	@classmethod
	def getMessagesSearch(cls, self):
		""" Calls search function and adds returned JSON to HTML output
		GETS should be in the format /search/messagesToSearchFor"""
		logging.debug("searchMessageJSON")
		output = ['']
		path = self.environ['PATH_INFO']
		path = str(path)
		if path is not "/": path = path.split('/')

		# MAIN PROCESSING HERE!
		msgToSearchFor = path[2]
		logging.debug('Messages To Get:' + str(msgToSearchFor))
		output.append(str(webControl.searchForMessagesJSON(msgToSearchFor)))  # Calls controller

		output_len = sum(len(line) for line in output)
		status = '200 OK'
		response_headers = [('Content-type', 'text/text'), ('Content-Length', str(output_len))]
		self.start(status, response_headers)
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
			output.append('<form method="post">'
			              'Create<input type="text" name="create">'
			              '<input type="submit"></form>')
		if formType == "edit":
			output.append('<form method="post">'
			              'Edit<input type="text" name="edit">'
			              'Index<input type="text" name="index">'
			              '<input type="submit"></form>')
		if formType == "delete":
			output.append('<form method="post">Delete(index)<input type="text" name="delete"><input type="submit"></form>')
		return output

	@classmethod
	def getMessagesTable(cls, output):
		""" Adds all messages to the HTML output for display"""
		logging.debug("Getting messages")
		# TODO Should move this code to the controller? (It's really short though -_-)

		output.append("<table><tr><th>Message</th><th>Timestamp</th><th>Index</th></tr>")

		msgList = cls.getMessagesFromDB()
		for x in msgList:
			message = str(messageModel.message(x))  # Fields stored as unicode, just to make life hard -_-
			timeStamp = str(messageModel.getTimestamp(x))
			msgIndex = str(messageModel.getIndex(x))
			# Cannot use cls.message to call, it needs to directly access its associated class

			output.append('<tr>')
			output.append('<td>' + message + '</td>')
			output.append('<td>' + timeStamp + '</td>')
			output.append('<td>' + msgIndex + '</td>')
			output.append('</tr>')

		output.append('</table>')
		return output

	@staticmethod
	def getFooter(output):
		str(datetime.datetime.now().replace(microsecond=0))
		output.append('<hr>Retrieved @ ' + str(datetime.datetime.now().replace(microsecond=0)))
		return output


class HTTP(HTMLHelper):
	"""Handles all web and text requests over HTTP"""
	@classmethod
	def GET_MainIndex(cls, self):
		""" HTML for create new message view + POST controller"""
		output = HTMLHelper.getHeader()

		output = HTMLHelper.getForm("create", output)

		output = HTMLHelper.getMessagesTable(output)
		# command=create&input=someTextHere
		# If we detect input, do this
		if self.environ['REQUEST_METHOD'] == 'POST':
			try:
				request_body_size = int(self.environ.get('CONTENT_LENGTH', 0))
			except ValueError:
				request_body_size = 0

			request_body = self.environ['wsgi.input'].read(request_body_size)
			cls.postControl(request_body)

		output = HTMLHelper.getFooter(output)

		output = ''.join(output)

		output_len = sum(len(line) for line in output)
		status = '200 OK'
		response_headers = [('Content-type', 'text/html'), ('Content-Length', str(output_len))]
		self.start(status, response_headers)
		yield ''.join(output)

	@classmethod
	def GET_edit(cls, self):
		""" HTML for create new message view + POST controller"""
		output = HTMLHelper.getHeader()

		output = HTMLHelper.getForm("edit", output)

		output = HTMLHelper.getMessagesTable(output)
		# command=create&input=someTextHere
		# If we detect input, do this
		if self.environ['REQUEST_METHOD'] == 'POST':
			try:
				request_body_size = int(self.environ.get('CONTENT_LENGTH', 0))
			except ValueError:
				request_body_size = 0

			request_body = self.environ['wsgi.input'].read(request_body_size)
			cls.postControl(request_body)

		output = HTMLHelper.getFooter(output)

		output = ''.join(output)

		output_len = sum(len(line) for line in output)
		status = '200 OK'
		response_headers = [('Content-type', 'text/html'), ('Content-Length', str(output_len))]
		self.start(status, response_headers)
		yield ''.join(output)

	@classmethod
	def GET_delete(cls, self):
		""" HTML for create new message view + POST controller"""
		output = HTMLHelper.getHeader()

		output = HTMLHelper.getForm("delete", output)

		output = HTMLHelper.getMessagesTable(output)
		# command=create&input=someTextHere
		# If we detect input, do this
		if self.environ['REQUEST_METHOD'] == 'POST':
			try:
				request_body_size = int(self.environ.get('CONTENT_LENGTH', 0))
			except ValueError:
				request_body_size = 0

			request_body = self.environ['wsgi.input'].read(request_body_size)
			cls.postControl(request_body)

		output = HTMLHelper.getFooter(output)

		output = ''.join(output)

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
