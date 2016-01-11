#!/usr/bin/python
import sqlite3


DBdir = '/home/pi/scripts/mpd/example2.db'

def GetConnection():
	return sqlite3.connect(DBdir)