import sys, os
sys.path.append('/home/pi/Desktop/MirrorMirror/CapstoneII')
from guizero import *
import datetime
import calendar
import RPi.GPIO as GPIO
import time
from msg_parser import MessageParser
from filelock import Timeout, FileLock
import tkinter
import threading
from rss import RssFeed
from weather import Weather
import json
from PIL import Image, ImageDraw, ImageFont
from GoogleAPI import Google

settings_file = "./conf/settings.json"

#GPIO SETUP
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#LED Button and Output Pin - Button: GPIO26, Control: GPIO19
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(19, GPIO.OUT)
GPIO.output(19, GPIO.LOW)
global lastPressLED
lastPressLED =0

#Button2
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#Button3
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#Button4
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#Button5-RestartButton
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

global lastPress2, lastPress3, lastPress4, lastPress5
lastPress2 = 0
lastPress3 = 0
lastPress4 = 0
lastPress5 = 0

global Box1, Box2, Box3, Box4, Box5
#Global Variables
global my_name
my_name = "UW-Stout"


#Grid Location Variables - We will change these grid numbers to change Locations. [x,y]
global Time_Date_Greeting_Grid, Calendar_Grid
Time_Date_Greeting_Grid = [0,0]
Calendar_Grid = [0,3]
Email_Grid = [0,2]
Events_Grid = [0,1]

global year, month

#Visibility for Boxes
global Time_Date_Greeting_Visible, Calendar_Visible, Emails_Visible, Events_Visible
Time_Date_Greeting_Visible = 1
Calendar_Visible = 1
Emails_Visible = 1
Events_Visible = 1

#construct google object
goog = Google()

global now, display_clock, display_date, clock, date, display_emails, display_events, emails, events, access_token
now = datetime.datetime.now()
clock = now.strftime("%I:%M %p")
date = now.strftime("%a %b-%d, %Y")
cal = calendar.TextCalendar(calendar.SUNDAY)
access_token = ""
rss_feeds = []
emails = []
events = []

#def read_settings():
#    lock = FileLock(settings_file + ".lock", timeout=2)
#    try:
#        with lock:
#            with open(settings_file, 'r') as settings:
#                settings_val = json.loads(settings.read())
#                print(settings_val)
#                rss_feeds = []
#                try:
#                    rss_feeds = RssFeed(settings_val["RssFeeds"])
#                except:
#                    print("Problem reading rss feeds")
 #               print("Received RSS Feeds.")
 #               weather_locs = []
 ##               for locations in settings_val["WeatherLocations"]:
  #                  print(locations)
  #                  loc = Weather(locations).get_results()
  #                  weather_locs.append(loc)
  #                  print(loc)
  #              
  #              access_token = settings_val['GoogleInfo']['AccessToken']
  #              print(access_token)
  #  except Timeout: print("failed to acquire lock")
  #  finally:
  #      lock.release()


    #Events Updating
    #   display_events = Text(Box4, text = , grid=[0,0], color="white", size="20")



