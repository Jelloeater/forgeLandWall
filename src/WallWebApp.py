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


def webHandler(environ, start_response):
	# Sets up HTML environment
	output = ['<pre>']

	#create a simple form:
	output.append('<form method="post">')
	output.append('<input type="text" name="inputBox">')
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