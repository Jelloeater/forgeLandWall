__author__ = 'Jesse'
import dbInterface
# TODO Think about moving to modules down the road maybe?
class JSONTxt:
	@staticmethod
	def getJSON(numberToGet = 1):
		return dbInterface.getMessagesFromDBasJSONObjectArray(numberToGet)

class HTTP:

	@staticmethod
	def rawPostInput(self):
		output = ['']
		try:
			request_body_size = int(self.environ.get('CONTENT_LENGTH', 0))
		except ValueError:
			request_body_size = 0

		request_body = self.environ['wsgi.input'].read(request_body_size)
		print(request_body)

		output_len = sum(len(line) for line in output)

		status = '200 OK'
		response_headers = [('Content-type', 'text/text'), ('Content-Length', str(output_len))]
		self.start(status, response_headers)
		output.append("True")

		# TODO Add query output?
		yield ''.join(output)


	@staticmethod
	def GET_MainIndex(self):
		output = ['<pre>']

		#create a simple form:
		# TODO Add Universal Header call
		output.append('<form method="post">')
		# output.append('Create <input type="radio" name="command" value = "create">')
		# output.append('Update <input type="radio" name="command" value = "update">')
		# output.append('Delete <input type="radio" name="command" value = "delete">')
		output.append('CREATE<input type="text" name="create">')
		output.append('<input type="submit">')
		output.append('</form>')

		# command=create&input=someTextHere
		# If we detect input, do this
		# TODO call rawPostInput HERE?
		if self.environ['REQUEST_METHOD'] == 'POST':
			try:
				request_body_size = int(self.environ.get('CONTENT_LENGTH', 0))
			except ValueError:
				request_body_size = 0

			request_body = self.environ['wsgi.input'].read(request_body_size)

			# TODO If POST = update
			# show form data as received by POST:
			output.append('<h1>FORM DATA</h1>')
			output.append(request_body)
			print(request_body)

		output_len = sum(len(line) for line in output)

		status = '200 OK'
		response_headers = [('Content-type', 'text/html'), ('Content-Length', str(output_len))]
		self.start(status, response_headers)

		# TODO Add footer call

		yield ''.join(output)

	@staticmethod
	def GET_hi(self):
		output = ['']
		output.append('hi')

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