from unittest import TestCase
from forgeLandWall import models
from tests.test_messageModel import TestMessageModel

__author__ = 'Jesse Laptop'


class TestWebControl(TestCase):
	messageStr = "testMessagePleaseIgnore"
	def setUp(self):
		"""Go-to project root so we can access the database"""

		print("TEST SETUP")

	def tearDown(self):
		"""Delete test messages"""
		from forgeLandWall.dbConnManage import dbConnManage

		dbConn, dbcursor = dbConnManage.dbConnect()
		sqlStr = 'DELETE FROM messages WHERE "message" LIKE "%' + TestMessageModel.messageStr + '%";'
		dbcursor.execute(sqlStr)
		dbConnManage.dbClose(dbConn)
		print("TEST TEARDOWN")

	def test_searchForRecordsIndex(self):
		# FIXME Write test for this method! *** WORK ON THIS NEXT!***
		dbObj = models.messageModel()
		dbObj.message(TestWebControl.messageStr)

		self.fail()