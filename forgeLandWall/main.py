from wsgiref.simple_server import make_server

import settings


__author__ = 'Jesse'

import dbSetup
import views
import dbInterface




def main():
	ip = settings.getIpAddress()
	port = settings.globalVars._portNumber
	dbSetup.setupDB()

	# TEST CODE

	# dbObj = models.messageModel()
	# dbObj.message("cats")

	# dbObj2 = models.messageModel(21)
	# dbObj2.message("newMessage")
	#
	# dbObj3 = models.messageModel(20)
	# dbObj3.deleteRecord()
	#
	# dbObj4 = models.messageModel(message="fuck")
	# print(dbObj4.message() + " " + dbObj4.getTimestamp())
	#
	# dbObj4 = models.messageModel(message="new")
	# print(dbObj4.message() + " " + dbObj4.getTimestamp())
	#
	# msg = models.messageModel(30)
	# print(msg.message() + msg.getTimestamp())


	print(dbInterface.getMessagesFromDBasJSONArray(5))
	print(dbInterface.getMessagesFromDBasJSONObjectArray(5))

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