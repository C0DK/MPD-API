#!/usr/bin/python
from subprocess import call

#get all files

def MakeMetadata():
	dirToMusic = "/home/pi/music/yt"
	allinDir = os.listdir(dirToMusic)