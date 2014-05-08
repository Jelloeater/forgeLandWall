__author__ = 'Jesse'
from unittest import TestCase
import forgeLandWall.models as models
import os
import constants


class TestMessageModel(TestCase):
	messageStr = constants.messageStr

	def setUp(self):
		"""Go-to project root so we can access the database"""
		os.chdir("..")
		os.chdir("forgeLandWall")
		import forgeLandWall.settings

		forgeLandWall.settings.globalVars.debugMode = True
		print("TEST SETUP")

	def tearDown(self):
		"""Delete test messages"""
		from forgeLandWall.dbConnManage import dbConnManage

		dbConn, dbcursor = dbConnManage.dbConnect()
		sqlStr = 'DELETE FROM messages WHERE "message" LIKE "%' + TestMessageModel.messageStr + '%";'
		dbcursor.execute(sqlStr)
		dbConnManage.dbClose(dbConn)
		print("TEST TEARDOWN")

	def test_message(self):
		# FIXME Broken due to bad lookup, FIX THE LOOKUP
		# Write

		dbObj = models.messageModel()
		dbObj.message(TestMessageModel.messageStr)

		# Search and read back
		dbObj2 = models.messageModel(message=TestMessageModel.messageStr)

		dbMessageStr = dbObj2.message()

		self.assertEquals(dbMessageStr, TestMessageModel.messageStr)

	def test_deleteRecord(self):
		# FIXME Broken due to bad lookup, FIX THE LOOKUP
		# Create message
		dbObj1 = models.messageModel()
		dbObj1.message(TestMessageModel.messageStr)

		# Delete message
		dbObj3 = models.messageModel(message=TestMessageModel.messageStr)
		dbObj3.deleteRecord()

		# Search for "missing" record
		dbObj = models.messageModel(message=TestMessageModel.messageStr)
		msgStr = dbObj.message()
		testStr = "CANNOT FIND MESSAGE: " + TestMessageModel.messageStr
		self.assertEquals(msgStr, testStr)


	def test_missingRecordMessage(self):
		# FIXME Broken due to bad lookup, FIX THE LOOKUP
		# Looks up message that shouldn't exist
		messageToTest = "someMissingMessage"
		dbOjb1 = models.messageModel(message=messageToTest)
		messageStr = dbOjb1.message()
		testStr = "CANNOT FIND MESSAGE: " + messageToTest

		self.assertEqual(messageStr, testStr)

	def test_missingRecordIndex(self):
		# Looks up message that should NEVER exist
		import random

		x = random.randint(1, 10)
		dbOjb1 = models.messageModel(x * -1)
		messageStr = dbOjb1.message()
		testStr = "CANNOT FIND MESSAGE @ INDEX" + str(x * -1)

		self.assertEqual(messageStr, testStr)


	def test_searchForRecords(self):
		# FIXME Broken due to bad lookup, FIX THE LOOKUP
		""""Search for many records containing string"""
		# Setup records
		testMsg1 = TestMessageModel.messageStr + "timmy1"
		testMsg2 = TestMessageModel.messageStr + "jimmy2"

		dbObj = models.messageModel()
		dbObj.message(testMsg1)
		dbObj3 = models.messageModel(message=testMsg1)  # tim
		msgOut1 = dbObj3.message()

		dbObj2 = models.messageModel()
		dbObj2.message(testMsg2)
		dbObj4 = models.messageModel(message=testMsg2)  # jim
		msgOut2 = dbObj4.message()

		self.assertEqual(testMsg1, msgOut1)
		self.assertEqual(testMsg2, msgOut2)


	def test_doesRecordExist(self):
		# FIXME Finish writing doesRecordExist test
		searchFlag = False
		# Create
		testMsg = TestMessageModel.messageStr + "exist"
		dbObj = models.messageModel()
		dbObj.message(testMsg)

		# Search

		# Compare
		self.assertTrue(searchFlag)