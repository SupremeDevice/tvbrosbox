#!/usr/bin/python3
import RPi.GPIO as GPIO
import os
import random
import time
from subprocess import PIPE, Popen, STDOUT, check_output, CalledProcessError
from datetime import datetime
from omxplayer.player import OMXPlayer
from os.path import exists
import threading
from threading import Thread
GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
initDone = False
isLCD = True
directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'videos')

directorySimpsons = os.path.join(directory, 'Simpsons')
myThread = None
videos = []
player = None
isScreenOn = True
isMute = False
isWide = False #if false and not letterbox = zoom
isSimpsons = False
isCommentary = False
isLetterBox = True
curIndex = -1 #index of video being played for 
screenChanged = False #if screen mode changed
stopPlayer = False
mountPaths = ['/mnt/usb1','/mnt/usb2','/mnt/usb3','/mnt/usb4','/mnt/usb5','/mnt/usb6','/mnt/usb7','/mnt/usb8']

def getVideos():
	global directory
	global directorySimpsons
	global videos
	global isSimpsons
	#print("getVideos simpsons", isSimpsons)
	videos = []
	global mountPaths
	dirPath = directory
	if isSimpsons:
		dirPath = directorySimpsons
	#print("dirPath is ", dirPath)
	for currentpath, folders, files in os.walk(dirPath):
		for file in files:
			if os.path.join(currentpath, file).lower().endswith('.mp4'):
				videos.append(os.path.join(currentpath, file))
			elif os.path.join(currentpath, file).lower().endswith('.mkv'):
				videos.append(os.path.join(currentpath, file))
	if not isSimpsons:
		for i in mountPaths:
			dirPath = os.path.join(i, "")
			dirPath = os.path.join(dirPath, 'videos')
	
			#print("alternate i ", dirPath)

	
			for currentpath, folders, files in os.walk(dirPath):
				for file in files:
					if os.path.join(currentpath, file).lower().endswith('.mp4'):
						videos.append(os.path.join(currentpath, file))
					elif os.path.join(currentpath, file).lower().endswith('.mkv'):
						videos.append(os.path.join(currentpath, file))

def endWait(length):
	global stopPlayer
	forced = False
	timeLeft = int(length)
	origTimeLeft = 0
	firstT = datetime.now()
	lastT = datetime.now()
	delta = lastT - firstT
	stopped = False
	global myThread
	while delta.seconds < timeLeft and forced == False:
		time.sleep(1)
		lastT = datetime.now()
		delta = lastT - firstT
		tempCmd = 'sudo ps -aux| grep omxplayer.bin'
		#check if omxplayer is still running
		try:
			value = check_output(tempCmd, shell=True)
		except CalledProcessError as e:
			value = ""
		if not value:
			origTimeLeft = timeLeft
			#print("Error occurred")
			forced = True
		else:
			if len(value) < 10:
				origTimeLeft = timeLeft
				forced = True
		if stopPlayer:
			#print("stopPlayer detected")
			forced = True
#		if not myThread.is_alive():
#			myThread = threading.Thread(target=buttonWatcher)
#			myThread.start()


def playVideos():
	global videos
	global curIndex
	global stopPlayer
	global isWide
	global isLetterbox
	global isCommentary
	global isSimpsons
	curIndex = 0
	vLength = 0
	global player
	if len(videos) == 0:
		getVideos()
		time.sleep(5)
		return
	random.shuffle(videos)
	length = len(videos)
	while curIndex < len(videos):
		video = videos[curIndex]
		#print("video is ", video)
		#print("stopPlayer is ", stopPlayer)
		tempCmd = 'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "%s"' % video
		value =  check_output(tempCmd, shell=True)
		vLength = int(float(value))
		if isLetterBox:
			player = OMXPlayer(video,args='--no-osd --aspect-mode Letterbox')
		elif isWide:
			player = OMXPlayer(video,args='--no-osd --aspect-mode stretch')
		else: #zoom
			player = OMXPlayer(video,args='--no-osd --aspect-mode fill')
		if isSimpsons and isCommentary:
			player.set_volume(2.5)
			player.select_audio(2)

		else:
			player.set_volume(1.25)

		endWait(vLength - 6)
		curIndex += 1
		if stopPlayer:
			stopPlayer = False
			if player is not None:
				player.quit()
				player = None
			#curIndex = len(videos) + 1
			if length != len(videos): #changed mode
				curIndex = 0
			
def setup():
	devPaths = ['/dev/sda','/dev/sdb','/dev/sdc','/dev/sdd','/dev/sda1','/dev/sdb1','/dev/sdc1','/dev/sdd1',]
	j = 0
	for i in mountPaths:
		#Mount the stuff
		mountProcess = Popen(['mount', '-r', devPaths[j], i])
		mountProcess.wait()
		j = j + 1
	myThread = threading.Thread(target=buttonWatcher)
	myThread.start()

