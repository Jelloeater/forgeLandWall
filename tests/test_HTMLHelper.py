from unittest import TestCase
import models
from views import HTMLHelper
import constants
import os
from dbConnManage import dbConnManage
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
		output = HTMLHelper.getMessagesTable(output)
		print(output)
		self.assertEqual("<table><tr><th>Message</th><th>Timestamp</th></tr>", output[0])
		# self.assertEqual(constants.messageStr + 'meow', output[1],)
		# TODO Maybe search for specific record? (We already test for this though -_-)