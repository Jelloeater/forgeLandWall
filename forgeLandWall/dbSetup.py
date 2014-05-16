import os
from dbConnManage import dbConnManage as dbConnection
import logging
from settings import globalVars

__author__ = 'Jesse'


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