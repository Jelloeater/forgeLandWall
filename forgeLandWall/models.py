import datetime

__author__ = 'Jesse'

from dbInterface import dbHelper
# from main import isDebugMode
import sqlite3

# Yes, I know we're all adults here, but I don't like getting suggestions for methods I don't need


class messageModel(dbHelper):  # CREATE OR READ RECORD FROM DB
	"""Represents a SINGLE record from the table, we manipulate the objects, rather then SQL"""

	def __init__(self, index=None, message=None):
		dbHelper.__init__(self)

		self.__messageTxt = None
		self.__timestamp = None

		if index is None and message is None:
			self.__index = None

		if message is not None and index is None:
			self.__lookupRecordFromMessage(message)
		if index is not None and message is None:
			# Index should still be used for edits and delete though
			self.__index = index
			self.__lookupRecordFromIndex()
			print("Record Found")
		# TODO Add check for record not found

	def message(self, message=None):
		"""Gets message from object, or writes message to DB"""
		if message is None:
			return self.__messageTxt
		else:
			self.__messageTxt = message
			self.__saveRecord()

	def getTimestamp(self):
		return self.__timestamp


	@staticmethod
	def __dbConnect(self):
		print("Connection Opened")
		dbConn = sqlite3.connect(self._dbPath)
		dbcursor = dbConn.cursor()
		return dbConn, dbcursor

	# TODO Move to dbInterface.dbHelper Class?
	@staticmethod
	def __dbClose(dbConn):
		print("Connection Closed")
		dbConn.commit()
		dbConn.close()

	def __lookupRecordFromMessage(self, searchStr):
		"""Looks up ONLY the FIRST record that matches the search"""
		print("Searching for: " + searchStr)
		dbConn, dbcursor = self.__dbConnect(self)

		try:
			sqlStr = 'SELECT * FROM messages WHERE message LIKE"%' + searchStr + '%"'
			dbcursor.execute(sqlStr)
			record = dbcursor.fetchone()
			self.__messageTxt = record[0]
			self.__timestamp = record[1]
			self.__index = record[2]
		except TypeError:  # FIXME Add better exception, no Pokemon exceptions!
			self.__messageTxt = "CANNOT FIND MESSAGE: " + searchStr
			self.__timestamp = ""
			self.__index = ""
			print("Record Not Found")
		self.__dbClose(dbConn)


	def __lookupRecordFromIndex(self):  # READ
		dbConn, dbcursor = self.__dbConnect(self)
		sqlStr = 'SELECT * FROM messages where "index" = "' + str(self.__index) + '"'

		try:
			dbcursor.execute(sqlStr)
			record = dbcursor.fetchone()
			self.__messageTxt = record[0]
			self.__timestamp = record[1]
			self.__index = record[2]
			print("Looked up record")
		except TypeError:
			print("Record does not exist")

		dbConn.close()

	def __saveRecord(self):  # UPDATE
		if self.__index is None:
			dbConn, dbcursor = self.__dbConnect(self)
			sqlStr = 'INSERT INTO messages ("message", "timestamp") VALUES' + \
			         '("' + self.__messageTxt + '","' + str(self.__getTimeStampFromSystem()) + '");'

			dbcursor.execute(sqlStr)
			self.__dbClose(dbConn)
		else:
			dbConn, dbcursor = self.__dbConnect(self)
			sqlStr = 'UPDATE messages SET message = "' + self.__messageTxt + '", "timestamp" = "' + str(
				self.__getTimeStampFromSystem()) + '"  WHERE "index" = "' + str(self.__index) + '";'
			# TODO Add try and catch to SQL code
			dbcursor.execute(sqlStr)
			self.__dbClose(dbConn)

	def deleteRecord(self):  # DELETE
		dbConn, dbcursor = self.__dbConnect(self)
		sqlStr = 'DELETE FROM messages WHERE "index" = "' + str(self.__index) + '";'
		dbcursor.execute(sqlStr)
		self.__dbClose(dbConn)

	@staticmethod
	def __getTimeStampFromSystem():
		return datetime.datetime.now().replace(microsecond=0)