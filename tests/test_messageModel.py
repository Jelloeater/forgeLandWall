__author__ = 'Jesse'
from unittest import TestCase
import forgeLandWall.models as models
import os


class TestMessageModel(TestCase):
	messageStr = "testMessagePleaseIgnore"

	def setUp(self):
		"""Go-to project root so we can access the database"""
		os.chdir("..")
		os.chdir("forgeLandWall")
		import forgeLandWall.settings
		forgeLandWall.settings.globalVars.debugMode = True
		print("TEST SETUP")

	def tearDown(self):
		"""Delete test messages"""
		import forgeLandWall.dbConnManage as dbConnManage
		dbConn, dbcursor = dbConnManage.dbConnect()
		sqlStr = 'DELETE FROM messages WHERE "message" LIKE "' + TestMessageModel.messageStr + '";'
		dbcursor.execute(sqlStr)
		dbConnManage.dbClose(dbConn)
		print("TEST TEARDOWN")

	def test_message(self):
		# Write

		dbObj = models.messageModel()
		dbObj.message(TestMessageModel.messageStr)

		# Search and read back
		dbObj2 = models.messageModel(message=TestMessageModel.messageStr)
		dbMessageStr = dbObj2.message()

		if dbMessageStr == TestMessageModel.messageStr:
			pass
		else:
			self.fail()

	def test_deleteRecord(self):
		# Create message
		dbObj1 = models.messageModel()
		dbObj1.message(TestMessageModel.messageStr)

		# Delete message
		dbObj3 = models.messageModel(message=TestMessageModel.messageStr)
		dbObj3.deleteRecord()

		# Search for "missing" record
		dbObj = models.messageModel(message=TestMessageModel.messageStr)
		msgStr = dbObj.message()

		if msgStr != TestMessageModel.messageStr:
			pass
		else:
			self.fail()