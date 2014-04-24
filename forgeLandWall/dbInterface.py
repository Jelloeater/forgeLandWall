__author__ = 'Jesse'

import sqlite3
import os


class dbHelper():
	_dbPath = "main.db"
	# Please don't mess with this, unless we want to do multiple DB's? :)
	# TODO (Wish list) Implement multiple db?

	def __init__(self):
		pass

	@staticmethod
	def setupDB():
		if not os.path.isfile(dbHelper._dbPath):
			print("Database Missing")
			dbConnection = sqlite3.connect(dbHelper._dbPath)
			dbcursor = dbConnection.cursor()

			dbcursor.execute('CREATE TABLE "messages" (\
				"message"  ,\
				"timestamp"  ,\
				"index"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\
			);')

			dbConnection.commit()
			dbConnection.close()
			print ("Database generated")

	# TODO Write method to get X number of records from bottom?
	@staticmethod
	def getLastIndex():  # We will use this for getting an certain number of records
		dbConnection = sqlite3.connect(dbHelper._dbPath)
		dbcursor = dbConnection.cursor()
		dbcursor.execute('SELECT "index"FROM messages ORDER BY "index" DESC LIMIT 1')
		lastIndex = dbcursor.fetchone()
		dbConnection.close()
		if lastIndex is None:  # If the column is empty
			return 1
		else:
			return lastIndex[0]


# TODO Use SQL select * to get everything, DON'T SPAM QUERYS! Let the program do the work!
def getMessagesFromDB():
	pass
