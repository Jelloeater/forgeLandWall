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

	def tearDown(self):
		"""Delete test message"""
		dbObj = models.messageModel(message=TestMessageModel.messageStr)
		dbObj.deleteRecord()

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
		dbObj3 = models.messageModel(message=TestMessageModel.messageStr)
		dbObj3.deleteRecord()

		dbObj = models.messageModel(message=TestMessageModel.messageStr)
		msgStr = dbObj.message()

		if msgStr != TestMessageModel.messageStr:
			pass
		else:
			self.fail()