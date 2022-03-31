import os
import sys
import math
import time
from datetime import datetime, timedelta, timezone
import pytz
from zeep import Client, xsd
from zeep.plugins import HistoryPlugin
from tkinter import *

from textcolours import *
from helper import *


###### TO DO
#
# - Platform blink (when platform number changes)
# - A better ticker scroll??



### Settings

settings = returnSettings('config.json')
numRows = 12
TickerSpeed = 8
Blink1Speed = 60
Blink2Speed = 200
Blink3Speed = 600
FadeSpeed = 20



### Main Variables

services = None
res = None
Initialise = True
NoServices = False
NoServicesToggle = False
Running = True
Reset = 0
ResetFadeCount = FadeSpeed
NoteStr = f''

ClockCount = 0
DataUpdateCount = 0
PauseCount = 0
FadeCount = 0
TickerTimeCount = 0
TickerCount = 0
TickerDone = False
cancelled = False
PlatformChange = False
PlatformETDblinkCount = 0
viaDestinationBlinkCount = 0
ThirdLineBlinkCount = 0

# Blink 1
PlatformETDblinkProgress = True
PlatformBlink = False
ETDBlink = False
otherETDBlink = False
trainhistory_platform = None

# Blink 2
DestinationBlinkProgress = True
viaToggle = False
otherviaToggle = False
trainDestination = f''
viaDestination = f''
othertrainDestination = f''
otherviaDestination = f''

# Blink 3
currentTrainThirdLine = 1

# Second line
SecondLineProgress = 0
callingPoints = f''
callingPointsOnly = f''
trainLength = f''
delayReason = f''
cancelReason = f''
franchiseName = f''
franchiseColour = colour.DEFAULT






