import sqlite3

from forgeLandWall.settings import globalVars


__author__ = 'Jesse Laptop'


def dbConnect():
	""" Connects to Database :rtype : dbConn, dbCur """
	if globalVars._debugMode: print("Connection Opened")
	dbConn = sqlite3.connect(globalVars._dbPath)
	dbCur = dbConn.cursor()

	return dbConn, dbCur

def dbClose(dbConn):
	"""	Closes the Database Connection """
	dbConn.commit()
	dbConn.close()
	if globalVars._debugMode: print("Connection Closed")