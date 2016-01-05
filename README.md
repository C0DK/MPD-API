# MPD-API
I made a API for MPD that automaticly downloads songs from youtube and plays on demand with an easy to use API which can easily be connected to an HTTP server.

## Work in progress 

## Requires:
An Youtube/Google API v3 key (for the search functionality)
  Get it:
    https://cloud.google.com/console > APIs & auth > Registered apps
  Source:
    https://developers.google.com/youtube/v3/code_samples/python
  
MPDClient (Python lib)
  Get it:
    pip install python-mpd2
  Source:
    http://pythonhosted.org/python-mpd2/
pytube
  Get it:
    pip install pytube
  Source:
    https://github.com/nficano/pytube

## Notes:

This only works with an MPD server running on localhost:6600

## How To:

Use by calling DoAPI(URI,data)

## Example:

DoAPI("DOWNLOAD/CONVERT/ADD/PLAY",
	{
    "url":"https://www.youtube.com/watch?v=20Ov0cDPZy8"
	})
	
This simply downloads the song with said URL (Free Falling by John Mayer), 
converts the download to mp3, adds it to the mpd server, and plays it.


