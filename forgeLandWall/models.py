__author__ = 'Jesse'

from dbInterface import dbHelper
from main import isDebugMode


class messageModel(dbHelper):
	def __init__(self, index=None, message=None):
		dbHelper.__init__(self)

		if index is None:
			self.index = self.getLastIndex()
			# We don't actually change the index, we just get it, I might be wrong
			self.message = message
			self.timestamp = self.getTimeStamp()
			print (isDebugMode())
			if isDebugMode(): print("Created new message object")
		else:
			self.index = index
			self.message = None  # Read message
			self.timestamp = None  # Read timestamp
			if isDebugMode(): print("Loaded Object")

	def commit(self):
		import sqlite3

		dbConn = sqlite3.connect(self.dbPath)
		dbcursor = dbConn.cursor()
		sqlStr = 'INSERT INTO messages (message, "timestamp", index) VALUES self.message, self.timestamp self.index'
		dbcursor.execute(sqlStr)
		dbConn.commit()
		dbConn.close()

	# TODO Write lookup method, we don't need edit, we should be able to edit the object

	@staticmethod
	def insertName():
		print("Name to add: ")
		nameIn = input()
		retString = 'insert into testtable values ("' + nameIn + '")'
		return retString
		dbcursor.execute(dbHelper.printList())
		fetchData = dbcursor.fetchall()
		print(fetchData)