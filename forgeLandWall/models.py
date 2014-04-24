import datetime

__author__ = 'Jesse'

from dbInterface import dbHelper
# from main import isDebugMode
import sqlite3

# Yes, I know we're all adults here, but I don't like getting suggestions for methods I don't need


class messageModel(dbHelper):  # CREATE OR READ RECORD FROM DB
	# FIXME Add message search call (__lookupRecordFromMessage) via non default variable ex 'message = "barf"'
	def __init__(self, index=None):
		dbHelper.__init__(self)

		self.__messageTxt = None
		self.__timestamp = None

		if index is None:
			self.__index = None
		else:
			# Index should still be used for edits and delete though
			self.__index = index
			self.__lookupRecordFromIndex()
			print("Record Found")

	def message(self, message=None):  # Gets message from object, or writes message to DB
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
		print("Searching for: " + searchStr)
		dbConn, dbcursor = self.__dbConnect(self)
		# TODO Should __lookupRecordFromMessage for a SPECIFIC RECORD




		# Search for message text & index
		# Call lookup record with index

		# SELECT * FROM Customers WHERE City LIKE 's%';
		# % 	A substitute for zero or more characters

		# _ 	A substitute for a single character

		# [charlist] 	Sets and ranges of characters to match
		# SELECT * FROM Customers WHERE City LIKE '[a-c]%'

		# [^charlist]
		# or
		# [!charlist] 	Matches only a character NOT specified within the brackets



		sqlStr = ''
		dbcursor.execute(sqlStr)
		record = dbcursor.fetchone()
		self.__messageTxt = record[0]
		self.__timestamp = record[1]

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
			# FIXME Does not execute
			return record
		except TypeError:
			print("Record does not exist")

		dbConn.close()

	# TODO Move to dbInterface.dbHelper Class

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