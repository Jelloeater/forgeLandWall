__author__ = 'Jesse'

import datetime

from dbInterface import dbInterface


class messageModel(dbInterface):
	def __init__(self, index=None, message=None):
		dbInterface.__init__(self)

		if index is None:
			self.index = self.getLastIndex()
			# We don't actually change the index, we just get it, I might be wrong
			self.message = message
			self.timestamp = datetime.datetime.now().replace(microsecond=0)

	def commit(self):
		import sqlite3

		dbConn = sqlite3.connect(self.dbPath)
		dbcursor = dbConn.cursor()
		sqlStr = 'INSERT INTO messages (message, timestamp, "index") VALUES self.message, self.timestamp'
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
		dbcursor.execute(dbInterface.printList())
		fetchData = dbcursor.fetchall()
		print(fetchData)