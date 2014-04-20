__author__ = 'smerlin'
import os
import socket

if os.name != "nt":
	import fcntl
	import struct

	def __get_interface_ip(interfaceName):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', interfaceName[:15]))[20:24])


def get_lan_ip():
	ip = socket.gethostbyname(socket.gethostname())
	if ip.startswith("127.") and os.name != "nt":  # Checks for loop back adapter
		interfaces = [
			"eth0",
			"eth1",
			"eth2",
			"wlan0",
			"wlan1",
			"wifi0",
			"ath0",
			"ath1",
			"ppp0",
		]

		for interfaceName in interfaces:
			try:
				ip = __get_interface_ip(interfaceName)
				# if not ip.startswith("10."):  # Rejects specific ip addresses?
				break
			except IOError:
				pass
	return ip

def getIpSocket():
	return socket.gethostbyname(socket.gethostname())