import sqlite3
from forgeLandWall.settings import globalVars

__author__ = 'Jesse Laptop'


def dbConnect():
	print("Connection Opened")
	dbConn = sqlite3.connect(globalVars._dbPath)
	dbcursor = dbConn.cursor()
	return dbConn, dbcursor


def dbClose(dbConn):
	if globalVars._debugMode: print("Connection Closed")
	dbConn.commit()
	dbConn.close()