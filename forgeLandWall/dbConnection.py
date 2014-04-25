import sqlite3

from forgeLandWall.settings import globalVars


__author__ = 'Jesse Laptop'


def dbConnect():
	""" Connects to Database :rtype : dbConn, dbcursor """
	if globalVars._debugMode: print("Connection Opened")
	dbConn = sqlite3.connect(globalVars._dbPath)
	dbcursor = dbConn.cursor()

	return dbConn, dbcursor


def dbClose(dbConn):
	"""	Closes the Database Connection """
	if globalVars._debugMode: print("Connection Closed")
	dbConn.commit()
	dbConn.close()