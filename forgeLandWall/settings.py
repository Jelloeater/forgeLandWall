import argparse

from forgeLandWall import networkInfo


__author__ = 'Jesse Laptop'


def isDebugMode():
	argParseHandle = argparse.ArgumentParser()
	argParseHandle.add_argument("-d", help="enables debug mode", action="store_true")
	args, unknown = argParseHandle.parse_known_args()
	if args.d:
		return True
	else:
		return False

class globalVars():
	_portNumber = 9000
	_debugMode = isDebugMode()
	_dbPath = "main.db"

	def __init__(self):
		pass


def getIpAddress():
	if globalVars._debugMode:
		print("DEBUG MODE ENABLED")
		return networkInfo.getIpSocket()
	else:
		return networkInfo.get_lan_ip()