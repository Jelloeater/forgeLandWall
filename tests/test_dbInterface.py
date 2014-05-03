import os
from unittest import TestCase

from forgeLandWall import dbInterface


__author__ = 'Jesse'


class TestDbInterface(TestCase):

	def setUp(self):
		os.chdir("..")  # Go-to project root
		os.chdir("forgeLandWall")

		import forgeLandWall.models as models

		x=models.messageModel()
		x.message("json1")
		x=models.messageModel()
		x.message("json2")
		x=models.messageModel()
		x.message("json3")
		print("TEST SETUP")

	def tearDown(self):
		"""Delete test messages"""
		from forgeLandWall.dbConnManage import dbConnManage
		dbConn, dbcursor = dbConnManage.dbConnect()
		messageStr = "json"
		sqlStr = 'DELETE FROM messages WHERE "message" LIKE "%' + messageStr + '%";'
		dbcursor.execute(sqlStr)
		dbConnManage.dbClose(dbConn)
		print("TEST TEARDOWN")

	def test_getMessagesFromDBasJSONObjectArray(self):
		import json

		retPut = dbInterface.dbInterface.getMessagesFromDBasJSONObjectArray(3)
		# Get the Data from the db

		objList = json.loads(retPut)
		objDict = objList[2]
		# Get Dict from List
		json3str = objDict['message']
		# Pull key value from dict

		self.assertEquals(json3str, "json3", "JSON Mismatch")


	def test_searchMessagesFromDB(self):
		results = dbInterface.dbInterface.searchMessagesFromDB("json")
		x = results[2]

		self.assertEqual(x[0], "json3")