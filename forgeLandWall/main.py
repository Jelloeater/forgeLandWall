from wsgiref.simple_server import make_server
import forgeLandWall.settings as settings
import forgeLandWall.dbSetup as dbSetup
import forgeLandWall.views as views
import logging

logging.basicConfig(format="[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(lineno)s)",
					level=logging.DEBUG)

__author__ = 'Jesse'


def main():
	ip = settings.getIpAddress()
	port = settings.globalVars.portNumber
	dbSetup.setupDB()

	logging.info("Serving on: http://" + str(ip) + ":" + str(port))
	httpd = make_server(ip, port, webHandler)
	httpd.serve_forever()


class webHandler():
	""" Sends HTTP requests to the proper functions"""
	def __init__(self, environ, start_response):
		self.environ = environ
		self.start = start_response

	def __iter__(self):
		path = self.environ['PATH_INFO']
		logging.info('Accessing' + path)

		if path is not "/":
			path = path.split('/')
			logging.debug('PathList: ' + str(path))

			if len(path) == 2:
				if path[1] == "edit":
					return views.HTTP.GET_edit(self)
				if path[1] == "delete":
					return views.HTTP.GET_delete(self)
				if path[1] == "post":  # POST Posts| /post [POST][create=x, delete=x]
					logging.debug('POST Messages')
					return views.JSON.POST_Messages(self)

			if len(path) == 3 and path[1] == "search" and str(path[2]):  # GET Search Messages| /get/msgToSearchFor
				logging.debug('GET Messages')
				return views.JSON.getMessagesSearch(self)

			if len(path) == 3 and path[1] == "get" and path[2].isdigit():  # GET Messages| /get/10
				logging.debug('GET Messages')
				return views.JSON.getMessages(self)

			if len(path) == 3 and path[1] == "msg" and path[2].isdigit():  # GET Message| /msg/234
				logging.debug('GET Single Message')
				return views.JSON.getMessage(self)

			else:
				logging.info('URL NOT FOUND: /' + str(path[1]))
				return views.HTTP.notFound(self)
		else:
			return views.HTTP.GET_MainIndex(self)

if __name__ == "__main__":  # Runs Script
	main()