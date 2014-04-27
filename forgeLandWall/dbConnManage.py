import sqlite3

from forgeLandWall.settings import globalVars


__author__ = 'Jesse Laptop'


def dbConnect():
	""" Connects to Database :rtype : dbConn, dbCur """
	if globalVars.debugMode: print("Connection Opened")
	dbConn = sqlite3.connect(globalVars.dbPath)
	dbCur = dbConn.cursor()

	return dbConn, dbCur

def dbClose(dbConn):
	"""	Closes the Database Connection """
	dbConn.commit()
	dbConn.close()
	if globalVars.debugMode: print("Connection Closed")