def update():
    global year, month
    global now, display_clock, display_date, clock, date, display_emails, display_events
    global my_name
    global Box1, Box2
    #Clock Updating
    now = datetime.datetime.now()
    #if(clock == now.strftime("%I:%M %p")):
        #print("No Update Required")
        
    if(clock != now.strftime("%I:%M %p")):
        #print("Updating Clock:")
        #print(clock)
        #print(now.strftime("%I:%M %p"))
        clock = now.strftime("%I:%M %p")
        date = now.strftime("%a %b-%d, %Y")
        if(now.strftime("%H") == "03" or now.strftime("%H") == "04" or now.strftime("%H") == "05" or now.strftime("%H") == "06" or now.strftime("%H") == "07" or now.strftime("%H") == "08" or now.strftime("%H") == "09" or now.strftime("%H") == "10" or now.strftime("%H") == "11"):
            display_clock = Text(Box1, text = clock, grid=[0,0], color="white", size="35")
            display_date = Text(Box1, text = date, grid=[0,1], color="white", size="35")
            display_greeting = Text(Box1, text = "\nGood Morning, \n"+my_name, grid=[0,3], color="white", size="35")   

        elif(now.strftime("H") =="12" or now.strftime("%H") == "13" or now.strftime("%H") == "14" or now.strftime("%H") == "15" or now.strftime("%H") == "16" or now.strftime("%H") == "17"):
            display_clock = Text(Box1, text = clock, grid=[0,0], color="white", size="35")
            display_date = Text(Box1, text = date, grid=[0,1], color="white", size="35")
            display_greeting = Text(Box1, text = "\nGood Afternoon, \n"+my_name, grid=[0,3], color="white", size="35")

        else:
            display_clock = Text(Box1, text = clock, grid=[0,0], color="white", size="35")
            display_date = Text(Box1, text = date, grid=[0,1], color="white", size="35")
            display_greeting = Text(Box1, text = "\nGood Evening, \n"+my_name, grid=[0,3], color="white", size="35")

    #Calandar Updating
    if(month != int(now.strftime("%-m"))):
        year = int(now.strftime("%Y"))
        month = int(now.strftime("%-m"))
        calFormat = cal.formatmonth(year,month,3,0)
            
        calImage = Image.new('RGB', (525,425), color = (0,0,0))
        #CalFont = ImageFont.truetype(ImageFont.load_default(),15)
        calDraw = ImageDraw.Draw(calImage)
        calDraw.text((20,20), calFormat, fill=(255,255,255))
        calImage.save('MonthCalandar.png'),
            
        Box2 = Box(app, grid=Calendar_Grid, visible = Calendar_Visible)
        #display_calendar = Text(Box2, text = calFormat, color="white", size="15")
        display_calendar = Picture(Box2, image="MonthCalandar.png")
    
def RestartAndShutdownTest():
    #Reboot Control
    if GPIO.input(12)==GPIO.HIGH:
        print("Reboot Initiated", flush=True)
        os.system("sudo reboot -h now")
    #Shutdown Control - Deciding on buttons to press
        #makes Sense to press reboot button and the LED button to Shutdown
    if GPIO.input(26)==GPIO.HIGH and GPIO.input(21)==GPIO.HIGH:
        print("Shutdown Initiated", flush=True)
        os.system("sudo shutdown -h now")

def ButtonTesting():
    #LED Controls
    global lastPressLED
    global lastPress2, lastPress3, lastPress4, lastPress5
    
    if GPIO.input(26)==GPIO.HIGH and lastPressLED ==0:
        lastPressLED = 1
        print("Button Pressed - LEDS ON", flush=True)
        GPIO.output(19, GPIO.HIGH)
        time.sleep(.5)

    if GPIO.input(26)==GPIO.HIGH and lastPressLED ==1:
        lastPressLED = 0
        print("Button Pressed - LEDS OFF", flush=True)
        GPIO.output(19, GPIO.LOW)
        time.sleep(.5)
        
    #Button 2    
    if GPIO.input(21)==GPIO.HIGH and lastPress2==0:
        lastPress2=1
        print("Button 2 Pressed- Monitor ON", flush=True)
        os.system("vcgencmd display_power 0")
        time.sleep(.5)
        
    if GPIO.input(21)==GPIO.HIGH and lastPress2==1:
        lastPress2=0
        print("Button 2 Pressed- Monitor OFF", flush=True)
        os.system("vcgencmd display_power 1")
        time.sleep(.5)
    
    #Button 3    
    if GPIO.input(20)==GPIO.HIGH and lastPress3==0:
        lastPress3=1
        print("Button 3 Pressed- Switch ON", flush=True)
        time.sleep(.5)
        
    if GPIO.input(20)==GPIO.HIGH and lastPress3==1:
        lastPress3=0
        print("Button 3 Pressed- Switch OFF", flush=True)
        time.sleep(.5)
    
    #Button 4    
    if GPIO.input(16)==GPIO.HIGH and lastPress4==0:
        lastPress4=1
        print("Button 4 Pressed- Switch ON", flush=True)
        time.sleep(.5)
        
    if GPIO.input(16)==GPIO.HIGH and lastPress4==1:
        lastPress4=0
        print("Button 4 Pressed- Switch OFF", flush=True)
        time.sleep(.5)
        
    #Button 5    
    if GPIO.input(12)==GPIO.HIGH and lastPress5==0:
        lastPress5=1
        print("Button 5 Pressed- Switch ON", flush=True)
        time.sleep(.5)
        
    if GPIO.input(12)==GPIO.HIGH and lastPress5==1:
        lastPress5=0
        print("Button 5 Pressed- Switch OFF", flush=True)
        time.sleep(.5)

