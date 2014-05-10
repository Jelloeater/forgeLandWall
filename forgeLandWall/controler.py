import json
from forgeLandWall.models import messageModel

import logging
from settings import globalVars
logging.basicConfig(format=globalVars.logFormat, level=logging.DEBUG)
__author__ = 'Jesse'


class dbInterface(messageModel):
	@classmethod
	def searchForRecordsIndex(cls, messageIn):
		"""
		Returns list of message index's matching search string
		When left empty, returns all message indexes, can also be used to see if a message is present
		Used for updates and deletes. The user should be directly calling dbInterface.searchMessageFromDB
		"""
		dbConn, dbcursor = cls.dbConnect()
		sqlStr = 'SELECT "index" FROM messages WHERE "message" LIKE "%' + messageIn + '%";'
		indexList = None
		try:
			dbcursor.execute(sqlStr)
			indexList = dbcursor.fetchall()
			listOut = []
			for x in indexList:
				listOut.append(x[0])
			indexList = listOut
			# indexList = [x[0] for x in indexList] #  Same thing as above, list comprehension
			logging.info("Looked up record")
		except TypeError:
			logging.error("Record does not exist")
		dbConn.close()
		return indexList

	@classmethod
	def getBottomIndexes(cls, numberOfBottomIndexesToGet=1):
		"""Gets X number of index values from the bottom of the message table"""
		dbConn, dbcursor = cls.dbConnect()

		dbcursor.execute('SELECT "index"FROM messages ORDER BY "index" DESC LIMIT ' + str(numberOfBottomIndexesToGet))
		indexList = dbcursor.fetchall()
		dbConn.close()

		if indexList is None:  # If the column is empty
			return [0]
		else:
			return indexList

	@classmethod
	def getMessagesFromDB(cls, numberToGet=0):
		"""	Returns list of messages as instances of messageModel
		@param numberToGet Number of db records to return
		@return: msgList
		@rtype : list
		"""
		# TODO default search returns all
		msgList = []
		if numberToGet == 0:
			indexList = cls.searchForRecordsIndex("")
			for index in indexList:
				index = str(index)
				index = index.strip('(),')
				msg = messageModel(index)
				msgList.append(msg)
		else:
			indexList = cls.getBottomIndexes(numberToGet)
			indexList.reverse()
			for index in indexList:
				index = str(index)
				index = index.strip('(),')
				msg = messageModel(index)
				msgList.append(msg)

		return msgList

	@classmethod
	def getMessagesFromDBasJSONObjectArray(cls, numberToGet):
		"""	Returns a JSON string of the numberToGet bottom database entries
		:param numberToGet:
		"""
		msgList = cls.getMessagesFromDB(numberToGet)

		msgObjList = []

		for messageModelInstance in msgList:
			msgObj = empty()
			msgObj.message = messageModel.message(messageModelInstance)
			msgObj.timestamp = messageModel.getTimestamp(messageModelInstance)
			msgObjList.append(msgObj)

		return json.dumps(msgObjList, default=cls.getDict, sort_keys=True)

	@classmethod
	def getMessagesFromDBasJSONArray(cls, numberToGet):
		"""
		Returns 2D Array of messages & timestamps
		@param numberToGet:
		@return: JSON String
		"""
		msgList = cls.getMessagesFromDB(numberToGet)

		msgListArray = []
		timeListArray = []
		for messageModelInstance in msgList:
			msgStr = messageModel.message(messageModelInstance)
			timeStr = messageModel.getTimestamp(messageModelInstance)
			msgListArray.append(msgStr)
			timeListArray.append(timeStr)

		msgListBag = zip(msgListArray, timeListArray)

		retStr = json.dumps(msgListBag, sort_keys=True)

		return retStr

	@classmethod
	def searchMessagesFromDB(cls, messageIn=None):
		"""
		Searches the database and return a list of message pairs in list form
		This is a raw text search, it is NOT for altering anything, it's just so the user can get
		simple query results
		"""
		# TODO Maybe remove this or rewrite is when done with models.getMessagesFromDB
		if messageIn is not None:
			dbConn, dbcursor = cls.dbConnect()

			sqlStr = 'SELECT "message","timestamp" FROM messages WHERE "message" LIKE "%' + messageIn + '%";'
			dbcursor.execute(sqlStr)
			results = dbcursor.fetchall()

			cls.dbClose(dbConn)
			return results
		else:
			return ""

	@classmethod
	def _clearMessageTable(cls):
		dbConn, dbcursor = cls.dbConnect()
		sqlStr = 'DELETE FROM messages;'
		dbcursor.execute(sqlStr)
		cls.dbClose(dbConn)
	@classmethod
	def getDict(cls, obj):
		"""The default encoder to take the object instances	fields as JSON fields"""
		return obj.__dict__


class empty():

	"""Dummy class for JSON creation"""
	pass


class webControl(dbInterface):
	"""
	Provides methods to work with POST, JSON and CRUD db operations
	Works on the model INDIRECTLY
	"""

	@classmethod
	def getJSON(cls, numberToGet=1):
		return cls.getMessagesFromDBasJSONObjectArray(numberToGet)

	@classmethod
	def postControl(cls, requestBody):
		"""Splits POST request and sends to correct method"""
		# requestBody = POST Message
		logging.debug('postControl')
		# FIXME Create universal method for processing POST requests, a POST message splitter

		requestList = str.split(requestBody,'=')
		action = requestList[0]

		data = requestList[1]
		logging.debug('Action: ' + action + ' Data: ' + data)
		data = str.replace(data, '+', ' ')  # Adds proper space to message
		if not str.isspace(data) and data != "":
			if action == 'create':
				cls.createRecord(data)


	@classmethod
	def readPost(cls, postMessageIn):
		pass
		# TODO Should get all posts? Maybe create separate method for the main display

	@classmethod
	def createRecord(cls, messageIn=None):
		x = messageModel()
		x.message(message=messageIn)

	@classmethod
	def updateRecords(cls, messageIn=None):
		# TODO 1) Search for record index
		# TODO 2) update records (for loop)
		pass

	@classmethod
	def deleteRecords(cls, messageIn=None):
		# TODO 1) Search for record index
		# TODO 2) delete records (for loop)
		pass
