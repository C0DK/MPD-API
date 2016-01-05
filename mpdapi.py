#!/usr/bin/python
import ytsearch, ytdownload, convertfiles
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
			#print "song = "+ song
			client.add("yt/"+song)
			state = client.status()["state"]
			if(state == "pause"):
				client.pause(0)
			elif(state == "stop"):
				client.play()
			client.disconnect()
			
	if(URI == "PLAY"):
		client = GetMPD()	
		if(state == "pause"):
			client.pause(0)
		elif(state == "stop"):
			client.play()
		client.disconnect()
	
	if(URI == "SEARCH"):
		data["yt_elements"] = ytsearch.youtube_search(data["query"],5)
		return data
		
	
	if(URI == "PLAYLAST"):
		client = GetMPD()
		queue = client.status()
		client.play(int(queue["playlistlength"])-1)
		client.disconnect()
		
	return data
	
def DoActionTrain(URI,data):
	while URI != "":
		action = GetCurrentURI(URI)
		URI = CutURI(URI)
		DoAction(action,data)
		
	return data


def DoAPI(URI, data):
	#only works with single songs
	if URI.startswith("GET"):
		print "input "+data["url"]
		#commands = ["sudo","python","/home/pi/scripts/dl-yt"]
		#commands.extend(data["url"].split(" "))
		#Popen(commands)
		result = ytdownload.Download(data["url"])
		
		if URI.startswith("GET/ADD"):
			client = GetMPD()
			print " "
			#print client.currentsong()
			client.add("yt/"+result)
			
		
		if URI.startswith("GET/PLAY"):
			client = GetMPD()
			print " "
			#print client.currentsong()
			client.add("yt/"+result)
			queue = client.status()
			#print len(queue)
			client.play(int(queue["playlistlength"])-1)
			client.disconnect()
			
		return {"result":"sucess","songName":result}
	if(URI.startswith("SEARCH")):
		result = ytsearch.youtube_search(data["query"],5)
		return {"result":"success_result","search":result}	
		
	return {"result":"no func found"}	

if __name__ == "__main__":
	returned = DoAPI("SEARCH",
	{
	#"url":"https://www.youtube.com/watch?v=8Uee_mcxvrw"
	"query":"kendrick lamar"
	})
	print returned
		