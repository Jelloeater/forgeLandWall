from forgeLandWall import dbInterface

__author__ = 'Jesse'

from wsgiref.simple_server import make_server

import networkInfo
import views

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
	dbInterface.setupDB()
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
			return views.GET_index(self)
		if path == "/post":
			return views.rawPostInput(self)
		if path == "/hi":
			return views.GET_hi(self)
		else:
			return views.notfound(self)


if __name__ == "__main__":  # Runs Script
	main()