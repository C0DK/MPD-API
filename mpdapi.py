#!/usr/bin/python
import ytsearch, ytdownload, convertfiles, sqlite3
from mpd import MPDClient

def GetCurrentURI(URI):
	return URI.split("/")[0]
	
def CutURI(URI):
	first = GetCurrentURI(URI)
	lngth = len(first)
	return URI[lngth+1:]
	
def GetMPD():
	client = MPDClient()           # create client object
	client.connect("localhost", 6600)  # connect to localhost:6600
	return client

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
			data["song_names"].append(ytdownload.Download(url))
	
	if(URI == "CONVERT"):
		convertfiles.DoConvert();
	
	if(URI == "ADD"):
		while len(data["song_names"]) != 0:
			song = data["song_names"].pop()
			client = GetMPD()
			client.add("yt/"+song)
			state = client.status()["state"]
			if(state == "pause"):
				client.pause(0)
			elif(state == "stop"):
				client.play()
			client.disconnect()
			
	if(URI == "PLAY"):
		client = GetMPD()
		state = client.status()["state"]
		if(state == "pause"):
			client.pause(0)
		elif(state == "stop"):
			client.play()
		elif(state == "play"):
			client.pause(1);
		client.disconnect()
		
	if(URI == "STATS"):
		conn = sqlite3.connect('/home/pi/scripts/mpd/example2.db')
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
		data["yt_elements"] = ytsearch.youtube_search(data["query"],5)
		#return data
		
	
	if(URI == "PLAYLAST"):
		client = GetMPD()
		queue = client.status()
		client.play(int(queue["playlistlength"])-1)
		client.disconnect()
		
	if(URI == "STATUS"):
		client = GetMPD()
		data["status"] = client.status()
		
	if(URI == "GETQUEUE"):
		client = GetMPD()
		data["queue"] = client.playlistinfo()
		
		
	return data
	
def DoActionTrain(URI,data):
	while URI != "":
		action = GetCurrentURI(URI)
		URI = CutURI(URI)
		DoAction(action,data)
		
	return data

if __name__ == "__main__":
	returned = DoActionTrain("GETQUEUE",
	{
		"query":"kendrick lamar"
	})
	print returned
		