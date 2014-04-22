__author__ = 'Jesse'

import sqlite3
import os


def setupDB():
	if not os.path.isfile(dbInterface.dbPath):
		print("Database Missing")
		dbConnection = sqlite3.connect(dbInterface.dbPath)
		dbcursor = dbConnection.cursor()

		dbcursor.execute('CREATE TABLE "messages" (\
			"message"  ,\
			"timestamp"  ,\
			"index"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\
		);')

		dbConnection.commit()
		dbConnection.close()
		print ("Database generated")


class dbInterface():
	def __init__(self):
		pass

	dbPath = "WallWebApp.db"
	# Should this be a module variable or a class variable?

	@staticmethod
	def getLastIndex():
		dbConnection = sqlite3.connect(dbInterface.dbPath)
		dbcursor = dbConnection.cursor()
		dbcursor.execute('SELECT "index"FROM messages ORDER BY "index" DESC LIMIT 1')
		lastIndex = dbcursor.fetchone()
		dbConnection.close()
		if lastIndex is None:  # If the column is empty
			return 1
		else:
			return lastIndex[0]