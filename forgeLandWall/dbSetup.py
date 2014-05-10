import os
from forgeLandWall.dbConnManage import dbConnManage as dbConnection

__author__ = 'Jesse'
import logging
from settings import globalVars
logging.basicConfig(format=globalVars.logFormat, level=logging.DEBUG)

def setupDB():
	"""	Initialize the database if it does not exist yet"""
	if not os.path.isfile(globalVars.dbPath):
		logging.error("Database Missing")
		dbConn, dbcursor = dbConnection.dbConnect()

		dbcursor.execute('CREATE TABLE "messages" (\
			"message"  ,\
			"timestamp"  ,\
			"index"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\
		);')

		dbConnection.dbClose(dbConn)
		logging.info("Database generated")