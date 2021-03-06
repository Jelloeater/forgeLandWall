import argparse

import networkInfo


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
	portNumber = 9000
	debugMode = isDebugMode()
	dbPath = "main.db"
	# TODO Maybe work out any absolute path in case we get multiple folders

	def __init__(self):
		pass


def getIpAddress():
	if globalVars.debugMode:
		print("DEBUG MODE ENABLED")
		return networkInfo.getIpSocket()
	else:
		return networkInfo.get_lan_ip()