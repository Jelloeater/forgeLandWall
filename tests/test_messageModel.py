from unittest import TestCase

import forgeLandWall.models as models


__author__ = 'Jesse'


class TestMessageModel(TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_message(self):
		# Write
		messageStr = "testMessagePleaseIgnore"
		dbObj = models.messageModel()
		dbObj.message(messageStr)

		# Search and read back
		dbObj2 = models.messageModel(message=messageStr)
		dbMessageStr = dbObj2.message()

		if dbMessageStr is messageStr:
			pass
		else:
			self.fail()

			# FIXME Test need db path to be absolute!