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