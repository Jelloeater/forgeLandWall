import os
import sqlite3

__author__ = 'Jesse'


def setupDB(dbPath):
	"""Initialize the database if it does not exist yet"""
	if not os.path.isfile(dbPath):
		print("Database Missing")
		dbConnection = sqlite3.connect(dbPath)
		dbcursor = dbConnection.cursor()

		dbcursor.execute('CREATE TABLE "messages" (\
			"message"  ,\
			"timestamp"  ,\
			"index"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\
		);')

		dbConnection.commit()
		dbConnection.close()
		print ("Database generated")