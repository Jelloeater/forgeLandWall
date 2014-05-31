import datetime
from controler import webControl
from models import messageModel
import logging
__author__ = 'Jesse'


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
		output.append(cls.getMessagesFromDBasJSONObjectArray(numberToGet))  # Calls controller

		output_len = sum(len(line) for line in output)
		status = '200 OK'
		response_headers = [('Content-type', 'text/html'), ('Content-Length', str(output_len))]
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
		output.append(str(cls.getMessageAsJSONObject(indexToGet)))  # Calls controller

		output_len = sum(len(line) for line in output)
		status = '200 OK'
		response_headers = [('Content-type', 'text/html'), ('Content-Length', str(output_len))]
		self.start(status, response_headers)
		yield ''.join(output)

	@classmethod
	def POST_Messages(cls, self):
		"""Handles all text JSON PUT requests
		PUT should be in the format create=message, edit=index+message=newmessage, delete=index """
		# logging.debug('JSON PUTs')
		output = ['']

		try:
			request_body_size = int(self.environ.get('CONTENT_LENGTH', 0))
		except ValueError:
			request_body_size = 0
		request_body = self.environ['wsgi.input'].read(request_body_size)

		if request_body_size != 0:
			returnValue = cls.postControl(request_body)
			output.append('Request Received (' + str(request_body) + ') : ' + str(returnValue))
			# FIXME Should reply with url of index for create
		else:
			output.append('Empty Request')
			logging.warning('Empty Request Body')


		output_len = sum(len(line) for line in output)
		status = '200 OK'
		response_headers = [('Content-type', 'text/html'), ('Content-Length', str(output_len))]
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
		response_headers = [('Content-type', 'text/html'), ('Content-Length', str(output_len))]
		self.start(status, response_headers)
		yield ''.join(output)

class HTMLHelper(webControl):
	@staticmethod
	def getHeader():
		# TODO Add search function (dbinterface.searchRecords should help)
		# Might need to generate separate page to handle request?
		output = []
		output.append('<pre>')
		output.append("ForgeLand Message Board: ")
		output.append(' <a href="/">Create</a>')
		output.append(' <a href="/edit">Edit</a>')
		output.append(' <a href="/delete">Delete</a>')
		output.append(' <a href="/search">Search</a>')
		output.append('<hr>')
		return output

	@staticmethod
	def getForm(formType, output):
		if formType == "create":
			output.append('<form method="post">'
			              '<input type="text" name="create" value="Message">'
			              '<input type="submit" value="Create" onclick="reloadPage()"></form>')
		if formType == "edit":
			output.append('<form method="post">'
			              '<input type="text" name="edit" value="New message">'
			              '<input type="text" name="index" value="Index">'
			              '<input type="submit" value="Edit"></form>')
		if formType == "delete":
			output.append('<form method="post">'
			              '<input type="text" name="delete" value="Index">'
			              '<input type="submit" value="Delete"></form>')

		if formType == "search":
			output.append('<form method="get">'
			              '<input type="text" name="q">'
			              '<input type="submit" value="Search"></form>')
		return output

	@classmethod
	def getMessagesTable(cls, output, search=None):
		""" Adds all messages to the HTML output for display"""
		logging.debug("Getting messages")
		# TODO Should move this code to the controller! (It's really short though -_-)

		output.append("<table><tr><th>Message</th><th>Timestamp</th><th>Index</th></tr>")

		if search is None:
			indexList = cls.getMessagesFromDB()
		else:
			indexList = cls.getMessagesFromDBsearch(search)

		for x in indexList:
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

	@classmethod
	def GET_search(cls, self):
		""" HTML for create new message view + POST controller"""
		output = HTMLHelper.getHeader()

		output = HTMLHelper.getForm('search', output)

		if self.environ['REQUEST_METHOD'] == 'GET':
			query = str(self.environ['QUERY_STRING'])
			if query.find('=') is not -1:
				query = query.split('=')
				search = query[1]
				if search == "":
					output = HTMLHelper.getMessagesTable(output)
				else:
					output.append('Searching for: ' + search)
					output = HTMLHelper.getMessagesTable(output, search)
			else:
				output = HTMLHelper.getMessagesTable(output)

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
		yield "Not Found"
