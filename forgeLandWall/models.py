import datetime
from forgeLandWall.dbConnManage import dbConnManage

from forgeLandWall.settings import globalVars


__author__ = 'Jesse'

# Yes, I know we're all adults here, but I don't like getting suggestions for methods I don't need


class messageModel(dbConnManage):
	# Creates record handle OR reads record from db
	"""Represents a SINGLE record from the table, we manipulate the objects, rather then SQL"""

	def __init__(self, index=None, message=None):


		if index is None and message is None:
			self.__index = None

		if message is not None and index is None:
			self.__lookupRecordFromMessage(message)
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

	def __lookupRecordFromMessage(self, searchStr):
		"""Looks up ONLY the FIRST record that matches the search"""

		dbConn, dbcursor = self.dbConnect()
		if globalVars.debugMode: print("Searching for: " + searchStr)
		try:
			sqlStr = 'SELECT * FROM messages WHERE message LIKE"%' + searchStr + '%"'
			dbcursor.execute(sqlStr)
			record = dbcursor.fetchone()
			self.__messageTxt = record[0]
			self.__timestamp = record[1]
			self.__index = record[2]
			if globalVars.debugMode: print("Record Found: " + searchStr)
		except TypeError:
			# FIXME Add better exception, no Pokemon exceptions!
			self.__messageTxt = "CANNOT FIND MESSAGE: " + searchStr
			self.__timestamp = ""
			self.__index = ""
			if globalVars.debugMode: print("Record Not Found")
		self.dbClose(dbConn)

	def __lookupRecordFromIndex(self):  # READ
		dbConn, dbcursor = self.dbConnect()
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
			dbConn, dbcursor = self.dbConnect()
			sqlStr = 'INSERT INTO messages ("message", "timestamp") VALUES' + \
			         '("' + self.__messageTxt + '","' + str(self.__getTimeStampFromSystem()) + '");'

			dbcursor.execute(sqlStr)
			self.dbClose(dbConn)
		else:
			dbConn, dbcursor = self.dbConnect()
			sqlStr = 'UPDATE messages SET message = "' + self.__messageTxt + '", "timestamp" = "' + \
					str(self.__getTimeStampFromSystem()) + '"  WHERE "index" = "' + str(self.__index) + '";'
			# TODO Add try and catch to SQL code
			dbcursor.execute(sqlStr)
			self.dbClose(dbConn)

	def deleteRecord(self):  # DELETE
		dbConn, dbcursor = self.dbConnect()
		sqlStr = 'DELETE FROM messages WHERE "index" = "' + str(self.__index) + '";'
		dbcursor.execute(sqlStr)
		if globalVars.debugMode: print("RECORD DELETED")
		self.dbClose(dbConn)

	def searchForRecords(self, messageIn=None):
		# FIXME Search for records with matching indexes
		# FIXME Return object array of matching records

		pass

	@staticmethod
	def __getTimeStampFromSystem():
		return datetime.datetime.now().replace(microsecond=0)