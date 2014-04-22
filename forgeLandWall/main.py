__author__ = 'Jesse'

import argparse

from forgeLandWall import dbInterface
import networkInfo
import views


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


def main():
	isDebugMode()
	ip = preBoot()
	port = 9000
	dbInterface.dbHelper.setupDB()

	import models

	dbObj = models.messageModel()
	dbObj.message("Fuck yo couch")

	dbObj2 = models.messageModel(10)
	dbObj2.message("newMessage")

	dbObj3 = models.messageModel(3)
	dbObj3.deleteRecord()

	dbObj4 = models.messageModel(5)
	print(dbObj4.message())


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