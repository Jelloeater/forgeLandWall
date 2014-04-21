__author__ = 'Jesse'

import sqlite3
import os

dbPath = "WallWebApp.db"


def setupDB():
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


def run():

	dbconnection = sqlite3.connect("todoList.db")
	dbcursor = dbconnection.cursor()

	dbcursor.execute(insertName())

	dbcursor.execute(printList())
	fetchData=dbcursor.fetchall()
	print(fetchData)

	dbconnection.commit()
	dbconnection.close()


def insertName():
	print("Name to add: ")
	nameIn = input()
	retString = 'insert into testtable values ("' + nameIn + '")'
	return retString


def printList():
	retString = 'select * from testtable where name="Jesse"'
	return retString
