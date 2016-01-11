#!/usr/bin/python
from mpd import MPDClient
import time, sqlite3, mpdapi

DBdir = '/home/pi/scripts/mpd/example2.db'


lastSong = "";
lastTime = 0;

def Log():

	client = mpdapi.GetMPD()
	state = client.status()
	currentSong = client.currentsong()
	
	global lastSong;
	global lastTime;
	
	if(state['state'] != "play"):
		return
	
	print "time= "+currentSong['time']
	
	if(currentSong['file'] == lastSong and state['elapsed'] >= lastTime):
		return
	
	#lastSong = "test"
	lastSong = currentSong['file']
	lastTime = state['elapsed']
	
	print currentSong
	
	conn = sqlite3.connect(DBdir)
	c = conn.cursor()
	
	Exists = c.execute("SELECT EXISTS(SELECT 1 FROM songPlays WHERE fileName=? LIMIT 1)",(lastSong,));
	
	if(Exists.fetchone()[0] == 0):
		c.execute("INSERT INTO songPlays VALUES (?,1)",(lastSong,))
	else:
		c.execute("UPDATE songPlays SET times=times+1 WHERE fileName=?",(lastSong,))	
	
	#print "exists0"+str(Exists.fetchone());
	
	conn.commit()
	commandResult = c.execute("SELECT * FROM songPlays where fileName=?",(lastSong,))
	
	for row in commandResult:
		print row
	
	result = commandResult.fetchone()
	print "selected=" +str(result);
	conn.commit()
	conn.close()
	client.disconnect();


def Repeater():

	client = mpdapi.GetMPD()
	state = client.status()
	if(state['state'] == "play"):
		currentSong = client.currentsong()
		global lastSong
		global lastTime
		lastSong = currentSong['file']
		lastTime = state['elapsed']
		client.disconnect();
	
	while(True):
		print "Instance"
		Log()
		time.sleep(1)
		
		
		
		
		
if __name__ == "__main__":
	conn = sqlite3.connect(DBdir)
	c = conn.cursor()

	# Create table
	#c.execute('''CREATE TABLE songPlays (fileName TEXT PRIMARY KEY, times INTEGER)''')

	conn.commit()
	conn.close()
	
	Repeater()
	