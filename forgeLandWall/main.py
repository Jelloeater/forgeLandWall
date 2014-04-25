import dbSetup

__author__ = 'Jesse'

import argparse

import networkInfo
import views
# import dbInterface
# FIXME BROKEN

def isDebugMode():
	argParseHandle = argparse.ArgumentParser()
	argParseHandle.add_argument("-d", help="enables debug mode", action="store_true")
	args = argParseHandle.parse_args()
	if args.d:
		return True
	else:
		return False

def preBoot():
	if isDebugMode():
		print("DEBUG MODE ENABLED")
		return networkInfo.getIpSocket()
	else:
		return networkInfo.get_lan_ip()


class globalVars():
	def __init__(self):
		pass
	_debugMode = isDebugMode()
	_dbPath = "main.db"

def main():
	globalVars.debugMode = isDebugMode()
	ip = preBoot()
	port = 9000
	dbSetup.setupDB()

	# TEST CODE
	import models

	# dbObj = models.messageModel()
	# dbObj.message("cats")

	dbObj2 = models.messageModel(21)
	dbObj2.message("newMessage")

	dbObj3 = models.messageModel(20)
	dbObj3.deleteRecord()

	dbObj4 = models.messageModel(message="fuck")
	print(dbObj4.message() + " " + dbObj4.getTimestamp())

	dbObj4 = models.messageModel(message="new")
	print(dbObj4.message() + " " + dbObj4.getTimestamp())

	msg = models.messageModel(30)
	print(msg.message() + msg.getTimestamp())


# dbInterface.getMessagesFromDB()  # BROKEN
# FIXME Move db connection to db interface class, that way we can call dbInterface methods from main



# print("Serving on: http://" + str(ip) + ":" + str(port))
# httpd = make_server(ip, port, webHandler)
# httpd.serve_forever()


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