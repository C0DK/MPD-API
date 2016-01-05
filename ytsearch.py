#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyA8_6wdobpUNy9LeT32P59EY99GWq7N9mg"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(query,max_results=5):
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
	developerKey=DEVELOPER_KEY)
	
	# Call the search.list method to retrieve results matching the specified
	# query term.
	search_response = youtube.search().list(
		q=query,
		type="video",
		part="id,snippet",
		maxResults=max_results
		).execute()

	videos = []
	channels = []
	playlists = []

	# Add each result to the appropriate list, and then display the lists of
	# matching videos, channels, and playlists.
	for search_result in search_response.get("items", []):
		if search_result["id"]["kind"] == "youtube#video":
			videos.append({
			"title":search_result["snippet"]["title"],
			"uri":search_result["id"]["videoId"],
			"pic":search_result["snippet"]["thumbnails"]["high"]["url"]
			})
	return videos
	
if __name__ == "__main__":
	try:
		query = "test"
		print "searching for: "+query
		#youtube_search(query)
		
	except HttpError, e:
		print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)