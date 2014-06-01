import json
from unittest import TestCase
import constants
import models
from forgeLandWall.controler import webControl

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
		# ONLY TESTS FOR EMPTY LIST (we need a better test)
		# TODO Write a better test (see webControl TODO's)
		# Create message
		dbObj = models.messageModel()
		dbObj.message(constants.messageStr)

		# Search for index
		indexList = webControl.searchRecords(constants.messageStr)
		dbObj2 = models.messageModel(index=indexList[0])
		testStr = dbObj2.message()

		self.assertEqual(constants.messageStr, testStr)

		indexList = webControl.searchRecords('headheadheadheadheadheadhead')
		self.assertFalse(indexList)

	def test_searchForMessagesJSON(self):
		dbObj = models.messageModel()
		dbObj.message(constants.messageStr)

		rawJSON = webControl.searchForMessagesJSON(constants.messageStr)
		jsonObj = json.loads(rawJSON)
		jsonTest = jsonObj[0]['message']

		self.assertEqual(constants.messageStr, jsonTest)