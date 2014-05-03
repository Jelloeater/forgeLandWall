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


class webHandler():
	def __init__(self, environ, start_response):
		self.environ = environ
		self.start = start_response

	def __iter__(self):
		path = self.environ['PATH_INFO']
		print('PATH: ')
		print(path)
		path = str(path)

		if path is not "/":
			path = path.split('/')
			print(path[0])
			print(path[1])
			# print(path[2])
			pathLength = len(path)
			print(pathLength)

			if path[1] == "edit"and pathLength <= 2:
				return views.HTTP.GET_edit(self)
			if path[1] == "delete"and pathLength <= 2:
				return views.HTTP.GET_delete(self)
			if path[1] == "rawJSON"and pathLength <= 2:
				# TODO Split string for amount
				return views.JSONTxt.getJSON(self)
			else:
				return views.HTTP.notFound(self)
		else:
			print('hi')
			return views.HTTP.GET_MainIndex(self)

		# root      Create
		# /edit   update
		# /delete   delete
		# FIXME Add specific pages for tasks

if __name__ == "__main__":  # Runs Script
	main()