#!/usr/bin/python

import sqlite3, Database
import pprint

def CreateTable():
	conn = Database.GetConnection()
	c = conn.cursor()

	# Create table
	c.execute('''CREATE TABLE alarms 
		(id INTEGER PRIMARY KEY, active INTEGER, hours INTEGER, minutes INTEGER, days TEXT, type TEXT)''')

	conn.commit()
	c.execute("INSERT INTO alarms VALUES (0,1,6,30,'1111100','')")
	conn.commit()
	conn.close()
	
def NewAlarm(hours,minutes,days):
	
	conn = Database.GetConnection()
	c = conn.cursor()
	index = c.execute("SELECT id FROM alarms ORDER BY id DESC LIMIT 1").fetchone()[0]
	print index
	index += 1;
	print index
	c.execute("INSERT INTO alarms VALUES (?,?,?,?,?,?)",(index,1,hours,minutes,days,"",))
	
	#pprint.pprint(c.execute("SELECT * FROM alarms"))
	for row in c.execute("SELECT * FROM alarms"):
		print row
	print "--"
	conn.commit()
	conn.close()

def SetActiveAlarm(id,active):
	
	conn = Database.GetConnection()
	c = conn.cursor()
	c.execute("UPDATE alarms SET active=? WHERE id=?",(active,id))
	
	conn.commit()
	#pprint.pprint(c.execute("SELECT * FROM alarms"))
	for row in c.execute("SELECT * FROM alarms"):
		print row
	print "--"
		
	conn.commit()
	conn.close()

def UpdateTable(id, hours,minutes,days):
	conn = Database.GetConnection()
	c = conn.cursor()
	c.execute("UPDATE alarms SET hours=? minutes=? days=? WHERE id=?",(hours,minutes,days,id))
	
	conn.commit()
	conn.close()
	
	
def DropTable():
	conn = Database.GetConnection()
	c = conn.cursor()
	
	c.execute("DROP TABLE alarms")
	
	conn.commit()
	conn.close()
	
def GetTable():
	conn = Database.GetConnection()
	c = conn.cursor()
	alarms = c.execute("SELECT * FROM alarms")
	
	output = []
	
	for row in alarms:
		output.append({"id":row[0],"active":row[1],"hours":row[2],"minutes":row[3],"days":row[4],"type":row[5]})
		 
	conn.close()
	
	return output;
	
	
if __name__ == "__main__":
	DropTable();
	CreateTable()
	#NewAlarm(8,00,"1111111")
	#SetActiveAlarm(1,0);
	print GetTable()