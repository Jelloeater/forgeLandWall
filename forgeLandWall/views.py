import datetime
from forgeLandWall.controler import webControl
from forgeLandWall.models import messageModel

__author__ = 'Jesse'

import logging
from settings import globalVars
logging.basicConfig(format=globalVars.logFormat, level=logging.DEBUG)


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

		cls.postControl(request_body)
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
			output.append('<form method="post">Create<input type="text" name="create"'
			              'onsubmit="setTimeout(function () { window.location.reload(); }, 10)"'
			              '><input type="submit"></form>')
		if formType == "edit":
			output.append('<form method="post">Edit<input type="text" name="edit"><input type="submit"></form>')
		if formType == "delete":
			output.append('<form method="post">Delete<input type="text" name="delete"><input type="submit"></form>')
		return output

	@classmethod
	def getMessagesTable(cls, output):
		""" Adds all messages to the HTML output for display"""
		# TODO Should move this code to the controller? (It's really short though -_-)

		output.append("<table><tr><th>Message</th><th>Timestamp</th></tr>")

		msgList = cls.getMessagesFromDB()
		for x in msgList:
			message = str(messageModel.message(x))  # Fields stored as unicode, just to make life hard -_-
			timeStamp = str(messageModel.getTimestamp(x))
			# Cannot use cls.message to call, it needs to directly access its associated class
			output.append('<tr><td>' + message + '</td><td>' + timeStamp + '</td></tr>')
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
