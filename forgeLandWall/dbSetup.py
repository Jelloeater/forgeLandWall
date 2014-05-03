import os
from settings import globalVars
from dbConnManage import dbConnManage as dbConnection

__author__ = 'Jesse'


def setupDB():
	"""	Initialize the database if it does not exist yet"""
	if not os.path.isfile(globalVars.dbPath):
		if globalVars.debugMode: print("Database Missing")
		dbConn, dbcursor = dbConnection.dbConnect()

		dbcursor.execute('CREATE TABLE "messages" (\
			"message"  ,\
			"timestamp"  ,\
			"index"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\
		);')

		dbConnection.dbClose(dbConn)
		if globalVars.debugMode: print ("Database generated")