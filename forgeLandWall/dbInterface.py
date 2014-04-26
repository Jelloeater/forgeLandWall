from forgeLandWall.settings import globalVars

__author__ = 'Jesse'

import dbConnection
import models
import json


def getBottomIndexes(numberOfBottomIndexesToGet=1):
	"""Gets X number of index values from the bottom of the message table"""
	dbConn, dbcursor = dbConnection.dbConnect()

	dbcursor.execute('SELECT "index"FROM messages ORDER BY "index" DESC LIMIT ' + str(numberOfBottomIndexesToGet))
	indexList = dbcursor.fetchall()
	dbConn.close()

	if indexList is None:  # If the column is empty
		return [1]
	else:
		return indexList


# TODO Use SQL select * to get everything, DON'T SPAM QUERYS! Let the program do the work!

def getMessagesFromDB(numberToGet):
	"""	Returns list of messages as instances of messageModel (Ex msgStr = models.messageModel.message(msgMdlInst)) """
	indexList = getBottomIndexes(numberToGet)
	indexList.reverse()
	msgList = []
	for index in indexList:
		index = str(index)
		index = index.strip('(),')
		msg = models.messageModel(index)
		msgList.append(msg)

		if globalVars._debugMode: print(msg.message() + msg.getTimestamp())

	return msgList


class msgObj(object):
	def __init__(self, msg, time):
		self.msg = msg
		self.time = time


def getDict(obj):
	return obj.__dict__


class empty():
	pass


def getMessageJSONObjects(numberToGet):
	msgList = getMessagesFromDB(numberToGet)

	msgObjList = []

	for messageModelInstance in msgList:
		msgStr = models.messageModel.message(messageModelInstance)
		timeStr = models.messageModel.getTimestamp(messageModelInstance)
		msgObjList.append(msgObj(msgStr, timeStr))

	return json.dumps(msgObjList, default=getDict, sort_keys=True)


def getMessagesFromDBasJSONArray(numberToGet):
	msgList = getMessagesFromDB(numberToGet)

	msgListArray = []
	timeListArray = []
	for messageModelInstance in msgList:
		msgStr = models.messageModel.message(messageModelInstance)
		timeStr = models.messageModel.getTimestamp(messageModelInstance)
		msgListArray.append(msgStr)
		timeListArray.append(timeStr)

	msgListBag = zip(msgListArray, timeListArray)

	retStr = json.dumps(msgListBag, sort_keys=True)

	return retStr


def searchMessagesFromDB():
	"""Searches the database and return a list of message objects"""
	# TODO Write search function that returns a ... just see the docstring -_-
	# Get last x index numbers
	# Pull X records
	# Throw records in a list
	# ?
	# Profit!!!
	pass
