import argparse

__author__ = 'Jesse Laptop'


def isDebugMode():
	argParseHandle = argparse.ArgumentParser()
	argParseHandle.add_argument("-d", help="enables debug mode", action="store_true")
	args = argParseHandle.parse_args()
	if args.d:
		return True
	else:
		return False

class globalVars():
	def __init__(self):
		pass
	_debugMode = isDebugMode()
	_dbPath = "main.db"