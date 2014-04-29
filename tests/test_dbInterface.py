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

		objList = json.loads(retPut)
		objDict = objList[2]
		# Get Dict from List
		json3str = objDict['message']
		# Pull key value from dict

		if json3str == "json3":
			pass
		else:
			self.fail(msg="JSON Mis-match")