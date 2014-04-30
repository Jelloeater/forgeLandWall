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
		print(path)
		path = str(path)

		if path is not "/":
			path = path.split('/')
			print(path[0])
			print(path[1])
			# print(path[2])
			pathLength = len(path)
			print(pathLength)

			if path[1] == "hi"and pathLength <= 2:
				return views.HTTP.GET_hi(self)
			if path[1] == "rawJSON"and pathLength <= 2:
				# TODO Split string for amount
				return views.JSONTxt.getJSON(self)
			else:
				return views.HTTP.notFound(self)
		else:
			return views.HTTP.GET_MainIndex(self)
		# /         Create
		# /update   update
		# /delete   delete
		# FIXME Add specific pages for tasks

if __name__ == "__main__":  # Runs Script
	main()

class postControl:
	@staticmethod
	def readPost(postMessageIn):
		pass
		# FIXME Write filter method
	@staticmethod
	def createRecord(messageIn = None):
		pass
	# TODO Write Create call
	@staticmethod
	def updateRecord(messageIn = None):
		pass
	# TODO write update call
	@staticmethod
	def deleteRecord(messageIn = None):
		pass
	# TODO write delete call