#os.system('setterm -cursor off')
try:
    app = App(title="Mirror Mirror", width=1500, height=800, layout="grid", bg="black")

    #Black-Background Boxs- Will set all to Black525x425.png for final set. Use colors for debug
    B1 = Picture(app, image="Black525x425.png", grid=[0,0])
    B2 = Picture(app, image="Black525x425.png", grid=[0,1])
    B3 = Picture(app, image="Black525x425.png", grid=[0,2])
    B4 = Picture(app, image="Black525x425.png", grid=[0,3])
    B5 = Picture(app, image="Black525x425.png", grid=[1,0])

    #Time_Date_Greeting_Grid Section- WORKING!
    global Box1
    Box1 = Box(app,layout="grid", grid=Time_Date_Greeting_Grid, visible=Time_Date_Greeting_Visible)
    if(now.strftime("%H") == "03" or now.strftime("%H") == "04" or now.strftime("%H") == "05" or now.strftime("%H") == "06" or now.strftime("%H") == "07" or now.strftime("%H") == "08" or now.strftime("%H") == "09" or now.strftime("%H") == "10" or now.strftime("%H") == "11"):
        display_clock = Text(Box1, text = clock, grid=[0,0], color="white", size="35")
        display_date = Text(Box1, text = date, grid=[0,1], color="white", size="35")
        display_greeting = Text(Box1, text = "\nGood Morning, \n"+my_name, grid=[0,3], color="white", size="35")   

    elif(now.strftime("H") =="12" or now.strftime("%H") == "13" or now.strftime("%H") == "14" or now.strftime("%H") == "15" or now.strftime("%H") == "16" or now.strftime("%H") == "17"):
        display_clock = Text(Box1, text = clock, grid=[0,0], color="white", size="35")
        display_date = Text(Box1, text = date, grid=[0,1], color="white", size="35")
        display_greeting = Text(Box1, text = "\nGood Afternoon, \n"+my_name, grid=[0,3], color="white", size="35")

    else:
        display_clock = Text(Box1, text = clock, grid=[0,0], color="white", size="35")
        display_date = Text(Box1, text = date, grid=[0,1], color="white", size="35")
        display_greeting = Text(Box1, text = "\nGood Evening, \n"+my_name, grid=[0,3], color="white", size="35")

    #Calandar Section
    year = int(now.strftime("%Y"))
    month = int(now.strftime("%-m"))
    calFormat = cal.formatmonth(year,month,4,2)
    print(calFormat, flush=True)
    
    calImage = Image.new('RGB', (525,425), color = (0,0,0))
    #CalFont = ImageFont.truetype(ImageFont.load_default(),15)
    calDraw = ImageDraw.Draw(calImage)
    calDraw.text((20,20), calFormat, fill=(255,255,255))
    calImage.save('MonthCalandar.png'),
    
    Box2 = Box(app, grid=Calendar_Grid, visible = Calendar_Visible)
    #display_calendar = Text(Box2, text = calFormat, color="white", size="15")
    display_calendar = Picture(Box2, image="MonthCalandar.png")
    
    
    #Emails and Events
    Box3 = Box(app, grid = Email_Grid, visible = Emails_Visible)
    #for email in emails:
        #display_emails = Text(Box3, text = , grid=[0,0], color="white", size="20")
        
    Box4 = Box(app, grid = Events_Grid, visible = Events_Visible, align = "left")
    #display_events = Text(Box4, text = , grid=[0,0], color="white", size="20")

    Box5 = Box(app, layout="grid", grid=[1,1], visible=True)

    #Updating and Fxn Call Section
    app.repeat(100,RestartAndShutdownTest)
    app.repeat(100, ButtonTesting)
    app.repeat(500,update)
    #access_token =  "ya29.GltrBt6Z38EXSpkETvrn3GYZYbXbvJC6f9cJqJM54A__57zB1mI1I2cLvwockccCRnvyCCnq9X3grxJWCMu-BV4ObYdvJKPaEjVGszy_QtYSDOIc-YDHPoDXl1f_"
    #app.repeat(100000, google_update(access_token))
    #app.repeat(50000, read_settings)
    
    #sets full screen-Makes debug hard. To Get out: CTR+ALT+D
    app.tk.attributes("-fullscreen", True)
    q1 = "Test1"
    q2 = "Test2"
    q3 = "Test3"
    q4 = "Test4"
    q5 = "Test5"
    Text1 = Text(Box1, text=q1, grid=[1, 0], color="white", size="10", align="left")
    Text2 = Text(Box2, text=q2, grid=[1, 0], color="white", size="10", align="left")
    Text3 = Text(Box3, text=q3, grid=[1, 0], color="white", size="10", align="left")
    Text4 = Text(Box4, text=q4, grid=[1, 0], color="white", size="10", align="left")
    Text5 = Text(Box5, text=q5, grid=[1, 0], color="white", size="10", align="left")
    #nocursor is not working to turn cursor to be invisible.
    #will need to find something else to make it invisible or move position to side/corner
    def start_listening():

        def update_quads(bindings, quads):
            if quads[0]['ItemType'] != None:
                q1 = bindings.get(quads[0]['ItemType'])
                Text4.value = q1
                #print(bindings.get(quads[0]['ItemType']))
            if quads[1]['ItemType'] != None:
                q2 = bindings.get(quads[1]['ItemType'])
                Text2.value = q2
               # print(bindings.get(quads[1]['ItemType']))
            if quads[2]['ItemType'] != None:
                q3 = bindings.get(quads[2]['ItemType'])
                Text3.value = q3
               # print(bindings.get(quads[2]['ItemType']))
            if quads[3]['ItemType'] != None:
                q4 = bindings.get(quads[3]['ItemType'])
                Text4.value = q4
               # print(bindings.get(quads[3]['ItemType']))
            if quads[4]['ItemType'] != None:
                q5 = bindings.get(quads[4]['ItemType'])
                Text5.value = q5
               # print(bindings.get(quads[4]['ItemType']))

        def google_update(token):
            print(token)
            #global emails, events
            goog.configure(token)
            emails = goog.MessageList()
            events = goog.EventList()
            #Email Updating
            try:
                return (emails, events)
                #not working
                #display_emails= Text(Box3, text = emails[0]['summary'], grid=[0,0], color="white", size="20")
            except:
                print("error", flush = True)

        def msg_callback(body):
            lock = threading.Lock()
            lock.acquire()
            json_data = json.loads(body)
            quads = json_data["Cfg"]
            rss_feeds = json_data["RssFeeds"]
            weather_locs = json_data["WeatherLocations"]
            google_info = json_data["GoogleInfo"]
            feed_text = RssFeed(rss_feeds).get_entries()
            emails = ""
            events = ""
            if google_info != None:
                (emails, events) = google_update(google_info[0]["AccessToken"])
            bindings = {"RSS Feeds": feed_text}
            update_quads(bindings, quads)
            lock.release()
        msg = MessageParser(msg_callback)
        msg.start_listening()

    thread = threading.Thread(target=start_listening)
    thread.start()

        
    app.display()
except KeyboardInterrupt:
    quit()
    
