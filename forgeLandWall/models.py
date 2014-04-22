__author__ = 'Jesse'

from dbInterface import dbHelper
# from main import isDebugMode


class messageModel(dbHelper):
	def __init__(self, index=None):
		dbHelper.__init__(self)

		if index is None:
			# if isDebugMode(): print("Created new message object")
			self.index = None
			pass
		else:
			self.index = index  # Read index from database where index is index
			# SQL select * from messages where index = self.index, fill in info with index
			self.message = None  # Read message from database where index is index
			self.timestamp = None  # Read timestamp
		# if isDebugMode(): print("Loaded Object")

	def commit(self):
		import sqlite3

		if self.index is None:
			dbConn = sqlite3.connect(self.dbPath)
			dbcursor = dbConn.cursor()

			sqlStr = 'INSERT INTO messages ("message", "timestamp") VALUES ("' + self.message + '", "' + str(
				dbHelper.getTimeStamp()) + '");'
			dbcursor.execute(sqlStr)
			dbConn.commit()
			dbConn.close()
		else:
			dbConn = sqlite3.connect(self.dbPath)
			dbcursor = dbConn.cursor()
			sqlStr = 'UPDATE messages set message = self.message ' \
			         '"timestamp" = dbHelper.getTimeStamp() WHERE index = self.index;'
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