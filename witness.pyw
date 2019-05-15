import tkinter
from tkinter import ttk
import pyautogui
import time
import threading
import decimal
from decimal import Decimal
import os.path
import sys
#import graphics
#from graphics import *
#import win32gui

top = tkinter.Tk()
top.title("Witness 1.0")

if getattr(sys, 'frozen', False):
   application_path = sys._MEIPASS
elif __file__:
   application_path = os.path.dirname(__file__)

iconFile = 'witness.ico'

top.iconbitmap(default=os.path.join(application_path, iconFile))



#top.iconbitmap(r'witness.ico')
top.configure(background='Snow')

style = ttk.Style()
style.theme_use('clam')
style.configure('.', font=('Arial Black', 12))

isRecording = False

fileNameLabel = ttk.Label(top, text="File Name: ", background="Snow").grid(row=0)

fileNameEntry = ttk.Entry(top, font=('Arial Black', 12))
fileNameEntry.grid(row=0, column=1)
fileNameEntry.insert(0,"A_Custom_Name")

fileExtensionLabel = ttk.Label(top, text=".jpg", background="Snow").grid(row=0, column=2)

delayLabel = ttk.Label(top, text="Delay: ", background="Snow").grid(row=1)

delayEntry = ttk.Entry(top, font=('Arial Black', 12))
delayEntry.grid(row=1, column=1)
delayEntry.insert(0,"1")

delayUnitOfMeasureLabel = ttk.Label(top, text="second(s)", background="Snow").grid(row=1, column=2)

maxShotsLabel = ttk.Label(top, text="Max. # of Shots: ", background="Snow").grid(row=2, column=0)

maxShotsEntry = ttk.Entry(top, font=('Arial Black', 12))
maxShotsEntry.grid(row=2, column=1)
maxShotsEntry.insert(0,"1000")

counterStartLabel = ttk.Label(top, text="Counter init: ", background="Snow").grid(row=3, column=0)

counterStartEntry = ttk.Entry(top, font=('Arial Black', 12))
counterStartEntry.grid(row=3, column=1)
counterStartEntry.insert(0,"0")

recordingStatus = tkinter.StringVar()
recordingStatus.set("")

def canBeParsedAsInteger(inputValue):
    try: 
        int(inputValue)
        return True
    except ValueError:
        return False
		
def canBeParsedAsDecimal(inputValue):
    try: 
        Decimal(inputValue)
        return True
    except (ValueError, decimal.DecimalException, decimal.InvalidOperation):
        return False

def changerecordingStatus(isRecordingIn):
   global recordingStatus
   if isRecordingIn:
      recordingStatus.set("Recording in progress.")
   if not isRecordingIn:
      recordingStatus.set("")

def applyCountPadding(inCount, inMaxShots):
   countLength = len(str(inCount))
   maxShotsLength = len(str(inMaxShots))
   countPadding = ""
   if countLength<maxShotsLength:
      for i in range(maxShotsLength-countLength):
         countPadding+="0"
      return countPadding+str(inCount)		 
   else:
      return str(inCount)

def stopRecording():
   global isRecording   
   isRecording = False
   changerecordingStatus(isRecording)
   global counterStartEntry
   newInit = int(counterStartEntry.get()) + 1
   counterStartEntry.delete(0,tkinter.END)
   counterStartEntry.insert(0,newInit)

	  
def startRecording():
   def callback():
      global isRecording
      isRecording = True
      changerecordingStatus(isRecording)
      while isRecording:         
         global maxShotsEntry
         maxShots = maxShotsEntry.get()
         if not canBeParsedAsInteger(maxShots):
            maxShots = 1000
         elif int(maxShots)<1:
            maxShots = 1000
         else:
            maxShots = int(maxShots)		 
         global counterStartEntry
         count = counterStartEntry.get()
         if not canBeParsedAsInteger(count):
            count = 0
         elif int(count)<0:
            count = 0
         elif int(count)>maxShots:
            count = maxShots - 1
         else:
            count = int(count)
         if count<maxShots:
            count+=1
            #cursorPos = win32gui.GetCursorPos()
            #cursorImage = Circle(cursorPos, 25)
            #cursorImage.draw()
            pic = pyautogui.screenshot()
            global fileNameEntry
            global delayEntry
            directory = "You_should_enter_filename_next_time"
            filename = "You_should_enter_filename_next_time"
            if not (fileNameEntry.get()==""):
               filename = fileNameEntry.get()
               directory = fileNameEntry.get()
            delay = delayEntry.get()
            if canBeParsedAsDecimal(delay) or canBeParsedAsInteger(delay):
               if Decimal(delay)>=0:
                  delay = Decimal(delay)
               else:
                  delay = 1
            else:
               delay = 1
            if not os.path.exists(directory):
               os.makedirs(directory)
            completeFileNameWithPath = os.path.join(directory, filename+applyCountPadding(count, maxShots)+'.jpg')
            pic.save(completeFileNameWithPath, 'jpeg', optimize=True)
            counterStartEntry.delete(0,tkinter.END)
            counterStartEntry.insert(0,count)
            time.sleep(delay)
         if count==maxShots:
            stopRecording()
            break		 
   t = threading.Thread(target=callback)
   t.start()

startBtn = ttk.Button ( top, text="Start", command = startRecording )
startBtn.grid(row=4, column=0)

recordingrecordingStatusLabel = ttk.Label(top, textvariable=recordingStatus, background="Snow").grid(row=4, column=1)

stopBtn = ttk.Button ( top, text="Stop", command = stopRecording ).grid(row=4, column=2)

top.mainloop()