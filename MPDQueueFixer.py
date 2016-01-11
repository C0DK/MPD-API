#!/usr/bin/python
from mpd import MPDClient
from MPDHelper import GetMPD

##########
#Fixes it so that the playing song is always first in the queue. 
#anything else would be freaky amirite?
##########

def Fix():
	client = GetMPD()
	
	state = client.status()
	if(state['state'] == "stop"): 
		client.disconnect()
		return
	
	while(client.currentsong()["pos"] != "0"):
		queue = client.playlistinfo()
		print queue
		songName = queue[0]["file"]
		songID = queue[0]["id"]
		client.deleteid(songID)
		client.add(songName)
	
	client.disconnect()
	
	

if __name__ == "__main__":
	Fix()