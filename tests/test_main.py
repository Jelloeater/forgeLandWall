from unittest import TestCase
import urllib2
import os
from subprocess import Popen
import time

import forgeLandWall.settings as settings

__author__ = 'Jesse'

class TestMain(TestCase):
	def setUp(self):
		os.chdir("..")  # Go-to project root
		os.chdir("forgeLandWall")
		Popen(["python", "main-controller.py"])  # Runs server in the background
		time.sleep(.25)  # Gives server time to start

	def tearDown(self):
		pass

	def test_main(self):
		url = "http://" + str(settings.getIpAddress()) + ":" + str(settings.globalVars.portNumber)
		url = url.strip()
		print('TEST SERVER @ ' + url)
		website = urllib2.urlopen(url)
		website_html = str(website.read())
		flag = website_html.__contains__("<pre>")
		TestCase.assertTrue(self,flag, "Invalid Server Response")