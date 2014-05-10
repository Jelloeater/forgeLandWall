from wsgiref.simple_server import make_server
import forgeLandWall.settings as settings
import forgeLandWall.dbSetup as dbSetup
import forgeLandWall.views as views
import logging

logging.basicConfig(format='%(levelname)s %(asctime)sZ  pid: %(process)s module: %(module)s   \t\t %(message)s',
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
	"""
	root      Create
	/edit     update
	/delete   delete
	"""
	def __init__(self, environ, start_response):
		self.environ = environ
		self.start = start_response

	def __iter__(self):
		path = self.environ['PATH_INFO']
		path = str(path)

		if path is not "/":
			path = path.split('/')

			if path[1] == "edit" and len(path) <= 2:
				return views.HTTP.GET_edit(self)
			if path[1] == "delete" and len(path) <= 2:
				return views.HTTP.GET_delete(self)
			if path[1] == "raw" and len(path) >= 3 and path[2].isdigit():  # GET POSTS| /raw/9000
				return views.JSON.getMessages(self)
			if path[1] == "raw" and len(path) <= 2:  # PUT POSTS| /raw [POST][create=x, delete=x]
				return views.JSON.putMessages(self)
			else:
				print('NOT FOUND')
				print(path[1])
				return views.HTTP.notFound(self)
		else:
			return views.HTTP.GET_MainIndex(self)

if __name__ == "__main__":  # Runs Script
	main()