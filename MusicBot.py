#!/usr/bin/python
from mpd import MPDClient
import time, sqlite3, Database,Logger,MPDQueueFixer, CheckButton

def Repeater():

	logObj = Logger.LoggerClass()
	buttBot = CheckButton.ButtonBot()
	
	while(True):
		try:
			print "Instance"
			logObj.AddLog()
			buttBot.Check()
			MPDQueueFixer.Fix()
			time.sleep(1)
		except KeyboardInterrupt:
			print "was exited by user!"
			return
		except:
			print "error happened in loop"
		
		
		
		
		
if __name__ == "__main__":
	conn = Database.GetConnection()
	c = conn.cursor()

	# Create table
	#c.execute('''CREATE TABLE songPlays (fileName TEXT PRIMARY KEY, times INTEGER)''')

	conn.commit()
	conn.close()
	
	Repeater()
	