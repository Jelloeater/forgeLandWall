import os
import sqlite3
from forgeLandWall.settings import globalVars

import main


__author__ = 'Jesse'


def setupDB():
	"""Initialize the database if it does not exist yet"""
	if not os.path.isfile(globalVars._dbPath):
		print("Database Missing")
		dbConnection = sqlite3.connect(globalVars._dbPath)
		dbcursor = dbConnection.cursor()

		dbcursor.execute('CREATE TABLE "messages" (\
			"message"  ,\
			"timestamp"  ,\
			"index"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL\
		);')

		dbConnection.commit()
		dbConnection.close()
		print ("Database generated")