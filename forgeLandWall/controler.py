from forgeLandWall.dbInterface import dbInterface
from forgeLandWall.models import messageModel

__author__ = 'Jesse'


class webControl(messageModel):
	@staticmethod
	def readPost(postMessageIn):
		pass
	# FIXME Write filter method
	# TODO Should get all posts, this will be the main display
	# TODO This might be in the wrong place?

	@staticmethod
	def createRecord(messageIn=None):
		x = messageModel()
		x.message(message=messageIn)

	@staticmethod
	def updateRecords(messageIn=None):
		pass
	# TODO write update call
	# TODO 1) Search for record index 2) update records (for loop)

	@staticmethod
	def deleteRecords(messageIn=None):
		pass
		# TODO 1) Seach for record index 2) update records (for loop)
		# TODO write delete call

	@staticmethod
	def getJSON(numberToGet=1):
		return dbInterface.getMessagesFromDBasJSONObjectArray(numberToGet)


	@classmethod
	def postSplitter(cls, requestBody):
		"""Splits POST request and sends to correct method"""
		# requestBody = POST Message
		# TODO Create universal method for processing POST requests, a POST message splitter
		print('postSplitter')
		print(locals())