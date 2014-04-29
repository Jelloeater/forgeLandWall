from wsgiref.simple_server import make_server
import forgeLandWall.settings as settings

__author__ = 'Jesse'

import forgeLandWall.dbSetup as dbSetup
import forgeLandWall.views as views


def main():
	ip = settings.getIpAddress()
	port = settings.globalVars.portNumber
	dbSetup.setupDB()

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