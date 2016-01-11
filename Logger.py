#!/usr/bin/python
from mpd import MPDClient
from MPDHelper import GetMPD
import sqlite3, Database
class LoggerClass():
	
	lastSong = ""
	lastTime = 0
	
	def __init__(self):
		self.StartLog()

	def CreateLogger():
		conn = Database.GetConnection()
		c = conn.cursor()

		# Create table
		c.execute('''CREATE TABLE songPlays (fileName TEXT PRIMARY KEY, times INTEGER)''')

		conn.commit()
		conn.close()

	def StartLog(self):
		client = GetMPD()
		state = client.status()
		if(state['state'] == "play"):
			currentSong = client.currentsong()
			self.lastSong = currentSong['file']
			self.lastTime = state['elapsed']
			client.disconnect();

	def AddLog(self):

		client = GetMPD()
		state = client.status()
		currentSong = client.currentsong()
				
		if(state['state'] != "play"):
			client.disconnect()
			return
		
		print "time= "+currentSong['time']
		
		if(currentSong['file'] == self.lastSong and state['elapsed'] >= self.lastTime):
			client.disconnect()
			return
		
		self.lastSong = currentSong['file']
		self.lastTime = state['elapsed']
		
		print self.lastSong
		
		conn = Database.GetConnection()
		c = conn.cursor()
		
		Exists = c.execute("SELECT EXISTS(SELECT 1 FROM songPlays WHERE fileName=? LIMIT 1)",(self.lastSong,));
		
		if(Exists.fetchone()[0] == 0):
			c.execute("INSERT INTO songPlays VALUES (?,1)",(self.lastSong,))
		else:
			c.execute("UPDATE songPlays SET times=times+1 WHERE fileName=?",(self.lastSong,))	
		
		conn.commit()
		
		conn.commit()
		conn.close()
		client.disconnect();