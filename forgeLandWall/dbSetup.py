import os
from forgeLandWall.settings import globalVars
import forgeLandWall.dbConnManage as dbConnection


__author__ = 'Jesse'


def setupDB():
	"""Initialize the database if it does not exist yet"""
	if not os.path.isfile(globalVars._dbPath):
		if globalVars._debugMode: print("Database Missing")
		dbConn, dbcursor = dbConnection.dbConnect()

		dbcursor.execute('CREATE TABLE "messages" (\
			"message"  ,\
			"timestamp"  ,\
			"index"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\
		);')

		dbConnection.dbClose(dbConn)
		if globalVars._debugMode: print ("Database generated")