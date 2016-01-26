#!/usr/bin/python
import ytsearch, ytdownload, convertfiles, sqlite3, Database, ir
from mpd import MPDClient
from MPDHelper import GetMPD

def GetCurrentURI(URI):
	return URI.split("/")[0]
	
def CutURI(URI):
	first = GetCurrentURI(URI)
	lngth = len(first)
	return URI[lngth+1:]
	
#def GetMPD():
#	client = MPDClient()           # create client object
#	client.connect("localhost", 6600)  # connect to localhost:6600
#	return client

def doRepeat(func, data, dataDenominator):
	for obj in data[dataDenominator]:
		func(obj)
	del data[dataDenominator]
	return data
	
def DoAction(URI, data):
	if(URI == "DOWNLOAD"):
		
		while len(data["url"]) != 0:
			url = data["url"].pop()
			if not ("song_names" in data) : 
				data["song_names"] = []
			data["song_names"].append("yt/"+ytdownload.Download(url))
	
	if(URI == "CONVERT"):
		convertfiles.DoConvert();
	
	if(URI == "ADD"):
		while len(data["song_names"]) != 0:
			song = data["song_names"].pop()
			print "song to play="+song
			client = GetMPD()
			client.add(song)
			state = client.status()["state"]
			if(state == "pause"):
				client.pause(0)
			elif(state == "stop"):
				client.play()
			client.disconnect()
			
	if(URI == "PLAY"):
		client = GetMPD()
		state = client.status()["state"]
		print "state="+state
		if(state == "pause"):
			client.pause(0)
		elif(state == "stop"):
			client.play()
		elif(state == "play"):
			client.pause(1);
		client.disconnect()

	if(URI == "Ch_Pi"):
                ir.ChPi();

		
			
	if(URI == "STATS"):
		conn = Database.GetConnection()
		c = conn.cursor()
		songs = c.execute("SELECT * FROM songPlays ORDER BY times DESC")
		data["stats"] = [];	
		for song in songs:
			data["stats"].append({"song":str(song[0]),"times":str(song[1])})
		
	if(URI == "STOP"):
		client = GetMPD()	
		client.stop()
		client.disconnect()
		
	if(URI == "NEXT"):
		client = GetMPD()	
		client.next()
		client.disconnect()
	
	if(URI == "SEARCH"):
		data["yt_elements"] = ytsearch.youtube_search(data["query"],15)
		#return data
		
	if(URI == "CLEAR"):
		client = GetMPD()
		client.clear()
		client.disconnect()
	
	if(URI == "PLAYLAST"):
		client = GetMPD()
		queue = client.status()
		client.play(int(queue["playlistlength"])-1)
		client.disconnect()
		
	if(URI == "STATUS"):
		client = GetMPD()
		data["status"] = client.status()
		client.disconnect()
		
	if(URI == "GETQUEUE"):
		client = GetMPD()
		data["queue"] = client.playlistinfo()
		client.disconnect()
		
	if(URI == "LS"):
		client = GetMPD()
		lsLookup = client.lsinfo(data["LS-dir"])
		data["LS-dir"] = ""
		data["LSresult"] = lsLookup
		client.disconnect()
		
	if(URI == "VOLUMEUP"):
		ir.VolumeUp(5)
		
	if(URI == "PLAYLIST"):
		client = GetMPD()
		data["PLContent"] = client.listplaylist(data["PLName"])
		
		data["PLName"] = ""
		
		client.disconnect()
		
	if(URI == "VOLUMEDOWN"):
		ir.VolumeDown(5);
	if(URI == "POWER"):
		ir.Power();
		
		#data["VolumeTimes"] = ""
		#data["LS-result"] = lsLookup
			
	return data
	
def DoActionTrain(URI,data):
	while URI != "":
		action = GetCurrentURI(URI)
		URI = CutURI(URI)
		DoAction(action,data)
		
	return data

if __name__ == "__main__":
	returned = DoActionTrain("LS",
	{
		"LS-dir":"/"
	})
	print returned
		
