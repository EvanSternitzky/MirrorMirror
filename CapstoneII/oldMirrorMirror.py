#import tkinter
from guizero import *
import datetime
import calendar
#import asyncio
#import socket
import os
import sys
#import tkinter


#GPIO SETUP
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#LED Button and Output Pin - Button: GPIO26, Control: GPIO19
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(19, GPIO.OUT)
GPIO.output(19, GPIO.LOW)
global lastPressLED
lastPressLED =0

#UNSETUP BUTTONS - GPIO21, GPIO20, GPIO16
GPIO.setup(21,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(20,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(16,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Restart Button - GPIO12
GPIO.setup(12,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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


def RebootAndShutdownTest():
    #Restart Control
    if GPIO.input(12) == GPIO.HIGH:
        print("Reboot Initiated")
        os.system("sudo reboot -h now")
        
    #Shutdown Control - deciding on buttons to press
        #Makes sense to press the reboot button and the LED button to shutdown
    if GPIO.input(12) == GPIO.HIGH and GPIO.input(21)== HIGH:
        print("Shutdown Initiated")
        os.system("sudo shutdown -h now")

def LEDTest():
    #LED Controls
    global lastPressLED
    #print("IN LEDTESTING LOOP")
    if GPIO.input(26)==GPIO.HIGH and lastPressLED ==0:
        lastPressLED = 1
        print("Button Pressed - LEDS ON")
        GPIO.output(19, GPIO.HIGH)
        time.sleep(.5)

    if GPIO.input(26)==GPIO.HIGH and lastPressLED ==1:
        lastPressLED = 0
        print("Button Pressed - LEDS OFF")
        GPIO.output(19, GPIO.LOW)
        time.sleep(.5)

def update():
	now = datetime.datetime.now()
	display_clock.set(now.strftime("%I:%M %p"))
	display_date.set(now.strftime("%a %b-%d, %Y"))
        
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
        print(calFormat)
        Box2 = Box(app, grid=Calendar_Grid, visible = Calendar_Visible)
        display_calendar = Text(Box2, text = calFormat, color="white", size="35", align="left")

        app.repeat(100, LEDTest)
        app.repeat(100, RestartAndShutdownTest)
        app.repeat(500, update)
        
        #sets full screen-Makes debug hard. To Get out: CTR+ALT+D
        app.tk.attributes("-fullscreen", True)

        #nocursor is not working to turn cursor to be invisible.
        #will need to find something else to make it invisible or move position to side/corner

        app.display()

except KeyboardInterrupt:
	quit()

