__author__ = 'Jesse'

from wsgiref.simple_server import make_server

import networkInfo

import argparse
argParseHandle = argparse.ArgumentParser()
argParseHandle.add_argument("-d", help="enables debug mode", action="store_true")
args = argParseHandle.parse_args()
if args.d:
	debugMode = True
else:
	debugMode = False

port = 9000

if debugMode:
	ip = networkInfo.getIpSocket()
	print("DEBUG MODE ENABLED")
else:
	ip = networkInfo.get_lan_ip()


def main():
	print("Serving on: http://" + str(ip) + ":" + str(port))
	httpd = make_server(ip, port, webHandler)
	httpd.serve_forever()


class webHandler:
	def __init__(self, environ, start_response):
		self.environ = environ
		self.start = start_response

	def __iter__(self):
		path = self.environ['PATH_INFO']

		if path == "/":
			return self.GET_index()
		if path == "/post":
			return self.rawPostInput()
		if path == "/hi":
			return self.GET_hi()
		else:
			return self.notfound()


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


	def GET_index(self):
		output = ['<pre>']

		#create a simple form:
		output.append('<form method="post">')
		output.append('<input type="radio" name="command" value = "create">')
		output.append('<input type="radio" name="command" value = "update">')
		output.append('<input type="radio" name="command" value = "delete">')
		output.append('<input type="text" name="input">')
		output.append('<input type="submit">')
		output.append('</form>')

		# command=create&input=someTextHere

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
		response_headers = [('Content-type', 'text/html'), ('Content-Length', str(output_len))]
		self.start(status, response_headers)

		yield ''.join(output)

	def GET_hi(self):
		output = ['']

		#create a simple form:
		output.append('hi')

		output_len = sum(len(line) for line in output)

		status = '200 OK'
		response_headers = [('Content-type', 'text/html'), ('Content-Length', str(output_len))]
		self.start(status, response_headers)

		yield ''.join(output)


	def notfound(self):
		status = '404 Not Found'
		response_headers = [('Content-type', 'text/plain')]
		self.start(status, response_headers)
		yield "Not Found\n"


if __name__ == "__main__":  # Runs Script
	main()