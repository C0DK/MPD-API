#!/usr/bin/python
import os, datetime
from subprocess import call


def DoConvert():

	startTime = datetime.datetime.now()
	dirToMusic = "/home/pi/music/yt"
	allinDir = os.listdir(dirToMusic)
	
	print "Converting files.."
	mp4s = []
	
	for obj in allinDir:
		if obj.endswith(".mp4"):
			mp4s.append(obj)
			
	for file in mp4s:
		filename = file.split(".")[0]
		print "	converting '"+filename+"'";
		newFile = dirToMusic+"/"+filename+".mp3"
		oldFile = dirToMusic+"/"+file
		call(["ffmpeg","-i",oldFile,newFile], stdout=open(os.devnull, 'wb'))
		if os.path.isfile(newFile):
			os.remove(oldFile)
			
	endTime = datetime.datetime.now()
	print "-------------------------"
	print "Start time="+str(startTime.hour) + ":"+str(startTime.minute)+":"+str(startTime.second) + ","+str(startTime.microsecond)
	print "End time="+str(endTime.hour) + ":"+str(endTime.minute)+":"+str(endTime.second) + ","+str(endTime.microsecond)
	deltatime = (endTime - startTime)
	print "difference "+str(deltatime.microseconds)+" microseconds"
	print "("+str(deltatime.seconds)+" seconds)"
	
	print "-------------------------"
if __name__ == "__main__":
	DoConvert()
		