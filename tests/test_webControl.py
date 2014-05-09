from re import L
from unittest import TestCase
from forgeLandWall import models
from forgeLandWall.controler import webControl
import constants
import os

__author__ = 'Jesse Laptop'


class TestWebControl(TestCase):
	def setUp(self):
		"""Go-to project root so we can access the database"""
		os.chdir("..")
		os.chdir("forgeLandWall")
		print("TEST SETUP")

	def tearDown(self):
		"""Delete test messages"""
		from forgeLandWall.dbConnManage import dbConnManage

		dbConn, dbcursor = dbConnManage.dbConnect()
		sqlStr = 'DELETE FROM messages WHERE "message" LIKE "%' + constants.messageStr + '%";'
		dbcursor.execute(sqlStr)
		dbConnManage.dbClose(dbConn)
		print("TEST TEARDOWN")

	def test_searchForRecordsIndex(self):
		# Create message
		dbObj = models.messageModel()
		dbObj.message(constants.messageStr)

		# Search for index
		indexList = webControl.searchForRecordsIndex(constants.messageStr)
		dbObj2 = models.messageModel(index=indexList[0])
		testStr = dbObj2.message()

		self.assertEqual(constants.messageStr,testStr)

		indexList = webControl.searchForRecordsIndex('headheadheadheadheadheadhead')
		self.assertFalse(indexList)