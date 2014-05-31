import sqlite3
import logging
from settings import globalVars

__author__ = 'Jesse Laptop'


class dbConnManage():
	logging.basicConfig(format="[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(lineno)s)", level=logging.DEBUG)
	@staticmethod
	def dbConnect():
		""" Connects to Database
		@return: dbConn, dbCur"""
		logging.debug("Connection Opened")
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
		logging.debug("Connection Closed")