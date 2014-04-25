import os
import sqlite3

import main


__author__ = 'Jesse'


def setupDB():
	"""Initialize the database if it does not exist yet"""
	if not os.path.isfile(main.globalVars._dbPath):
		print("Database Missing")
		dbConnection = sqlite3.connect(main.globalVars._dbPath)
		dbcursor = dbConnection.cursor()

		dbcursor.execute('CREATE TABLE "messages" (\
			"message"  ,\
			"timestamp"  ,\
			"index"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\
		);')

		dbConnection.commit()
		dbConnection.close()
		print ("Database generated")