def buttonWatcher():
	global initDone
	global isWide
	global isMute
	global isLetterBox
	global Issimpsons
	global isCommentary
	global isScreenOn	
	global stopPlayer
	initDone = False
	stopPlayer = False
	isSimpsons = GPIO.input(22)
	isCommentary = GPIO.input(16)

	isLetterBox = GPIO.input(17)
	isWide = GPIO.input(27) # Wide = Stretched
	isMute = not GPIO.input(26)
	isScreenOn = GPIO.input(18)
	input = False
	initDone = True
	while(True):
		checkSimpsons()
		checkCommentary()
		checkLetterBox()
		checkWide(False)
		checkMute()
		checkScreenOn()
		if not stopPlayer:
			checkNext()
		time.sleep(0.2)

def checkSimpsons():
	global isSimpsons
	global stopPlayer
	global initDone
	input =  GPIO.input(22)

	if input != isSimpsons:
		isSimpsons = input
		if initDone:
			#print("isSimpsons changed to ", isSimpsons)
			getVideos()  
			stopPlayer = True

def checkCommentary():
	global isCommentary
	global player
	global isSimpsons
	global initDone
	input = GPIO.input(16)
	#print("Commentary is ",isSimpsons, input)

	#print("isSimpsons is ",isSimpsons)

	if isSimpsons or initDone == False:
		if input != isCommentary or initDone == False:
			#print("Commentary is ",input)
			isCommentary = input
			if initDone:
				if player is not None:
					if input:
						player.select_audio(2)
						player.set_volume(2.5)
					else:
						player.select_audio(0)
						player.set_volume(1.25)


def checkLetterBox():
	global isLetterBox
	global player
	input = GPIO.input(17)
	if input != isLetterBox:
		isLetterBox = input
		#print("is isLetterBox ", isLetterBox, player)
		if player is not None:
			if input:
				#print("Set to letterbox")
				player.set_aspect_mode('letterbox')
			#else should be handled by 4de
			else:
				checkWide(True)

def checkWide(isForced):
	global isWide
	global isLetterBox
	global player
	input = GPIO.input(27) # Wide = Stretched
	if (isWide != input and isLetterBox == False) or isForced == True:
		print("isWide is now ", isWide)
		isWide = input
		if player is not None:
			if input:
				player.set_aspect_mode('stretch')
			else:
				player.set_aspect_mode('fill')

def checkMute():
	global isMute
	input = not GPIO.input(26)
	if (input != isMute):
		isMute = input
		if input:
			os.system('raspi-gpio set 19 ip')			
		else:
			os.system('raspi-gpio set 19 op a5')

def turnOnScreen():
	#Add code to check hdmi screen
	global isLCD
	if isLCD:
		os.system('tvservice -e "CEA 4 HDMI"')
	else:
		os.system('tvservice -p')

	input = not GPIO.input(26) #unmute
	if input:
		os.system('raspi-gpio set 19 ip')			
	else:
		os.system('raspi-gpio set 19 op a5')
	
def ReadOnly(val):
	cmd = ''
	if val:
		cmd = 'sudo mount -o remount,ro / ; sudo mount -o remount,ro /boot'
	else:
		cmd = 'sudo mount -o remount,rw / ; sudo mount -o remount,rw /boot'
	os.system(cmd)
	

def checkScreenOn():
	global isScreenOn	
	global initDone
	global isLCD
	isLCD = True
	shouldRestart = False
	if initDone == False:
		tempCmd = 'tvservice -n | grep DWE-HDMI'
		#check if built-in LCD is only used
		try:
			value = check_output(tempCmd, shell=True)
		except CalledProcessError as e:
			value = ""
		if not value:
			isLCD = False
		else:
			if len(value) < 5:
				isLCD = False
		print("isLCD is ", isLCD)
		hdmiFileExists = exists('/boot/hdmiFlag')
		ReadOnly(False)

		if not isLCD:
			if hdmiFileExists:
				Print("External is connected and file is present")
			else:
				os.system('sudo touch /boot/hdmiFlag')
				os.system('sudo cp -f /boot/hdmi/config.txt /boot/config.txt')
				shouldRestart = True
		else:
			if hdmiFileExists:
				os.system('sudo rm /boot/hdmiFlag')
				os.system('sudo cp -f /boot/lcd/config.txt /boot/config.txt')
				shouldRestart = True
			else:
				print("LCD is connected and no need to delete file")
		ReadOnly(True)
	input = GPIO.input(18)
	if initDone == False or input != isScreenOn:
		isScreenOn = input
		if input:
			turnOnScreen()
		else:
			os.system('raspi-gpio set 19 ip')			
			os.system('tvservice -o')

def checkNext():
	global stopPlayer
	global initDone
	input = not GPIO.input(6)
	
	if input and initDone:
		stopPlayer = True	

checkScreenOn()
setup()
while (True):
	playVideos()