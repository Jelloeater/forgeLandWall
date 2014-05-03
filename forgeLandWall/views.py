__author__ = 'Jesse'
import POSTController
# TODO Think about moving to modules down the road maybe?

class HTMLHelper():
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

	@staticmethod
	def getFooter(outputIn):
		output = outputIn
		import datetime
		str(datetime.datetime.now().replace(microsecond=0))
		output.append('<hr>Retrieved @ ' + str(datetime.datetime.now().replace(microsecond=0)))
		# TODO Add footer
		return output

class HTTP(HTMLHelper):
	@staticmethod
	def rawPostInput(self):
		output = ['']

		try:
			request_body_size = int(self.environ.get('CONTENT_LENGTH', 0))
		except ValueError:
			request_body_size = 0
		request_body = self.environ['wsgi.input'].read(request_body_size)

		path = self.environ['PATH_INFO']
		print('PATH: ')
		print(path)
		path = str(path)

		if path is not "/":	path = path.split('/')


		if request_body == "": # For GET's and empty POST's
		# In order to get here, the path HAS to be long enough to look for a record
		# NOTE: We are NOT re-splitting the path, just going off what we took from the main method
			try:
				output.append(POSTController.JSONTxt.getJSON(int(path[2])))
			except:
				output.append("ERROR - Path NaN")


		else: # We're getting a POST request
			# request_body = POST Message
			print('request Body')
			print(request_body)
			# TODO Create universal method for processing POST requests, a POST message splitter

			if request_body == "create":
				POSTController.postControl.createRecord("rawPOSTinput")


		output_len = sum(len(line) for line in output)
		status = '200 OK'
		response_headers = [('Content-type', 'text/text'), ('Content-Length', str(output_len))]
		self.start(status, response_headers)
		# TODO Add query output?
		yield ''.join(output)




	@staticmethod
	def GET_MainIndex(self):
		""" HTML for create new message view + POST controller"""
		output = HTMLHelper.getHeader()



		output = HTMLHelper.getForm("create", output)

		# command=create&input=someTextHere
		# If we detect input, do this
		# TODO call rawPostInput HERE?
		if self.environ['REQUEST_METHOD'] == 'POST':
			try:
				request_body_size = int(self.environ.get('CONTENT_LENGTH', 0))
			except ValueError:
				request_body_size = 0

			request_body = self.environ['wsgi.input'].read(request_body_size)
			# FIXME Call POSTcontroller
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

	@staticmethod
	def GET_delete(self):
		output = HTMLHelper.getHeader()


		output = HTMLHelper.getForm("delete", output)


		output = HTMLHelper.getFooter(output)
		output_len = sum(len(line) for line in output)
		status = '200 OK'
		response_headers = [('Content-type', 'text/html'), ('Content-Length', str(output_len))]
		self.start(status, response_headers)
		yield ''.join(output)