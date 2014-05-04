import json
from models import messageModel
from settings import globalVars

__author__ = 'Jesse'


class dbInterface(messageModel):
	@classmethod
	def getBottomIndexes(cls, numberOfBottomIndexesToGet=1):
		"""Gets X number of index values from the bottom of the message table"""
		dbConn, dbcursor = cls.dbConnect()

		dbcursor.execute('SELECT "index"FROM messages ORDER BY "index" DESC LIMIT ' + str(numberOfBottomIndexesToGet))
		indexList = dbcursor.fetchall()
		dbConn.close()

		if indexList is None:  # If the column is empty
			return [1]
		else:
			return indexList

	@classmethod
	def getMessagesFromDB(cls, numberToGet):
		"""	Returns list of messages as instances of messageModel
		@param numberToGet Number of db records to return
		@return: msgList
		@rtype : list
		"""
		indexList = cls.getBottomIndexes(numberToGet)
		indexList.reverse()
		msgList = []
		for index in indexList:
			index = str(index)
			index = index.strip('(),')
			msg = messageModel(index)
			msgList.append(msg)

			if globalVars.debugMode: print(msg.message() + msg.getTimestamp())

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
		"""Searches the database and return a list of message pairs in list form"""
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
	@classmethod
	def getJSON(cls, numberToGet=1):
		return cls.getMessagesFromDBasJSONObjectArray(numberToGet)

	@classmethod
	def postSplitter(cls, requestBody):
		"""Splits POST request and sends to correct method"""
		# requestBody = POST Message
		# FIXME Create universal method for processing POST requests, a POST message splitter
		print('postSplitter')
		print(locals())

	@classmethod
	def readPost(cls, postMessageIn):
		pass
	# TODO Should get all posts? Maybe create separate method for the main display
	# TODO write update call
	# TODO 1) Search for record index 2) update records (for loop)

	@classmethod
	def createRecord(cls, messageIn=None):
		x = messageModel()
		x.message(message=messageIn)
	# TODO 1) Search for record index 2) update records (for loop)
	# TODO write delete call

	@classmethod
	def updateRecords(cls, messageIn=None):
		pass


	@classmethod
	def deleteRecords(cls, messageIn=None):
		pass
