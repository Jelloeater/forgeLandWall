import os
from unittest import TestCase

__author__ = 'Jesse'


class TestdbInterface(TestCase):

	def setUp(self):
		os.chdir("..")  # Go-to project root
		os.chdir("forgeLandWall")

	def tearDown(self):
		pass

	def test_getMessagesFromDBasJSONObjectArray(self):
		self.fail(msg="Unfinished Test")
		# TODO Write JSON unit test