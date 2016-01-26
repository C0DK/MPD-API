#!/usr/bin/python2
import RPi.GPIO as GPIO
#from mpd import MPDClient
#from MPDHelper import GetMPD
import time, mpdapi
from espeak import espeak


class ButtonBot():

	toggleState = False;
	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		self.toggleState = GPIO.input(18)

	def Check(self):

		input_state = GPIO.input(18)
		if(self.toggleState != input_state):
			print('Button Pressed ='+str(input_state))
			self.toggleState = input_state;
			if(self.toggleState):
				mpdapi.DoActionTrain("ADD", #PLAYLAST
					{
						#"song_names":[u"Music/Soul & RnB/Mighty Sam McClain"]
						#"song_names":["yt/Miguel - Coffee.mp3"]
						"song_names":["yt/Kenny Loggins - Danger Zone.mp3"]
					})
		
	def __exit__(self, exc_type, exc_value, traceback):
		GPIO.cleanup()

if __name__ == "__main__":
	while True :
		Check();
		time.sleep(0.2)

