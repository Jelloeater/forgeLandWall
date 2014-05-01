import datetime

import forgeLandWall.dbConnManage as dbConnection
from forgeLandWall.settings import globalVars


__author__ = 'Jesse'

# Yes, I know we're all adults here, but I don't like getting suggestions for methods I don't need


class messageModel(globalVars):
	# Creates record handle OR reads record from db, we shouldn't work with more then one record
	"""Represents a SINGLE record from the table, we manipulate the objects, rather then SQL"""

	def __init__(self, index=None, message=None):
		globalVars.__init__(self)

		self.__messageTxt = None
		self.__timestamp = None

		if index is None and message is None:
			self.__index = None

		if index is not None and message is None:
			# Index should still be used for edits and delete though
			self.__index = index
			self.__lookupRecordFromIndex()
			if globalVars.debugMode: print("Record Found")

	def message(self, message=None):
		"""Gets message from object, or writes message to DB"""
		if message is None:
			return self.__messageTxt
		else:
			self.__messageTxt = message
			self.__saveRecord()

	def getTimestamp(self):
		return self.__timestamp


	def __lookupRecordFromIndex(self):  # READ
		dbConn, dbcursor = dbConnection.dbConnect()
		sqlStr = 'SELECT * FROM messages where "index" = "' + str(self.__index) + '"'

		try:
			dbcursor.execute(sqlStr)
			record = dbcursor.fetchone()
			self.__messageTxt = record[0]
			self.__timestamp = record[1]
			self.__index = record[2]
			if globalVars.debugMode: print("Looked up record")
		except TypeError:
			self.__messageTxt = "CANNOT FIND MESSAGE @ INDEX" + str(self.__index)
			self.__timestamp = ""
			self.__index = ""
			if globalVars.debugMode: print("Record does not exist")

		dbConn.close()

	def __saveRecord(self):  # UPDATE
		if self.__index is None:
			dbConn, dbcursor = dbConnection.dbConnect()
			sqlStr = 'INSERT INTO messages ("message", "timestamp") VALUES' + \
			         '("' + self.__messageTxt + '","' + str(self.__getTimeStampFromSystem()) + '");'

			dbcursor.execute(sqlStr)
			dbConnection.dbClose(dbConn)
		else:
			dbConn, dbcursor = dbConnection.dbConnect()
			sqlStr = 'UPDATE messages SET message = "' + self.__messageTxt + '", "timestamp" = "' + str(
				self.__getTimeStampFromSystem()) + '"  WHERE "index" = "' + str(self.__index) + '";'
			# TODO Add try and catch to SQL code
			dbcursor.execute(sqlStr)
			dbConnection.dbClose(dbConn)

	def deleteRecord(self):  # DELETE
		dbConn, dbcursor = dbConnection.dbConnect()
		sqlStr = 'DELETE FROM messages WHERE "index" = "' + str(self.__index) + '";'
		dbcursor.execute(sqlStr)
		if globalVars.debugMode: print("RECORD DELETED")
		dbConnection.dbClose(dbConn)

	def searchForRecords(self,messageIn = None):
		# FIXME Search for records with matching indexes
		# FIXME Return object array of matching records

		pass

	@staticmethod
	def __getTimeStampFromSystem():
		return datetime.datetime.now().replace(microsecond=0)