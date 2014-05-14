import json
from models import messageModel

import logging

__author__ = 'Jesse'


class dbInterface(messageModel):
	@classmethod
	def searchRecords(cls, messageIn=""):
		"""
		Returns list of message index's matching search string
		When left empty, returns all message indexes, can also be used to see if a message is present
		Used for updates and deletes. The user should be directly calling dbInterface.searchMessageFromDB
		(why should they?)
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
			logging.debug("Looked up record")
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
		msgList = []
		if numberToGet == 0:
			indexList = cls.searchRecords("")
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
		msgList = cls.getMessagesFromDB(numberToGet)

		msgObjList = []

		for messageModelInstance in msgList:
			msgObj = empty()
			msgObj.message = messageModel.message(messageModelInstance)
			msgObj.timestamp = messageModel.getTimestamp(messageModelInstance)
			msgObj.index = messageModel.getIndex(messageModelInstance)
			msgObjList.append(msgObj)

		return json.dumps(msgObjList, default=cls.getDict, sort_keys=True)

	@classmethod
	def getMessageAsJSONObject(cls, index):

		msgObj = messageModel(index=index)  # Gets the message via index
		msgJSON = empty()
		msgJSON.message = msgObj.message()
		msgJSON.timestamp = msgObj.getTimestamp()
		msgJSON.index = msgObj.getIndex()

		return json.dumps(msgJSON, default=cls.getDict, sort_keys=True)

	@classmethod
	def searchMessagesFromDB(cls, messageIn=None):
		# TODO Remove this, it's sill and we have better code to do the same thing
		"""
		Searches the database and return a list of message pairs in list form
		This is a raw text search, it is NOT for altering anything, it's just so the user can get
		simple query results
		"""
		# TODO Maybe remove this or rewrite is when done with models.getMessagesFromDB (WAT?)
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
	def searchForMessagesJSON(cls, msgToSearchFor):
		""" Takes message string and returns JSON object"""
		# TODO Write unit tests to cover this
		logging.debug('Looking up: ' + msgToSearchFor)
		indexList = cls.searchRecords(msgToSearchFor)
		jsonString = []
		jsonString.append("[")
		for x in indexList:
			jsonString.append(cls.getMessageAsJSONObject(x))
			jsonString.append(",")

		jsonString.pop()  # Remove the extra comma introduced in the for loop
		logging.debug('Got message')
		jsonString.append(']')
		return ''.join(jsonString)

	@classmethod
	def postControl(cls, requestBody):
		# TODO Write unit tests to cover this
		"""Splits POST request and sends to correct method"""
		# requestBody = POST Message
		logging.debug('postControl')

		requestList = str.split(requestBody, '=')
		action = requestList[0]

		data = requestList[1]
		logging.debug('Action: ' + action + ' Data: ' + data)
		data = str.replace(data, '+', ' ')  # Adds proper space to message
		if not str.isspace(data) and data != "":
			if action == 'create':
				cls.createRecord(data)
			if action == 'delete':
				cls.deleteRecords(data)
			if action == 'edit':
				# TODO write better method for dealing with out of sequence POST messages
				# edit=someMessage&index=someNumber (normal)
				# index=someNumber&edit=someMessage (no control for this)
				indexIn = requestList[2]
				messageIn = requestList[1].split('&')
				cls.updateRecords(indexIn=indexIn, messageIn=messageIn[0].replace("+", " "))

	@classmethod
	def createRecord(cls, messageIn=None):
		x = messageModel()
		x.message(message=messageIn)

	@classmethod
	def updateRecords(cls, indexIn, messageIn=None):
		x = messageModel(index=indexIn)
		x.message(message=messageIn)
		pass

	@classmethod
	def deleteRecords(cls, index=None):
		x = messageModel(index=index)
		x.deleteRecord()
		pass
