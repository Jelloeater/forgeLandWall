from unittest import TestCase
from forgeLandWall import models
from forgeLandWall.views import HTMLHelper
import constants
import os
from forgeLandWall.dbConnManage import dbConnManage
__author__ = 'Jesse'


class TestHTMLHelper(TestCase):
	def setUp(self):
		"""Go-to project root so we can access the database"""
	os.chdir("..")
	os.chdir("forgeLandWall")

	x = models.messageModel()
	x.message(constants.messageStr + 'meow')
	x = models.messageModel()
	x.message(constants.messageStr + 'cats')
	print("TEST SETUP")

	def tearDown(self):
		"""Delete test messages"""
		dbConn, dbcursor = dbConnManage.dbConnect()
		sqlStr = 'DELETE FROM messages WHERE "message" LIKE "%' + constants.messageStr + '%";'
		dbcursor.execute(sqlStr)
		dbConnManage.dbClose(dbConn)
		print("TEST TEARDOWN")

	def test_getMessages(self):
		output = []
		output = HTMLHelper.getMessages(output)
		print(output)
		self.assertEqual(output[0],"<br>")
		self.assertEqual(output[1], constants.messageStr + 'meow')