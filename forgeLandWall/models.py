__author__ = 'Jesse'

from dbInterface import dbHelper
# from main import isDebugMode
import sqlite3


class messageModel(dbHelper):
	def __init__(self, index=None):
		dbHelper.__init__(self)

		if index is None:
			self.index = None
		else:
			self.index = index
			self.lookupRecord()
			print("Record Found")

	def lookupRecord(self):
		dbConn = sqlite3.connect(self.dbPath)
		dbcursor = dbConn.cursor()
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

	def saveRecord(self):
		if self.index is None:
			dbConn = sqlite3.connect(self.dbPath)
			dbcursor = dbConn.cursor()
			sqlStr = 'INSERT INTO messages ("message", "timestamp") VALUES' + \
			         '("' + self.message + '","' + str(dbHelper.getTimeStamp()) + '");'

			dbcursor.execute(sqlStr)
			dbConn.commit()
			dbConn.close()
		else:
			dbConn = sqlite3.connect(self.dbPath)
			dbcursor = dbConn.cursor()
			sqlStr = 'UPDATE messages SET message = "' + self.message + '", "timestamp" = "' + str(
				dbHelper.getTimeStamp()) + '"  WHERE "index" = "' + str(self.index) + '";'
			# TODO Add try and catch to SQL code
			dbcursor.execute(sqlStr)
			dbConn.commit()
			dbConn.close()

	def deleteRecord(self):
		dbConn = sqlite3.connect(self.dbPath)
		dbcursor = dbConn.cursor()
		sqlStr = 'DELETE FROM messages WHERE "index" = "' + str(self.index) + '";'
		dbcursor.execute(sqlStr)
		dbConn.commit()
		dbConn.close()