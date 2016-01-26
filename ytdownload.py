#!/usr/bin/python2
# -*- coding: utf-8 -*-

from pytube import YouTube
import pprint, sys, os, shutil, time
from mpd import MPDClient
from subprocess import call


def Download(songURI, bestQuality = False):
	filetype = "mp4"
	#Check if NAS is mounted
	nasDir = '/home/pi/music/yt/'
	bckDir = '/home/pi/musicBAK/'
	dirUse = nasDir
	if os.path.isdir(nasDir):
		#put bck files into nasDirs
		bakFiles = os.listdir(bckDir)
		for x in range(0,len(bakFiles)):
			shutil.copy(bckDir+bakFiles[x], nasDir+bakFiles[x])
			os.remove(bckDir+bakFiles[x])
	else:
		dirUse = bckDir

	#if input is null then return
	if songURI == "":
		return
	
	songURL = "https://www.youtube.com/watch?v="+songURI
	#use full url if that is given
	if  "youtube.com" in songURI:
		songURL = songURI
	try:
		yt = YouTube(songURL)
	except:
		print "ERROR: URL is not a video!"
	
	
	if bestQuality:
		video = yt.filter(filetype)[-1]
	else :
		video = yt.filter(filetype)[0]
	print "starting download to '" + dirUse + "'";
	
	try:
		video.download(dirUse);
		print "down succeeded"
	except:
		print "download failed:", sys.exc_info()
		

	if dirUse == nasDir:
		client = MPDClient()           # create client object
		client.connect("localhost", 6600)  # connect to localhost:6600
		#client.update("yt/"+yt.filename + "."+filetype)
		
		#Hack so that it will wait for the fucking update.
		call(["mpc", "update",("yt/"+yt.filename+"."+filetype),"-w"])
		
		client.disconnect()
	
	time.sleep(0.1);
	
	return yt.filename + "."+filetype


if __name__ == "__main__":
	for x in range(1,len(sys.argv)):
		#songURI = sys.argv[x]
		Download(sys.argv[x])