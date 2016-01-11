#!/usr/bin/python
from mpd import MPDClient
import time, sqlite3, Database,Logger,MPDQueueFixer

def Repeater():

	logObj = Logger.LoggerClass()
	
	while(True):
		print "Instance"
		logObj.AddLog()
		MPDQueueFixer.Fix()
		time.sleep(1)
		
		
		
		
		
if __name__ == "__main__":
	conn = Database.GetConnection()
	c = conn.cursor()

	# Create table
	#c.execute('''CREATE TABLE songPlays (fileName TEXT PRIMARY KEY, times INTEGER)''')

	conn.commit()
	conn.close()
	
	Repeater()
	