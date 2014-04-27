import os
from unittest import TestCase

from forgeLandWall import dbInterface


__author__ = 'Jesse'


class TestdbInterface(TestCase):

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
		import forgeLandWall.dbConnManage as dbConnManage
		dbConn, dbcursor = dbConnManage.dbConnect()
		messageStr = "json"
		sqlStr = 'DELETE FROM messages WHERE "message" LIKE "' + messageStr + '";'
		dbcursor.execute(sqlStr)
		dbConnManage.dbClose(dbConn)
		print("TEST TEARDOWN")

	def test_getMessagesFromDBasJSONObjectArray(self):
		import json

		retPut = dbInterface.getMessagesFromDBasJSONObjectArray(3)
		# Get the Data from the db

		ObjList = json.loads(retPut)
		testStr = ObjList[0].message
		print("JSON: " + retPut)
		print("JSONtoObj: " + testStr)
		if retPut == testStr:
			pass
		else:
			self.fail(msg="Unfinished Test")
		# TODO Write JSON unit test