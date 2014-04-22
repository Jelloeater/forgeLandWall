__author__ = 'Jesse'

from dbInterface import dbHelper
# from main import isDebugMode
import sqlite3


class messageModel(dbHelper):  # CREATE
	def __init__(self, index=None):
		dbHelper.__init__(self)

		self.message = None
		self.timestamp = None

		if index is None:
			self.index = None
		else:
			self.index = index
			self.lookupRecord()
			print("Record Found")

	def dbConnect(self):
		print("Connection Opened")
		dbConn = sqlite3.connect(self.dbPath)
		dbcursor = dbConn.cursor()
		return dbConn, dbcursor

	@staticmethod
	def dbClose(dbConn):
		print("Connection Closed")
		dbConn.commit()
		dbConn.close()

	def lookupRecord(self):  # READ
		dbConn, dbcursor = self.dbConnect()
		sqlStr = 'SELECT * FROM messages where "index" = "' + str(self.index) + '"'

		try:
			dbcursor.execute(sqlStr)
			record = dbcursor.fetchone()
			self.message = record[0]
			self.timestamp = record[1]
			print("Looked up record")
			return record
		except TypeError:
			print("Record does not exist")

		dbConn.close()

	def saveRecord(self):  # UPDATE
		if self.index is None:
			dbConn, dbcursor = self.dbConnect()
			sqlStr = 'INSERT INTO messages ("message", "timestamp") VALUES' + \
			         '("' + self.message + '","' + str(dbHelper.getTimeStamp()) + '");'

			dbcursor.execute(sqlStr)
			self.dbClose(dbConn)
		else:
			dbConn, dbcursor = self.dbConnect()
			sqlStr = 'UPDATE messages SET message = "' + self.message + '", "timestamp" = "' + str(
				dbHelper.getTimeStamp()) + '"  WHERE "index" = "' + str(self.index) + '";'
			# TODO Add try and catch to SQL code
			dbcursor.execute(sqlStr)
			self.dbClose(dbConn)

	def deleteRecord(self):  # DELETE
		dbConn, dbcursor = self.dbConnect()
		sqlStr = 'DELETE FROM messages WHERE "index" = "' + str(self.index) + '";'
		dbcursor.execute(sqlStr)
		self.dbClose(dbConn)