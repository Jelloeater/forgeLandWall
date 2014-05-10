import sqlite3

__author__ = 'Jesse Laptop'

import logging
from settings import globalVars
logging.basicConfig(format=globalVars.logFormat, level=logging.DEBUG)


class dbConnManage():
	@staticmethod
	def dbConnect():
		""" Connects to Database
		@return: dbConn, dbCur"""
		logging.info("Connection Opened")
		dbConn = sqlite3.connect(globalVars.dbPath)
		dbCur = dbConn.cursor()

		return dbConn, dbCur

	@staticmethod
	def dbClose(dbConn):
		"""	Closes the Database Connection
		@param dbConn: object
		"""
		dbConn.commit()
		dbConn.close()
		logging.info("Connection Closed")