import sqlite3

from forgeLandWall.settings import globalVars

__author__ = 'Jesse Laptop'


class dbConnManage:
	@staticmethod
	def dbConnect():
		""" Connects to Database
		@return: dbConn, dbCur"""
		if globalVars.debugMode: print("Connection Opened")
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
		if globalVars.debugMode: print("Connection Closed")