#import tkinter
from guizero import *
import datetime
import calendar
import threading
#import socket
#import os
#import sys
from msg_parser import MessageParser
from filelock import Timeout, FileLock
#import tkinter
import json
from rss import RssFeed

settings_file = "./conf/settings.json"


#def check_settings():
#	lock = FileLock(settings_file + ".lock", timeout=2)
#	s_data = None
#	try:
#		with lock:
#			settings_data_fhandle = open(settings_file)
#			settings_data = settings_data_fhandle.read()
#			json_data = json.loads(settings_data)
#			rss_feeds = []
#			feed_titles = ""
#			rss_feeds = Text(app, text = "Test", grid=[0,0], color="white", size="35")
#			for feed in json_data["RssFeeds"]:
#				feed_info = RssFeed(feed["Name"], feed["FeedUrl"])
#				for f_3 in feed_info.news_entries:
#					feed_titles += f_3 + '\n'
#			rss_feeds.set(feed_titles)	
#
#			print(settings_data)
#	except Timeout:
#		print("Failed to acquire file lock")
#	finally:
#		lock.release()


#def spawn_thread():
#	thread = Thread(target=check_settings)
#	thread.start()


#Global Variables
global my_name
my_name = "Dr. Peng"


#Grid Location Variables - We will change these grid numbers to change Locations. [x,y]
global Time_Date_Greeting_Grid, Calendar_Grid
Time_Date_Greeting_Grid = [0,0]
Calendar_Grid = [0,3]


#Visibility for Boxes
global Time_Date_Greeting_Visible, Calendar_Visible
Time_Date_Greeting_Visible = 1
Calendar_Visible = 1

global now, display_clock, display_date
now = datetime.datetime.now()
display_clock = now.strftime("%I:%M %p")
display_date = now.strftime("%a %b-%d, %Y")
cal = calendar.TextCalendar(calendar.SUNDAY)

#class CursorOff(object)
#    def _enter_(self):
#        os.system('setterm -cursor off')
#
#    def _exit_(self,*args):
#        os.system('setterm -cursor on')



def update():
	now = datetime.datetime.now()
	display_clock.value = (now.strftime("%I:%M %p"))
	display_date.value = (now.strftime("%a %b-%d, %Y"))
        
#os.system('setterm -cursor off')
try:
	app = App(title="Mirror Mirror", width=1500, height=800, layout="grid", bg="black")

	#Black-Background Boxs- Will set all to Black525x425.png for final set. Use colors for debug
	B1 = Picture(app, image="Black525x425.png", grid=[0,0])
	B2 = Picture(app, image="Red525x425.png", grid=[0,1])
	B3 = Picture(app, image="Green525x425.png", grid=[0,2])
	B4 = Picture(app, image="Orange525x425.png", grid=[0,3])
	B5 = Picture(app, image="Yellow525x425.png", grid=[1,0])
	B6 = Picture(app, image="Blue525x425.png", grid=[1,1])


	#Time_Date_Greeting_Grid Section- WORKING!
	Box1 = Box(app,layout="grid", grid=Time_Date_Greeting_Grid, visible=Time_Date_Greeting_Visible)
	if(now.strftime("%h") < "12"):
		display_clock = Text(Box1, text = display_clock, grid=[0,0], color="white", size="45")
		display_date = Text(Box1, text = display_date, grid=[0,1], color="white", size="45")
		display_greeting = Text(Box1, text = "\nGood Morning, \n"+my_name, grid=[0,3], color="white", size="45")   

	elif(now.strftime("%h") >= "12" and now.strftime("%h") < "19"):
		display_clock = Text(Box1, text = display_clock, grid=[0,0], color="white", size="45")
		display_date = Text(Box1, text = display_date, grid=[0,1], color="white", size="45")
		display_greeting = Text(Box1, text = "\nGood Afternoon, \n"+my_name, grid=[0,3], color="white", size="45")

	elif(now.strftime("%h") >= "19"):
		display_clock = Text(Box1, text = display_clock, grid=[0,0], color="white", size="45")
		display_date = Text(Box1, text = display_date, grid=[0,1], color="white", size="45")
		display_greeting = Text(Box1, text = "\nGood Evening, \n"+my_name, grid=[0,3], color="white", size="45")


	#Calandar Section. Not working, Everything is center aligned not aligned, not in columns
	year = int(now.strftime("%Y"))
	month = int(now.strftime("%-m"))
	calFormat = cal.formatmonth(year,month,0,0)
	print(calFormat, flush=True)
	Box2 = Box(app, grid=Calendar_Grid, visible = Calendar_Visible)
	display_calendar = Text(Box2, text = calFormat, color="white", size="35", align="left")
	Box3 = Box(app, layout="grid", grid=[0,1], visible=True)
	Box4 = Box(app, layout="grid", grid=[0,2], visible=True)
	Box5 = Box(app, layout="grid", grid=[1,1], visible=True)
	q1 = "Test1"
	q2 = "Test2"
	q3 = "Test3"
	q4 = "Test4"
	q5 = "Test5"
	Text1 = Text(Box1, text=q1, grid=[0, 2], color="white", size="8", align="left")
	Text2 = Text(Box2, text=q2, grid=[1, 1], color="white", size="8", align="left")
	Text3 = Text(Box3, text=q3, grid=[1, 1], color="white", size="8", align="left")
	Text4 = Text(Box4, text=q4, grid=[1, 1], color="white", size="8", align="left")
	Text5 = Text(Box5, text=q5, grid=[1, 1], color="white", size="8", align="left")
	app.repeat(500,update)
	#app.repeat(1000, spawn_thread)
	#sets full screen-Makes debug hard. To Get out: CTR+ALT+D
	app.tk.attributes("-fullscreen", True)
	def start_listening():

		def update_quads(bindings, quads):
			if quads[0]['ItemType'] != None:
				q1 = bindings.get(quads[0]['ItemType'])
				Text1.value = q1
				print(bindings.get(quads[0]['ItemType']))
			if quads[1]['ItemType'] != None:
				q2 = bindings.get(quads[1]['ItemType'])
				Text2.value = q2
				print(bindings.get(quads[1]['ItemType']))
			if quads[2]['ItemType'] != None:
				q3 = bindings.get(quads[2]['ItemType'])
				Text3.value = q3
				print(bindings.get(quads[2]['ItemType']))
			if quads[3]['ItemType'] != None:
				q4 = bindings.get(quads[3]['ItemType'])
				Text4.value = q4
				print(bindings.get(quads[3]['ItemType']))
			if quads[4]['ItemType'] != None:
				q5 = bindings.get(quads[4]['ItemType'])
				Text5.value = q5
				print(bindings.get(quads[4]['ItemType']))

		def msg_callback(body):
			lock = threading.Lock()
			lock.acquire()
			json_data = json.loads(body)
			quads = json_data["Cfg"]
			rss_feeds = json_data["RssFeeds"]
			weather_locs = json_data["WeatherLocations"]
			google_info = json_data["GoogleInfo"]
			feed_text = RssFeed(rss_feeds).get_entries()
			bindings = {"RSS Feeds": feed_text}
			update_quads(bindings, quads)
			lock.release()
		msg = MessageParser(msg_callback)
		msg.start_listening()

	thread = threading.Thread(target=start_listening)
	thread.start()

	#nocursor is not working to turn cursor to be invisible.
	#will need to find something else to make it invisible or move position to side/corner
	app.display()

except KeyboardInterrupt:
	quit()

