__author__ = 'Jesse'

import sqlite3

import main
import models


def getBottomIndexes(numberOfBottomIndexesToGet=1):
	"""Gets X number of index values from the bottom of the message table"""
	dbConnection = sqlite3.connect(main.globalVars._dbPath)
	dbcursor = dbConnection.cursor()

	dbcursor.execute('SELECT "index"FROM messages ORDER BY "index" DESC LIMIT ' + str(numberOfBottomIndexesToGet))
	indexList = dbcursor.fetchall()
	dbConnection.close()

	if indexList is None:  # If the column is empty
		return [1]
	else:
		return indexList


# TODO Use SQL select * to get everything, DON'T SPAM QUERYS! Let the program do the work!

def getMessagesFromDB():
	indexList = getBottomIndexes(10)
	indexList.reverse()
	for index in indexList:
		index = str(index)
		index = index.strip('(),')
		msg = models.messageModel(index)
		print(msg.message() + msg.getTimestamp())


def searchMessagesFromDB():
	"""Searches the database and return a list of message objects"""
	# TODO Write search function that returns a ... just see the docstring -_-
	# Get last x index numbers
	# Pull X records
	# Throw records in a list
	# ?
	# Profit!!!
	pass
