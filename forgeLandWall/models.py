import datetime

__author__ = 'Jesse'

from dbInterface import dbHelper
# from main import isDebugMode
import sqlite3

# Yes, I know we're all adults here, but I don't like getting suggestions for methods I don't need


class messageModel(dbHelper):  # CREATE
	def __init__(self, index=None):
		dbHelper.__init__(self)

		self.__messageTxt = None
		self.__timestamp = None

		if index is None:
			self.__index = None
		else:
			self.__index = index
			self.__lookupRecord()
			print("Record Found")

	def message(self, message=None):
		if message is None:
			return self.__messageTxt
		else:
			self.__messageTxt = message
			self.__saveRecord()

	def __dbConnect(self):
		print("Connection Opened")
		dbConn = sqlite3.connect(self._dbPath)
		dbcursor = dbConn.cursor()
		return dbConn, dbcursor

	@staticmethod
	def __dbClose(dbConn):
		print("Connection Closed")
		dbConn.commit()
		dbConn.close()

	def __lookupRecord(self):  # READ
		dbConn, dbcursor = self.__dbConnect()
		sqlStr = 'SELECT * FROM messages where "index" = "' + str(self.__index) + '"'

		try:
			dbcursor.execute(sqlStr)
			record = dbcursor.fetchone()
			self.__messageTxt = record[0]
			self.__timestamp = record[1]
			print("Looked up record")
			return record
		except TypeError:
			print("Record does not exist")

		dbConn.close()

	def __saveRecord(self):  # UPDATE
		if self.__index is None:
			dbConn, dbcursor = self.__dbConnect()
			sqlStr = 'INSERT INTO messages ("message", "timestamp") VALUES' + \
			         '("' + self.__messageTxt + '","' + str(self.__getTimeStamp()) + '");'

			dbcursor.execute(sqlStr)
			self.__dbClose(dbConn)
		else:
			dbConn, dbcursor = self.__dbConnect()
			sqlStr = 'UPDATE messages SET message = "' + self.__messageTxt + '", "timestamp" = "' + str(
				self.__getTimeStamp()) + '"  WHERE "index" = "' + str(self.__index) + '";'
			# TODO Add try and catch to SQL code
			dbcursor.execute(sqlStr)
			self.__dbClose(dbConn)

	def deleteRecord(self):  # DELETE
		dbConn, dbcursor = self.__dbConnect()
		sqlStr = 'DELETE FROM messages WHERE "index" = "' + str(self.__index) + '";'
		dbcursor.execute(sqlStr)
		self.__dbClose(dbConn)

	@staticmethod
	def __getTimeStamp():
		return datetime.datetime.now().replace(microsecond=0)