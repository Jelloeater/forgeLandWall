from forgeLandWall.settings import globalVars

__author__ = 'Jesse'

import forgeLandWall.dbConnManage as dbConnection
import forgeLandWall.models as models
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


def getMessagesFromDB(numberToGet):
	"""	Returns list of messages as instances of messageModel
	@param numberToGet Number of db records to return
	@return: msgList
	@rtype : list
	"""
	indexList = getBottomIndexes(numberToGet)
	indexList.reverse()
	msgList = []
	for index in indexList:
		index = str(index)
		index = index.strip('(),')
		msg = models.messageModel(index)
		msgList.append(msg)

		if globalVars.debugMode: print(msg.message() + msg.getTimestamp())

	return msgList


def getDict(obj):
	"""The default encoder to take the object instances	fields as JSON fields"""
	return obj.__dict__


class empty():
	"""Dummy class for JSON creation"""
	pass


def getMessagesFromDBasJSONObjectArray(numberToGet):
	"""	Returns a JSON string of the numberToGet bottom database entries
	:param numberToGet:
	"""
	msgList = getMessagesFromDB(numberToGet)

	msgObjList = []

	for messageModelInstance in msgList:
		msgObj = empty()
		msgObj.message = models.messageModel.message(messageModelInstance)
		msgObj.timestamp = models.messageModel.getTimestamp(messageModelInstance)
		msgObjList.append(msgObj)

	return json.dumps(msgObjList, default=getDict, sort_keys=True)


def getMessagesFromDBasJSONArray(numberToGet):
	"""
	Returns 2D Array of messages & timestamps
	@param numberToGet:
	@return: JSON String
	"""
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


def searchMessagesFromDB(messageIn = None):
	"""Searches the database and return a list of message pairs in list form"""
	# TODO Maybe remove this or rewrite is when done with models.getMessagesFromDB
	if messageIn is not None:
		import dbConnManage
		dbConn, dbcursor = dbConnManage.dbConnect()

		sqlStr = 'SELECT "message","timestamp" FROM messages ' \
		         'WHERE "message" LIKE "%' + messageIn + '%";'
		dbcursor.execute(sqlStr)
		results = dbcursor.fetchall()

		dbConnManage.dbClose(dbConn)
		return results
	else:
		return ""


def _clearMessageTable():
	dbConn, dbcursor = dbConnection.dbConnect()
	sqlStr = 'DELETE FROM messages;'
	dbcursor.execute(sqlStr)
	dbConnection.dbClose(dbConn)
