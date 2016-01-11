#!/usr/bin/python
from mpd import MPDClient
	
def GetMPD():
	client = MPDClient()           # create client object
	client.connect("localhost", 6600)  # connect to localhost:6600
	return client