### Source Setup
LDB_TOKEN = settings['apiKey']
WSDL = 'http://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2017-10-01'
if ((LDB_TOKEN == '') or (LDB_TOKEN == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")):
    raise Exception("Please configure your OpenLDBWS token in config.json")
history = HistoryPlugin()
client = Client(wsdl=WSDL, plugins=[history])
header = xsd.Element(
    '{http://thalesgroup.com/RTTI/2013-11-28/Token/types}AccessToken',
        xsd.ComplexType([
            xsd.Element(
                '{http://thalesgroup.com/RTTI/2013-11-28/Token/types}TokenValue',
                xsd.String()),
        ])
    )
header_value = header(TokenValue=LDB_TOKEN)







#### Set up Tkinter

root = Tk()
root.title('Departure Board')
root.geometry('540x95')
root.configure(bg='black')

firstFrame = Frame(root, bg='black', bd=0)  
firstFrame.pack( ipadx=0, ipady=1, pady=0, fill='both' )

secondFrame = Frame(root, bg='black', bd=0)  
secondFrame.pack( ipadx=0, ipady=0, pady=2, fill='x' )

thirdFrame = Frame(root, bg='black', bd=0)  
thirdFrame.pack( ipadx=0, ipady=0, pady=1, fill='x' )

fourthFrame = Frame(root, bg='black', bd=0)  
fourthFrame.pack( ipadx=0, ipady=0, pady=1, fill='x' )


### First Line Widgets

timeLabel = Label(
    firstFrame, text=f'', bg="black", fg=colour.DEFAULT, font=("pixelmix", 12), anchor="w", width=4
)
timeLabel.pack( ipadx=1, ipady=0, fill='x', side='left' )

platformLabel = Label(
    firstFrame, text=f'', bg="black", fg=colour.DEFAULT, font=("pixelmix", 12), width=3
)
platformLabel.pack( ipadx=1, ipady=0, fill='x', side='left' )

destinationLabel = Label(
    firstFrame, text=f'', bg="black", fg=colour.DEFAULT, font=("pixelmix bold", 12,), anchor="w"
)
destinationLabel.pack( ipadx=1, ipady=0, fill='x', side='left', expand=True )

ETDLabel = Label(
    firstFrame, text=f'', bg="black", fg=colour.GREEN, font=("pixelmix", 12), anchor="w"
)
ETDLabel.pack( ipadx=0, ipady=0, fill='x', side='right' )


### Second Line

text_width = 60
text = Text(secondFrame, width=text_width, height=1, bd=0, highlightfocus=0, bg='black', fg=colour.DEFAULT, font=("pixelmix", 12, "normal"))
text.pack()
text.tag_configure("center", justify='center')
text.tag_configure("left", justify='left')
text.bindtags((str(text), str(root), "all"))


### Third Line Widgets

thirdLinenumberLabel = Label(
    thirdFrame, text=f'', bg="black", fg=colour.DEFAULT, font=("pixelmix", 12), anchor="w"
)
thirdLinenumberLabel.pack( ipadx=1, ipady=0, fill='x', side='left' )

thirdLinetimeLabel = Label(
    thirdFrame, text=f'', bg="black", fg=colour.DEFAULT, font=("pixelmix", 12), anchor="w"
)
thirdLinetimeLabel.pack( ipadx=1, ipady=0, fill='x', side='left' )

thirdLineplatformLabel = Label(
    thirdFrame, text=f'', bg="black", fg=colour.DEFAULT, font=("pixelmix", 12), width=2
)
thirdLineplatformLabel.pack( ipadx=1, ipady=0, fill='x', side='left' )

thirdLinedestinationLabel = Label(
    thirdFrame, text=f'', bg="black", fg=colour.DEFAULT, font=("pixelmix", 12), anchor="w"
)
thirdLinedestinationLabel.pack( ipadx=1, ipady=0, fill='x', side='left', expand=True )

thirdLineETDLabel = Label(
    thirdFrame, text=f'', bg="black", fg=colour.GREEN, font=("pixelmix", 12), anchor="w"
)
thirdLineETDLabel.pack( ipadx=0, ipady=0, fill='x', side='right' )


fourthLineTimeLabel = Label(
    fourthFrame, text=f'', bg='black', fg=colour.DEFAULT, font=("pixelmix bold", 12)
)
fourthLineTimeLabel.pack( ipadx=0, ipady=0, fill='x', side='top' )

fourthLineUpdateLabel = Label(
    fourthFrame, text=f'.', bg="black", fg='black', font=("pixelmix bold", 12), anchor="e", width=1
)
fourthLineUpdateLabel.pack( ipadx=0, ipady=0, fill='x', side='right' )













### Functions

## Download Departure Board Info
def updateTrainData():
    global res
    global services
    global Reset
    global NoServices
    global NoServicesToggle
    global NoteStr
    NoteStr = f'                                   '
    try:
        res = client.service.GetDepBoardWithDetails(numRows=numRows, crs=settings['StationCode'], _soapheaders=[header_value])
    except:
        NoteStr = f"Cannot download services."
        if (len(settings['StationCode']) != 3):
            raise Exception("Cannot download services. Is the Station code in config.json correct?")
        else:
            raise Exception("Cannot download services.")
    try:   
        services = res.trainServices.service
        NoServicesToggle = False
        ## Remove first service if should have already departed
        if((len(services) > 1) and ((datetime.strptime(services[0].std, '%H:%M') + timedelta(seconds=35)) < (datetime.now(pytz.timezone('Europe/London')).replace(year=1900, month=1, day=1).replace(tzinfo=None)) ) and (services[0].etd == "On time")):
            NoteStr = f"First listed service removed."
            del services[0]
        ## Check if need to transition from No Services screen to main
        if (NoServices == True):
            NoServices = False

        ## Check if First Train has changed
        if ((NoServices == False) and (Initialise == False)):
            if (services[0].std != timeLabel.cget("text") or replaceStationName(services[0].destination.location[0].locationName) != trainDestination):
                NoteStr = f"First train has left."
                Reset = 1

        if(len(services) == 0):
            NoteStr = f"There are no services. (1)"
            NoServicesToggle = True
            Reset = 1
    except:
        if (NoServices == False):
            NoteStr = f"There are no services. (2)"
            NoServicesToggle = True
            Reset = 1






## Update Next Train Details & Labels
def updateFirstTrain():
    global cancelled
    global trainDestination
    global viaToggle
    global viaDestination
    global callingPoints
    global callingPointsOnly
    global trainLength
    global delayReason
    global cancelReason
    global franchiseName
    global franchiseColour
    global ETDBlink
    
    # Scheduled Time
    timeLabel.config(text=f'{services[0].std}')
    
    # Platform
    if (services[0].platform == None):
        platformLabel.config(text=f'')
    else:
        platformLabel.config(text=f'{services[0].platform}')
        
    # Destination
    trainDestination = services[0].destination.location[0].locationName
    trainDestination = replaceStationName(trainDestination)
    destinationLabel.config(text=f'{trainDestination}', font=("pixelmix bold", 12))
    
    # Via
    if (services[0].destination.location[0].via == None):
        viaToggle = False
        viaDestination = f''
    else:
        viaToggle = True
        viaDestination = f'{services[0].destination.location[0].via}'
    
    # Depature Time
    if (services[0].etd == "On time"):
        cancelled = False
        ETDBlink = False
        ETDLabel.config(text=f'On time', fg=colour.GREEN)
    elif (services[0].etd == "Delayed"):
        cancelled = False
        ETDBlink = True
        ETDLabel.config(text=f'Delayed', fg=colour.RED)
    elif (services[0].isCancelled == True or services[0].etd == "Cancelled"):
        cancelled = True
        ETDBlink = True
        ETDLabel.config(text=f'Cancelled', fg=colour.RED)
    else:
        cancelled = False
        ETDBlink = True
        ETDLabel.config(text=f'Exp {services[0].etd}', fg=colour.RED)

    # Calling Points
    callingPoints = f''
    callingPointsOnly = f''
    cancelledPointsMessage = f''
    for calPoint in services[0].subsequentCallingPoints.callingPointList[0].callingPoint:
        if (calPoint == services[0].subsequentCallingPoints.callingPointList[0].callingPoint[0]):
            pass
        elif (calPoint == services[0].subsequentCallingPoints.callingPointList[0].callingPoint[-1]):
            callingPoints = f'{callingPoints} and '
        else:
            callingPoints = f'{callingPoints}, '
        if (len(services[0].subsequentCallingPoints.callingPointList[0].callingPoint) == 1):
            callingPointsOnly = f' only'
        if (len(calPoint.et) > 5):
            if (calPoint.et == 'Cancelled'):
                cancelledPointsMessage = f' Some calling points on this service have been cancelled.'
                callingPoints = f'{callingPoints + calPoint.locationName} ({calPoint.et}){callingPointsOnly}'
            else:
                callingPoints = f'{callingPoints + calPoint.locationName} ({calPoint.st}){callingPointsOnly}'
        else:
            callingPoints = f'{callingPoints + calPoint.locationName} ({calPoint.et}){callingPointsOnly}'
    callingPoints = f'{" Calling at:  " + callingPoints + "." + cancelledPointsMessage + " " * text_width }'
    
    # Number of Cars
    if (services[0].length == None):
        trainLength = f''
    else:
        trainLength = f'{services[0].length}'
        
    # Train Franchise
    franchiseName, franchiseColour = franchiseIdent(services[0].operatorCode, services[0].operator)
    
    # Delay Reason
    delayReason = f''
    if (services[0].delayReason != None):
        delayReason = f' ' * text_width + services[0].delayReason + f'.' + f' ' * text_width 
    
    # Cancel Reason
    cancelReason = f''
    if (services[0].cancelReason != None):
        cancelReason = f' ' * text_width + services[0].cancelReason + f'.' + f' ' * text_width 






## Update Third Line Labels and info
def updateOtherTrains(trainnumber = 0):
    global othertrainDestination
    global otherviaToggle
    global otherviaDestination
    global otherETDBlink

    if(trainnumber >= 1):
        # Train Number
        if(trainnumber == 1):
            thirdLinenumberLabel.config(text=f'2nd')
        elif(trainnumber == 2):
            thirdLinenumberLabel.config(text=f'3rd')
        elif(trainnumber == 3):
            thirdLinenumberLabel.config(text=f'4th')
        elif(trainnumber == 4):
            thirdLinenumberLabel.config(text=f'5th')
        elif(trainnumber == 5):
            thirdLinenumberLabel.config(text=f'6th')
        elif(trainnumber == 6):
            thirdLinenumberLabel.config(text=f'7th')
        elif(trainnumber == 7):
            thirdLinenumberLabel.config(text=f'8th')
        elif(trainnumber == 8):
            thirdLinenumberLabel.config(text=f'9th')

        # Scheduled Time
        thirdLinetimeLabel.config(text=f'{services[trainnumber].std}')
        
        # Platform
        if (services[trainnumber].platform == None):
            thirdLineplatformLabel.config(text=f'')
        else:
            thirdLineplatformLabel.config(text=f'{services[trainnumber].platform}')
            
        # Destination
        othertrainDestination = services[trainnumber].destination.location[0].locationName
        othertrainDestination = replaceStationName(othertrainDestination)
        thirdLinedestinationLabel.config(text=f'{othertrainDestination}')
        
        # Via
        if (services[trainnumber].destination.location[0].via == None):
            otherviaToggle = False
            otherviaDestination = f''
        else:
            otherviaToggle = True
            otherviaDestination = f'{services[trainnumber].destination.location[0].via}'
        
        # Depature Time
        if (services[trainnumber].etd == "On time"):
            otherETDBlink = False
            thirdLineETDLabel.config(text=f'On time', fg=colour.GREEN)
        elif (services[trainnumber].etd == "Delayed"):
            otherETDBlink = True
            thirdLineETDLabel.config(text=f'Delayed', fg=colour.RED)
        elif (services[trainnumber].isCancelled == True or services[trainnumber].etd == "Cancelled"):
            otherETDBlink = True
            thirdLineETDLabel.config(text=f'Cancelled', fg=colour.RED)
        else:
            otherETDBlink = True
            thirdLineETDLabel.config(text=f'Exp {services[trainnumber].etd}', fg=colour.RED)

    # If 0, blank
    else:
        thirdLinenumberLabel.config(text=f'')
        thirdLinetimeLabel.config(text=f'')
        thirdLineplatformLabel.config(text=f'')
        thirdLinedestinationLabel.config(text=f'')
        otherviaToggle = False
        otherETDBlink = False
        thirdLineETDLabel.config(text=f'')



## Handle Tkinter window close
def close_window():
  global Running
  Running = False  # turn off while loop
  print("")


## Text Effects

from textcolours import *

def fade(k=0, kmax=20, colourfade=colour.DEFAULT, textfade=None):
    r_fade = int(math.floor((hex_to_rgb(colourfade)[0] / kmax) * k))
    g_fade = int(math.floor((hex_to_rgb(colourfade)[1] / kmax) * k))
    b_fade = int(math.floor((hex_to_rgb(colourfade)[2] / kmax) * k))
    fadeColour = '#%02x%02x%02x' % (r_fade, g_fade, b_fade)
    textfade.config(fg=fadeColour)

def fadeMain(k=0, kmax=20, othercolour=colour.DEFAULT):
    if (k <= 1):
        updateFirstTrain()
    r_fade_default = int(math.floor((hex_to_rgb(colour.DEFAULT)[0] / kmax) * k))
    g_fade_default = int(math.floor((hex_to_rgb(colour.DEFAULT)[1] / kmax) * k))
    b_fade_default = int(math.floor((hex_to_rgb(colour.DEFAULT)[2] / kmax) * k))
    r_fade_green = int(math.floor((hex_to_rgb(colour.GREEN)[0] / kmax) * k))
    g_fade_green = int(math.floor((hex_to_rgb(colour.GREEN)[1] / kmax) * k))
    b_fade_green = int(math.floor((hex_to_rgb(colour.GREEN)[2] / kmax) * k))
    r_fade_red = int(math.floor((hex_to_rgb(colour.RED)[0] / kmax) * k))
    g_fade_red = int(math.floor((hex_to_rgb(colour.RED)[1] / kmax) * k))
    b_fade_red = int(math.floor((hex_to_rgb(colour.RED)[2] / kmax) * k))
    r_fade_other = int(math.floor((hex_to_rgb(othercolour)[0] / kmax) * k))
    g_fade_other = int(math.floor((hex_to_rgb(othercolour)[1] / kmax) * k))
    b_fade_other = int(math.floor((hex_to_rgb(othercolour)[2] / kmax) * k))
    fadeColourDefault = '#%02x%02x%02x' % (r_fade_default, g_fade_default, b_fade_default)
    fadeColourGreen = '#%02x%02x%02x' % (r_fade_green, g_fade_green, b_fade_green)
    fadeColourRed = '#%02x%02x%02x' % (r_fade_red, g_fade_red, b_fade_red)
    fadeColourOther = '#%02x%02x%02x' % (r_fade_other, g_fade_other, b_fade_other)
    timeLabel.config(fg=fadeColourDefault)
    platformLabel.config(fg=fadeColourDefault)
    destinationLabel.config(fg=fadeColourDefault)
    if (ETDLabel.cget("text") == "On time"):
        ETDLabel.config(fg=fadeColourGreen)
    else:
        ETDLabel.config(fg=fadeColourRed)
    if (SecondLineProgress == 4):
        text.config(fg=fadeColourOther)
    else:
        text.config(fg=fadeColourDefault)
    if(len(services) > 1):
        thirdLinenumberLabel.config(fg=fadeColourDefault)
        thirdLinetimeLabel.config(fg=fadeColourDefault)
        thirdLineplatformLabel.config(fg=fadeColourDefault)
        thirdLinedestinationLabel.config(fg=fadeColourDefault)
        if (thirdLineETDLabel.cget("text") == "On time"):
            thirdLineETDLabel.config(fg=fadeColourGreen)
        else:
            thirdLineETDLabel.config(fg=fadeColourRed)

def fadeNoServices(k=0, kmax=20):
    if (k <= 1):
        #updateNoServices()
        text.delete('1.0', END)
        text.config(font=("pixelmix bold", 12))
        text.insert("1.0", f'{replaceStationName(res.locationName)}')
        text.tag_add("center", 1.0, "end")
    r_fade_default = int(math.floor((hex_to_rgb(colour.DEFAULT)[0] / kmax) * k))
    g_fade_default = int(math.floor((hex_to_rgb(colour.DEFAULT)[1] / kmax) * k))
    b_fade_default = int(math.floor((hex_to_rgb(colour.DEFAULT)[2] / kmax) * k))
    fadeColourDefault = '#%02x%02x%02x' % (r_fade_default, g_fade_default, b_fade_default)
    text.config(fg=fadeColourDefault)


def ticker(tickerCount=0, tickerText=f'', textcolour=colour.DEFAULT):
    global TickerDone
    global text_width
    if (tickerCount < len(tickerText)-text_width):
        text.config(fg=textcolour)
        text.delete('1.0', END)
        text.insert("1.1", tickerText[tickerCount:tickerCount+text_width])
    else:
        TickerDone = True


def blink1():
    if (PlatformBlink == True and PlatformETDblinkProgress == False):
        platformLabel.config(fg='black')
    else:
        platformLabel.config(fg=colour.DEFAULT)
    if (ETDBlink == True and PlatformETDblinkProgress == False):
        ETDLabel.config(fg='black')
    elif (ETDLabel.cget("text") == "On time"):
        ETDLabel.config(fg=colour.GREEN)
    else:
        ETDLabel.config(fg=colour.RED)
    if (otherETDBlink == True and PlatformETDblinkProgress == False):
        thirdLineETDLabel.config(fg='black')
    elif (thirdLineETDLabel.cget("text") == "On time"):
        thirdLineETDLabel.config(fg=colour.GREEN)
    else:
        thirdLineETDLabel.config(fg=colour.RED)

def blink2():
    if (viaToggle == True and DestinationBlinkProgress == False):
        destinationLabel.config(text=f'{viaDestination}', font=("pixelmix", 12, "normal"))
    else:
        destinationLabel.config(text=f'{trainDestination}', font=("pixelmix bold", 12))
    if (otherviaToggle == True and DestinationBlinkProgress == False):
        thirdLinedestinationLabel.config(text=f'{otherviaDestination}')
    else:
        thirdLinedestinationLabel.config(text=f'{othertrainDestination}')

def blink3():
    global currentTrainThirdLine
    global otherviaToggle
    global otherETDBlink
    if(len(services) > 1):
        # If only one other service or reached the 9th service, go back to first next.
        if((currentTrainThirdLine == len(services)-1) or (currentTrainThirdLine == 8)):
            currentTrainThirdLine = 1
        else:
            currentTrainThirdLine += 1
        # Set third line labels.
        updateOtherTrains(currentTrainThirdLine)
    else:
        thirdLinenumberLabel.config(text=f'')
        thirdLinetimeLabel.config(text=f'')
        thirdLineplatformLabel.config(text=f'')
        thirdLinedestinationLabel.config(text=f'')
        otherviaToggle = False
        otherETDBlink = False
        thirdLineETDLabel.config(text=f'')


## Tkinter Mouse Drag
def start_move(event):
    root.x = event.x
    root.y = event.y

def stop_move(event):
    root.x = None
    root.y = None

def do_move(event):
    deltax = event.x - root.x
    deltay = event.y - root.y
    x = root.winfo_x() + deltax
    y = root.winfo_y() + deltay
    root.geometry(f"+{x}+{y}")



















### Program Start
try:
    # Window borderless
    if (settings['BorderlessWindow'] == True):
        root.overrideredirect(True)
    
    # Window Transparency
    #root.attributes('-alpha', 0.3)
    
    # Drag Window with Mouse
    root.bind("<ButtonPress-1>", start_move)
    root.bind("<ButtonRelease-1>", stop_move)
    root.bind("<B1-Motion>", do_move)

    root.protocol("WM_DELETE_WINDOW", close_window)

    updateTrainData()

    # Debug
    if (settings['DebugOutput'] == True):
        print (f'Clock Data B1  B2  B3   Reset RFade  SL Tick Fade Pause')

    ### Main Loop
    while Running:

        # Print Diagnostics
        if (settings['DebugOutput'] == True):
            print (f'{ClockCount:5} {DataUpdateCount:4} {PlatformETDblinkCount:2} {viaDestinationBlinkCount:3} {ThirdLineBlinkCount:3}   {Reset:5} {ResetFadeCount:5}  {SecondLineProgress:2} {TickerCount:4} {FadeCount:4} {PauseCount:5}', end='\r')

        # Check if Running
        if not Running:
            break

        # Bring window to top
        if (settings['WindowAlwaysOnTop']):
            root.attributes('-topmost', 'true')

        # Graphical Update
        root.update()
        time.sleep(0.01)

        # Check if Running again
        if not Running:
            break

        # Increment Global Counts
        ClockCount += 1
        DataUpdateCount += 1


        # Update Clock
        if (ClockCount >= 10):
            ClockCount = 0
            fourthLineTimeLabel.config(text=datetime.now(pytz.timezone('Europe/London')).strftime("%H:%M:%S"))
            pass

        # Update train data every 500 loops (~5 seconds)
        if (DataUpdateCount >= 500):
            fourthLineUpdateLabel.config(fg=colour.DEFAULT)
            updateTrainData()
            DataUpdateCount = 0
        else:
            fourthLineUpdateLabel.config(fg='black')

        # Initialise
        if(Initialise == True):
            # Fade in all AND timer
            # First, check what to fade in to (if main screen or no services screen)
            if (FadeCount < FadeSpeed):
                FadeCount += 1
                if (NoServicesToggle == True):
                    fadeNoServices(FadeCount, FadeSpeed)
                else:
                    if (FadeCount == 1):
                        updateFirstTrain()
                        updateOtherTrains(1)
                    fadeMain(FadeCount, FadeSpeed)
                fade(FadeCount, FadeSpeed, colour.DEFAULT, fourthLineTimeLabel)
            else:
                FadeCount = 0
                Initialise = False
                if (NoServicesToggle == True):
                    NoServices = True
                    Reset = 0

        # Reset functions
        elif (Reset > 0):
            # This is for transitioning from main screen to no services screen and vice versa,
            #    including when first train changes.

            # Fade out all except clock
            if (Reset == 1):
                if (ResetFadeCount < FadeSpeed*2):
                    ResetFadeCount += 1
                    if (NoServices == True):
                        fadeNoServices(-ResetFadeCount+(FadeSpeed*2), FadeSpeed)
                    if (NoServices == False):
                        fadeMain(-ResetFadeCount+(FadeSpeed*2), FadeSpeed)
                        if (SecondLineProgress == 3):
                            fade(-ResetFadeCount+(FadeSpeed*2), FadeSpeed, franchiseColour, text)
                        else:
                            fade(-ResetFadeCount+(FadeSpeed*2), FadeSpeed, colour.DEFAULT, text)
                else:
                    if (NoServicesToggle == True):
                        NoServices = True
                    Reset = 2
                    ResetFadeCount = 0

            # Update labels, reset second line count, etc
            elif (Reset == 2):
                timeLabel.config(text=f'')
                platformLabel.config(text=f'')
                destinationLabel.config(text=f'', anchor="w")
                ETDLabel.config(text=f'')
                text.delete('1.0', END)
                thirdLinenumberLabel.config(text=f'')
                thirdLinetimeLabel.config(text=f'')
                thirdLineplatformLabel.config(text=f'')
                thirdLinedestinationLabel.config(text=f'')
                thirdLineETDLabel.config(text=f'')
                DataUpdateCount = 0
                PauseCount = 0
                FadeCount = 0
                TickerCount = 0
                TickerDone = False
                TickerTimeCount = 0
                cancelled = False
                trainhistory_platform = None
                PlatformChange = False
                PlatformETDblinkCount = 0
                viaDestinationBlinkCount = 0
                ThirdLineBlinkCount = 0
                PlatformETDblinkProgress = True
                PlatformBlink = False
                ETDBlink = False
                otherETDBlink = False
                trainhistory_platform = None
                DestinationBlinkProgress = True
                viaToggle = False
                otherviaToggle = False
                trainDestination = f''
                viaDestination = f''
                othertrainDestination = f''
                otherviaDestination = f''
                currentTrainThirdLine = 1
                SecondLineProgress = 0
                Reset = 3

            # Fade in all
            elif (Reset == 3):
                if (ResetFadeCount < FadeSpeed):
                    ResetFadeCount += 1
                    if (NoServices == True):
                        fadeNoServices(ResetFadeCount, FadeSpeed)
                    if (NoServices == False):
                        if (ResetFadeCount == 1):
                            updateFirstTrain()
                            updateOtherTrains(1)
                            text.delete('1.0', END)
                        fadeMain(ResetFadeCount, FadeSpeed)
                else:
                    Reset = 0
                    ResetFadeCount = FadeSpeed

        # If No Services
        elif (NoServices == True):
            # Don't currently need anything here, only to stop next.
            pass

        # Process normal screen
        else:
            # Blink 1
            PlatformETDblinkCount += 1
            if (PlatformETDblinkCount == Blink1Speed):
                PlatformETDblinkCount = 0
                PlatformETDblinkProgress = not PlatformETDblinkProgress
                blink1()

            # Blink 2
            viaDestinationBlinkCount += 1
            if (viaDestinationBlinkCount == Blink2Speed):
                viaDestinationBlinkCount = 0
                DestinationBlinkProgress = not DestinationBlinkProgress
                blink2()

            # Blink 3
            ThirdLineBlinkCount += 1
            if (ThirdLineBlinkCount == Blink3Speed):
                ThirdLineBlinkCount = 0
                blink3()

            # Second Line: Cancelled or Calling Points
            if (SecondLineProgress == 0):
                # If cancelled, show reason
                if (cancelled == True):
                    text.config(fg=colour.DEFAULT)
                    TickerTimeCount += 1
                    if (TickerTimeCount == TickerSpeed):
                        TickerTimeCount = 0
                        TickerCount += 1
                        ticker(TickerCount, cancelReason, colour.DEFAULT)
                        if (TickerDone == True):
                            text.delete('1.0', END)
                            TickerDone = False
                            TickerCount = 0
                            SecondLineProgress = 3
                # Otherwise, show calling points
                else:
                    if (FadeCount < FadeSpeed):
                        if (FadeCount == 0):
                            text.config(fg='black', font=("pixelmix", 12, "normal"))
                            text.tag_add("left", 1.0, "end")
                            text.delete('1.0', END)
                            text.insert("1.1", callingPoints[0:0+text_width])
                        FadeCount += 1
                        fade(FadeCount, FadeSpeed, colour.DEFAULT, text)
                    elif (PauseCount < 50):
                        PauseCount += 1
                    else:
                        TickerTimeCount += 1
                        if (TickerTimeCount == TickerSpeed):
                            TickerTimeCount = 0
                            TickerCount += 1
                            ticker(TickerCount, callingPoints, colour.DEFAULT)
                            if (TickerDone == True):
                                text.delete('1.0', END)
                                FadeCount = 0
                                TickerDone = False
                                TickerCount = 0
                                SecondLineProgress = 1

            # Second Line: Number of Coaches
            elif (SecondLineProgress == 1):
                if (len(trainLength) > 0):
                    if (FadeCount < FadeSpeed):
                        if (FadeCount == 0):
                            text.delete('1.0', END)
                            if (trainLength == '1'):
                                text.insert("1.1", f'This train has {trainLength} coach.')
                            else:
                                text.insert("1.1", f'This train has {trainLength} coaches.')
                            text.tag_add("center", 1.0, "end")
                        FadeCount += 1
                        fade(FadeCount, FadeSpeed, colour.DEFAULT, text)
                    elif (PauseCount < 180):
                        PauseCount += 1
                    elif (FadeCount < FadeSpeed*2):
                        FadeCount += 1
                        fade(-FadeCount+(FadeSpeed*2), FadeSpeed, colour.DEFAULT, text)
                    else:
                        text.delete('1.0', END)
                        PauseCount = 0
                        FadeCount = 0
                        SecondLineProgress = 2
                else:
                    PauseCount = 0
                    FadeCount = 0
                    SecondLineProgress = 2

            # Second Line: Delayed Reason
            elif (SecondLineProgress == 2):
                if ((len(delayReason) > 0) and (ETDBlink == True)):
                    TickerTimeCount += 1
                    if (TickerTimeCount >= TickerSpeed):
                        TickerTimeCount = 0
                        TickerCount += 1
                        ticker(TickerCount, delayReason, colour.DEFAULT)
                        if (TickerDone == True):
                            TickerDone = False
                            TickerCount = 0
                            SecondLineProgress = 3
                else:
                    TickerDone = False
                    TickerCount = 0
                    text.delete('1.0', END)
                    SecondLineProgress = 3

            # Second Line: Operator
            elif (SecondLineProgress == 3):
                if (len(franchiseName) > 0):
                    if (FadeCount < FadeSpeed):
                        if (FadeCount == 0):
                            text.delete('1.0', END)
                            text.insert("1.1", franchiseName)
                            text.config(fg='black')
                            text.tag_add("center", 1.0, "end")
                        FadeCount += 1
                        fade(FadeCount, FadeSpeed, franchiseColour, text)
                    elif (PauseCount < 180):
                        PauseCount += 1
                    elif (FadeCount < FadeSpeed*2):
                        FadeCount += 1
                        fade(-FadeCount+(FadeSpeed*2), FadeSpeed, franchiseColour, text)
                    else:
                        text.delete('1.0', END)
                        PauseCount = 0
                        FadeCount = 0
                        SecondLineProgress = 0
                else:
                    PauseCount = 0
                    FadeCount = 0
                    SecondLineProgress = 0

            # End of Second Line operations, back to start
            else:
                SecondLineProgress = 0

except KeyboardInterrupt:
    print(f'KeyboardInterrupt')
except ValueError as error:
    print(f'ERROR: {error}')
except IndexError as error:
    print:(f'ERROR: Index error.')
except Exception as exc:
    print(f'ERROR: Unexpected exception.')
    print(f'{exc}')


