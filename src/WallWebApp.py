__author__ = 'Jesse'

import socket
from wsgiref.simple_server import make_server
import dbInterface

port = 9000
ip = socket.gethostbyname(socket.gethostname())


def main():
	print("Serving on: " + str(ip) + ":" + str(port))
	httpd = make_server(ip, port, webHandler)
	httpd.serve_forever()


class webHandler:
	def __init__(self, environ, start_response):
		self.environ = environ
		self.start = start_response

	def __iter__(self):
		path = self.environ['PATH_INFO']

		if self.environ['REQUEST_METHOD'] == 'POST':
			self.POST()

		if path == "/":
			return self.GET_index()
		else:
			return self.notfound()


	def POST(self):
		try:
			request_body_size = int(self.environ.get('CONTENT_LENGTH', 0))
		except ValueError:
			request_body_size = 0

		request_body = self.environ['wsgi.input'].read(request_body_size)


	def GET_index(self):
		output = ['<pre>']

		#create a simple form:
		output.append('<form method="post">')
		output.append('<input type="text" name="inputBox">')
		output.append('<input type="text" name="inputBox2">')
		output.append('<input type="submit">')
		output.append('</form>')


		if self.environ['REQUEST_METHOD'] == 'POST':
			try:
				request_body_size = int(self.environ.get('CONTENT_LENGTH', 0))
			except ValueError:
				request_body_size = 0

			request_body = self.environ['wsgi.input'].read(request_body_size)

			# show form data as received by POST:
			output.append('<h1>FORM DATA</h1>')
			output.append(request_body)
			print(request_body)

		output_len = sum(len(line) for line in output)

		status = '200 OK'
		response_headers = [('Content-type', 'text/html'), ('Content-Length', str(output_len)]
		self.start(status, response_headers)
		yield output



	def notfound(self):
		status = '404 Not Found'
		response_headers = [('Content-type', 'text/plain')]
		self.start(status, response_headers)
		yield "Not Found\n"


def webHandlerOLD(environ, start_response):
	# Sets up HTML environment
	output = ['<pre>']

	#create a simple form:
	output.append('<form method="post">')
	output.append('<input type="text" name="inputBox">')
	output.append('<input type="text" name="inputBox2">')
	output.append('<input type="submit">')
	output.append('</form>')

	if environ['REQUEST_METHOD'] == 'POST':
		try:
			request_body_size = int(environ.get('CONTENT_LENGTH', 0))
		except ValueError:
			request_body_size = 0

		request_body = environ['wsgi.input'].read(request_body_size)

		# show form data as received by POST:
		output.append('<h1>FORM DATA</h1>')
		output.append(request_body)
		print(request_body)



	output_len = sum(len(line) for line in output)
	start_response('200 OK', [('Content-type', 'text/html'),
	                          ('Content-Length', str(output_len))])
	return output


main()