#!/usr/bin/python
import datetime, time, mpdapi, random, AlarmModifier

updateTime = 60;

hour = 6; 
minutes = 29;

alarms = []

def UpdateAlarms():
	global alarms;
	alarms = AlarmModifier.GetTable()
	print alarms;
	
def ShouldWeAlarm():
	global alarms;
	currentDateTime = datetime.datetime.now()
	currentTime = datetime.datetime.time(datetime.datetime.now())
	for alarm in alarms:
		if(alarm["days"][currentDateTime.weekday()] == "1"):
			if(currentTime.hour == alarm["hours"] and currentTime.minute == alarm["minutes"]):
				print "RUMBO COMBO!"
				return True
		
		
	
	return False

def React():
	print "ALARM!"
	playlist = mpdapi.DoActionTrain("Ch_Pi/PLAYLIST",{"PLName":"wakeup"})["PLContent"]
	
	index = random.randint(0, len(playlist)-1)
	print playlist[index]
	time.sleep(5);
	mpdapi.DoActionTrain("ADD",
		{
		"song_names":[playlist[index]]
		})

while(True): 
	currentDateTime = datetime.datetime.now()
	currentTime = datetime.datetime.time(datetime.datetime.now())
	
	print currentTime;
	try:
	
		UpdateAlarms()
	
		if(ShouldWeAlarm()):
			React()
	except:
		print "error happened"
	time.sleep(updateTime)
	