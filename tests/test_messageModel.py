__author__ = 'Jesse'
from unittest import TestCase
import models as models
from controler import webControl
from dbConnManage import dbConnManage
import os
import constants


class TestMessageModel(TestCase):
	messageStr = constants.messageStr

	def setUp(self):
		"""Go-to project root so we can access the database"""
		os.chdir("..")
		os.chdir("forgeLandWall")
		print("TEST SETUP")

	def tearDown(self):
		"""Delete test messages"""
		dbConn, dbcursor = dbConnManage.dbConnect()
		sqlStr = 'DELETE FROM messages WHERE "message" LIKE "%' + TestMessageModel.messageStr + '%";'
		dbcursor.execute(sqlStr)
		dbConnManage.dbClose(dbConn)
		print("TEST TEARDOWN")

	def test_message(self):
		# Write
		dbObj = models.messageModel()
		dbObj.message(TestMessageModel.messageStr)

		# Search and read back
		indexList = webControl.searchForRecordsIndex(TestMessageModel.messageStr)
		dbObj2 = models.messageModel(index=indexList[0])

		dbMessageStr = dbObj2.message()

		self.assertEquals(dbMessageStr, TestMessageModel.messageStr)

	def test_deleteRecord(self):
		# Create message
		dbObj1 = models.messageModel()
		dbObj1.message(TestMessageModel.messageStr)

		# Delete message
		indexList = webControl.searchForRecordsIndex(TestMessageModel.messageStr)
		dbObj3 = models.messageModel(index=indexList[0])
		dbObj3.deleteRecord()

		# Search for "missing" record
		dbObj = models.messageModel(index=indexList[0])
		msgStr = dbObj.message()
		testStr = "CANNOT FIND MESSAGE @ INDEX" + str(indexList[0])
		self.assertEquals(msgStr, testStr)

	def test_missingRecordIndex(self):
		# Looks up message that should NEVER exist
		import random
		x = random.randint(1, 10)
		dbOjb1 = models.messageModel(x * -1)
		messageStr = dbOjb1.message()
		testStr = "CANNOT FIND MESSAGE @ INDEX" + str(x * -1)
		self.assertEqual(messageStr, testStr)

	def test_doesRecordExist(self):
		searchFlag = False
		# Create
		testMsg = TestMessageModel.messageStr + "exist"
		dbObj = models.messageModel()
		dbObj.message(testMsg)

		# Search
		indexList = webControl.searchForRecordsIndex(testMsg)
		# Compare
		self.assertTrue(models.messageModel.doesRecordExist(indexList[0]))