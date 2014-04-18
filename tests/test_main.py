from unittest import TestCase
from forgeLandWall import WallWebApp
import urllib2
__author__ = 'Jesse'


class TestMain(TestCase):
	def setUp(self):
		pass

	def test_main(self):
		url = "http://"+str(WallWebApp.ip)+":"+str(WallWebApp.port)+"/"

		print("Testing: " + url)

		website = urllib2.urlopen(url)
		website_html = str(website.read())
		flag = website_html.__contains__("<pre>")

		TestCase.assertEqual(self, flag, True, "Invalid Server Response")

if __name__ == '__main__':
	TestMain.setUp()