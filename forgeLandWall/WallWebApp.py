from forgeLandWall.views import rawPostInput, GET_index, GET_hi, notfound

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
			return GET_index(self)
		if path == "/post":
			return rawPostInput(self)
		if path == "/hi":
			return GET_hi(self)
		else:
			return notfound(self)


if __name__ == "__main__":  # Runs Script
	main()