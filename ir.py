#!/usr/bin/python
#from lirc.lirc import Lirc 
from subprocess import call

device = "STR-DE205"

def SendCommand(command, times = 1):
	call(["irsend","SEND_ONCE",device,command,"-#",str(times)])
	
if __name__ == "__main__":
	SendCommand("KEY_POWER")

#lircParse = Lirc('/etc/lirc/lircd.conf') 
#lircParse.send_once("STR-DE205", "KEY_VOLUMEUP")

def VolumeUp(times = 1):
	SendCommand("KEY_VOLUMEUP",times)

def VolumeDown(times = 1):
	SendCommand("KEY_VOLUMEDOWN",times)
	
def Power():
	SendCommand("KEY_POWER")
def Mute():
	SendCommand("KEY_MUTE")

def ChPi():
	SendCommand("KEY_TV")
