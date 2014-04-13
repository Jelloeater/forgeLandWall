__author__ = 'Jesse'

import sqlite3


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

