#!/usr/bin/python3
from multiprocessing import Process, Lock
import RPi.GPIO as GPIO
import os
import secrets
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
firstT = None
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
initDone = False
volumeScale = 1.0
curVolume = 0
GPIO.setup(12, GPIO.IN)
remotePin = 12 #pin32 
channelChanged = False
isLCD = True
directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'videos')
origTimeLeft = 0
directorySimpsons = os.path.join(directory, 'Simpsons')
videos = []
remoteOverride = False
remoteAspectOverride = False
remoteChannel = -1
channelIndex = -1 # current channel

allVideos = [] # 0
directorySimpsonsPath = "videos/Simpsons"
directoryZombiePath = "videos2/Zombie"
ZombieVideos = [] # 1
altChannel = False
SimpsonsVideos = [] # 1
directoryDariaPath = "videos/Daria"
DariaVideos = [] # 2 Daria
directoryAngelPath = "videos/Galaxy Angel"
AngelVideos = [] # 2 Galaxy Angel

directoryMomPath = "videos/Mom"

directoryMoonPath = "videos/Sailor Moon"
directoryRockPath = "videos/30 Rock"

MomVideos = [] # 2 Mom
MoonVideos = [] # 4 Mom

RockVideos = [] # 3 30 Rock

directoryGoldenPath = "videos/Golden Girls"
GoldenVideos = [] # 3 Golden Girls
directoryBarnyardPath = "videos/Back at the Barnyard"
BarnyardVideos = [] #4 Back at the Barnyard
directoryNannyPath = "videos/The Nanny"
NannyVideos = [] #5 The Nanny
directoryTotallyPath = "videos/Totally Spies!"
TotallyVideos = [] #6 Totally Spies
directoryRockoPath = "videos/Rocko's Modern Life"
RockoVideos = [] #7 Rocko
directoryGarfieldPath = "videos/Garfield and Friends"
directoryGarfieldPath2 = "videos/Garfield Specials"
GarfieldVideos = [] #8 Garfield and Friends
directoryRavenPath = "videos/That's So Raven"
RavenVideos = [] #9 Thats So Raven

directoryLooneyPath = "videos/Looney Tunes"
directoryXmenEPath = "videos/X-men Evolution"
XmenEVideos = []
LooneyVideos = []

DariaIndex = -1
AngelIndex = -1

MomIndex = -1
MoonIndex = -1
RockIndex = -1

GoldenIndex = -1
BarnyardIndex = -1
NannyIndex = -1
TotallyIndex = -1
RockoIndex = -1
GarfieldIndex = -1
RavenIndex = -1
SimpsonsIndex = -1
LooneyIndex = -1
XmenEIndex = -1

curFile = ""
player = None
isScreenOn = True
isMute = False
isMuteB = False

isWide = False #if false and not letterbox = zoom
isSimpsons = False
isCommentary = False
isLetterBox = True
timeLeft = 0
nextHeldCnt = 0

specialHeldCnt = 0
curIndex = -1 #index of video being played for 
screenChanged = False #if screen mode changed
stopPlayer = False

pausePlayer = False
ButtonsNames = ["UP","DOWN","LEFT","RIGHT","Vol+","Vol-","CH+","CH-","CHANNEL0","CHANNEL1","CHANNEL2","CHANNEL3","CHANNEL4","CHANNEL5","CHANNEL6","CHANNEL7","CHANNEL8","CHANNEL9","Digits","Last","PREVIOUS", "NEXT", "BACK15", "FORWARD15","Red","Green","Yellow","Blue", "PLAY","UP","DOWN","CH+","CH-","CHANNEL0","CHANNEL1","CHANNEL2","CHANNEL3","CHANNEL4","CHANNEL5","CHANNEL6","CHANNEL7","CHANNEL8","CHANNEL9","BACK15","FORWARD15","Red","Green","PLAY","PREVIOUS","NEXT"]
Buttons = [0x300fdc837,0x300fd28d7,0x300fd8877,0x300fd48b7,0x300fd12ed,0x300fd926d,0x300fd52ad,0x300fdd22d,0x300fd30cf,0x300fd40bf,0x300fdc03f,0x300fd20df,0x300fda05f,0x300fd609f,0x300fde01f,0x300fd10ef,0x300fd906f,0x300fd50af,0x300fdd02f,0x300fdb04f,0x300fd2ad5,0x300fdaa55,0x300fd6a95,0x300fdea15,0x300fd32cd,0x300fdb24d,0x300fd728d,0x300fdf20d, 0x300fd8a75,0x300ffa857,0x300ffe01f,0x300ffe21d,0x300ffa25d,0x300ff6897,0x300ff30cf,0x300ff18e7,0x300ff7a85,0x300ff10ef,0x300ff38c7,0x300ff5aa5,0x300ff42bd,0x300ff4ab5,0x300ff52ad,0x300ff9867,0x300ffb04f,0x300ff629d,0x300ff906f,0x300ffc23d,0x300ff22dd,0x300ff02fd]

mountPaths = ['/mnt/usb1','/mnt/usb2','/mnt/usb3','/mnt/usb4','/mnt/usb5','/mnt/usb6','/mnt/usb7','/mnt/usb8']
listPrograms = None
adjustedTime = 0
overlapTime = 0
isSpecialDown = False
isDualScreen = False
mutex = Lock()
def getVideos():
	global directory
	global directorySimpsons
	global videos
	global allVideos
	global SimpsonsVideos
	global isSimpsons
	global listPrograms
	global remoteOverride
	global remoteChannel
	global channelIndex

	global DariaVideos
	global AngelVideos

	global MomVideos
	global MoonVideos
	global RockVideos

	global GoldenVideos
	global BarnyardVideos
	global NannyVideos
	global TotallyVideos
	global RockoVideos
	global GarfieldVideos
	global RavenVideos
	global DariaIndex
	global AngelIndex
	global MomIndex
	global MoonIndex
	global RockIndex

	global GoldenIndex
	global BarnyardIndex
	global NannyIndex
	global TotallyIndex
	global RockoIndex
	global GarfieldIndex
	global RavenIndex
	global SimpsonsIndex
	global XmenEIndex
	global XmenEVideos
	global LooneyIndex
	global LooneyVideos
	global altChannel
	global ZombieVideos
	videos = []
	global mountPaths
	dirPath = directory
	initProgramList = False
	if listPrograms is None:
		initProgramList = True
		listPrograms = []
	videos = allVideos
	if (isSimpsons and remoteOverride == False):
		videos = SimpsonsVideos
		channelIndex = SimpsonsIndex
		random.shuffle(SimpsonsVideos)
	elif remoteOverride and remoteChannel != -1:
		if remoteChannel == 0:
			random.shuffle(allVideos)
			videos = allVideos
			channelIndex = -1			
		elif remoteChannel == 1:
			if not altChannel:
				videos = SimpsonsVideos
				random.shuffle(SimpsonsVideos)
			else:
				videos = ZombieVideos
				random.shuffle(ZombieVideos)
			channelIndex = SimpsonsIndex
		elif remoteChannel == 2:
			if not altChannel:
				videos = DariaVideos
				channelIndex = DariaIndex
				random.shuffle(DariaVideos)
			else:
				videos = MomVideos
				channelIndex = MomIndex
				random.shuffle(MomVideos)

		elif remoteChannel == 3:
			if not altChannel:
				videos = GoldenVideos
				channelIndex = GoldenIndex
				random.shuffle(GoldenVideos)
			else:
				videos = RockVideos
				channelIndex = RockIndex
				random.shuffle(RockVideos)

		elif remoteChannel == 4:
			if not altChannel:
				videos = BarnyardVideos
				channelIndex = BarnyardIndex

			else:
				videos = MoonVideos
				channelIndex = MoonIndex
			random.shuffle(BarnyardVideos)
			random.shuffle(MoonVideos)
		elif remoteChannel == 5:
			if not altChannel:
				videos = NannyVideos
				channelIndex = NannyIndex
			else:
				videos = AngelVideos
				channelIndex = AngelIndex

			random.shuffle(NannyVideos)

		elif remoteChannel == 6:
			videos = TotallyVideos
			channelIndex = TotallyIndex
			random.shuffle(TotallyVideos)

		elif remoteChannel == 7:
			videos = RockoVideos
			channelIndex = RockoIndex
			random.shuffle(RockoVideos)
		elif remoteChannel == 8:
			videos = GarfieldVideos
			channelIndex = GarfieldIndex
			random.shuffle(GarfieldVideos)
		elif remoteChannel == 9:
			videos = RavenVideos
			channelIndex = RavenIndex
			random.shuffle(RavenVideos)

		elif remoteChannel == 10:
			videos = XmenEVideos
			channelIndex = XmenEIndex
			random.shuffle(XmenEVideos)

		else:
			videos = LooneyVideos
			channelIndex = LooneyIndex
			random.shuffle(LooneyVideos)

	elif remoteChannel == -1 and remoteOverride:
		print("Channel change to " + str(channelIndex) + " " + listPrograms[channelIndex])
		videos = []
		for i in allVideos:
			if i.find(listPrograms[channelIndex]) != -1:
				videos.append(i)	
		print("len = " + str(len(videos)))

def outputList():
	global videos
	f = open("/tmp/curList", 'w')
	#tempCmd = "echo > /tmp/curList"
	#os.system(tempCmd)			
	j = 0
	for i in videos:
		#tempCmd = "echo " + str(j) + ": " + i + " >> /tmp/curList"
		#os.system(tempCmd)			
		f.writelines(str(j) + ": " + i +'\n')
		j = j + 1
	f.close()
def initVideoList():
	global directory
	global directorySimpsons
	global allVideos
	global SimpsonsVideos
	global listPrograms
	global directorySimpsonsPath

	global directoryAngelPath
	global directoryDariaPath
	global directoryMomPath
	global directoryMoonPath
	global directoryRockPath

	global DariaVideos
	global AngelVideos
	global MomVideos
	global MoonVideos
	global RockVideos

	global directoryGoldenPath
	global GoldenVideos
	global directoryBarnyardPath
	global BarnyardVideos
	global directoryNannyPath
	global NannyVideos
	global directoryTotallyPath
	global TotallyVideos
	global directoryRockoPath
	global RockoVideos
	global directoryGarfieldPath
	global directoryGarfieldPath2
	global GarfieldVideos
	global directoryRavenPath
	global RavenVideos

	global directoryXmenEPath
	global XmenEVideos

	global directoryLooneyPath
	global LooneyVideos
	global DariaIndex
	global AngelIndex
	global MomIndex
	global MoonIndex
	global RockIndex

	global GoldenIndex
	global BarnyardIndex
	global NannyIndex
	global TotallyIndex
	global RockoIndex
	global GarfieldIndex
	global RavenIndex
	global SimpsonsIndex

	global XmenEIndex
	global LooneyIndex
	allVideos = []
	SimpsonsVideos = []
	global mountPaths
	dirPath = directory
	listPrograms = []

	chopped = ""
	for currentpath, folders, files in os.walk(dirPath):
		chopped = currentpath[len(dirPath) - 6:len(currentpath)]
		if len(chopped) > 6:
			listPrograms.append(chopped)

		for file in files:
			if os.path.join(currentpath, file).lower().endswith('.mp4'):
				allVideos.append(os.path.join(currentpath, file))
				if currentpath.find(directorySimpsonsPath) != -1:
					SimpsonsVideos.append(os.path.join(currentpath, file))
				elif currentpath.find(directoryDariaPath) != -1:
					DariaVideos.append(os.path.join(currentpath, file))
				elif currentpath.find(directoryAngelPath) != -1:
					AngelVideos.append(os.path.join(currentpath, file))
				elif currentpath.find(directoryMomPath) != -1:
					MomVideos.append(os.path.join(currentpath, file))
				elif currentpath.find(directoryMoonPath) != -1:
					MoonVideos.append(os.path.join(currentpath, file))
				elif currentpath.find(directoryRockPath) != -1:
					RockVideos.append(os.path.join(currentpath, file))

				elif currentpath.find(directoryGoldenPath) != -1:
					GoldenVideos.append(os.path.join(currentpath, file))
				elif currentpath.find(directoryBarnyardPath) != -1:
					BarnyardVideos.append(os.path.join(currentpath, file))

				elif currentpath.find(directoryNannyPath) != -1:
					NannyVideos.append(os.path.join(currentpath, file))

				elif currentpath.find(directoryTotallyPath) != -1:
					TotallyVideos.append(os.path.join(currentpath, file))

				elif currentpath.find(directoryGarfieldPath) != -1:
					GarfieldVideos.append(os.path.join(currentpath, file))
#				elif currentpath.find(directoryGarfieldPath2) != -1:
#					GarfieldVideos.append(os.path.join(currentpath, file))

				elif currentpath.find(directoryRavenPath) != -1:
					RavenVideos.append(os.path.join(currentpath, file))

				elif currentpath.find(directoryRockoPath) != -1:
					RockoVideos.append(os.path.join(currentpath, file))

				elif currentpath.find(directoryLooneyPath) != -1:
					LooneyVideos.append(os.path.join(currentpath, file))
				elif currentpath.find(directoryXmenEPath) != -1:
					XmenEVideos.append(os.path.join(currentpath, file))


			elif os.path.join(currentpath, file).lower().endswith('.mkv'):
				allVideos.append(os.path.join(currentpath, file))
				if currentpath.find(directorySimpsonsPath) != -1:
					SimpsonsVideos.append(os.path.join(currentpath, file))


	for i in mountPaths:
		dirPath = os.path.join(i, "")
		dirPath = os.path.join(dirPath, 'videos')
		for currentpath, folders, files in os.walk(dirPath):
			chopped = currentpath[len(dirPath) - 6:len(currentpath)]
			if len(chopped) > 6:
				listPrograms.append(chopped)
			for file in files:
				if os.path.join(currentpath, file).lower().endswith('.mp4'):
					allVideos.append(os.path.join(currentpath, file))

					if currentpath.find(directoryDariaPath) != -1:
						DariaVideos.append(os.path.join(currentpath, file))
					elif currentpath.find(directoryAngelPath) != -1:
						AngelVideos.append(os.path.join(currentpath, file))

					elif currentpath.find(directoryMomPath) != -1:
						MomVideos.append(os.path.join(currentpath, file))
					elif currentpath.find(directoryMoonPath) != -1:
						MoonVideos.append(os.path.join(currentpath, file))
					elif currentpath.find(directoryRockPath) != -1:
						RockVideos.append(os.path.join(currentpath, file))
					elif currentpath.find(directoryGoldenPath) != -1:
						GoldenVideos.append(os.path.join(currentpath, file))
					elif currentpath.find(directoryBarnyardPath) != -1:
						BarnyardVideos.append(os.path.join(currentpath, file))
	
					elif currentpath.find(directoryNannyPath) != -1:
						NannyVideos.append(os.path.join(currentpath, file))
	
					elif currentpath.find(directoryTotallyPath) != -1:
						TotallyVideos.append(os.path.join(currentpath, file))
	
					elif currentpath.find(directoryGarfieldPath) != -1:
						GarfieldVideos.append(os.path.join(currentpath, file))
	
					elif currentpath.find(directoryRavenPath) != -1:
						RavenVideos.append(os.path.join(currentpath, file))
	
					elif currentpath.find(directoryRockoPath) != -1:
						RockoVideos.append(os.path.join(currentpath, file))
					elif currentpath.find(directoryLooneyPath) != -1:
						LooneyVideos.append(os.path.join(currentpath, file))
					elif currentpath.find(directoryXmenEPath) != -1:
						XmenEVideos.append(os.path.join(currentpath, file))


				elif os.path.join(currentpath, file).lower().endswith('.mkv'):
					allVideos.append(os.path.join(currentpath, file))
	listPrograms.sort()
	k = 0
	for i in listPrograms:
		if i.find(directoryDariaPath) != -1:
			DariaIndex = k
		elif i.find(directoryAngelPath) != -1:
			AngelIndex = k
		elif i.find(directoryMomPath) != -1:
			MomIndex = k
		elif i.find(directoryMoonPath) != -1:
			MoonIndex = k
		elif i.find(directoryRockPath) != -1:
			RockIndex = k
		elif i.find(directorySimpsonsPath) != -1:
			SimpsonsIndex = k
		elif i.find(directoryGoldenPath) != -1:
			GoldenIndex = k
		elif i.find(directoryBarnyardPath) != -1:
			BarnyardIndex = k
		elif i.find(directoryNannyPath) != -1:
			NannyIndex = k
		elif i.find(directoryTotallyPath) != -1:
			TotallyIndex = k
		elif i.find(directoryRockoPath) != -1:
			RockoIndex = k
		elif i.find(directoryGarfieldPath) != -1:
			GarfieldIndex = k
		elif i.find(directoryRavenPath) != -1:
			RavenIndex = k

		elif i.find(directoryXmenEPath) != -1:
			XmenEIndex = k

		elif i.find(directoryLooneyPath) != -1:
			LooneyIndex = k
		k += 1



def initVideoList2():
	global ZombieVideos
	global directoryZombiePath

	global mountPaths
	dirPath = directory
	listPrograms = []

	chopped = ""

	for i in mountPaths:
		dirPath = os.path.join(i, "")
		dirPath = os.path.join(dirPath, 'videos2')
		for currentpath, folders, files in os.walk(dirPath):
			chopped = currentpath[len(dirPath) - 6:len(currentpath)]
			if len(chopped) > 6:
				listPrograms.append(chopped)
			for file in files:
				if os.path.join(currentpath, file).lower().endswith('.mp4'):
					if currentpath.find(directoryZombiePath) != -1:
						ZombieVideos.append(os.path.join(currentpath, file))

				elif os.path.join(currentpath, file).lower().endswith('.mkv'):
					if currentpath.find(directoryZombiePath) != -1:
						ZombieVideos.append(os.path.join(currentpath, file))

def endWait(length):
	global player
	global mutex
	global stopPlayer
	global pausePlayer
	global curIndex
	forced = False
	global timeLeft
	timeLeft = int(length)
	global origTimeLeft
	origTimeLeft = length
	global firstT
	global channelChanged
	firstT = datetime.now()
	lastT = datetime.now()
	delta = lastT - firstT
	stopped = False
	global adjustedTime
	adjustedTime = 0
	timeLeft = origTimeLeft - delta.seconds
	global curFile
	tempCmd = "echo \"" + curFile + "\"> /tmp/curFile"
	os.system(tempCmd)			

	while timeLeft > 0 and forced == False:
		time.sleep(1)
		if pausePlayer:
			try:
				if player is not None and player.playback_status() == "Playing":
					player.pause()
					print("Playback paused")
					timeLeft = timeLeft + 1
	
				continue
			except Exception as e:
				player = None
				forced = True
		elif channelChanged == False:
			try:
				if player is not None and player.playback_status() != "Playing":
					player.play()
					print("Resume playback")
			except Exception as e:
				player = None
		lastT = datetime.now()
		delta = lastT - firstT
		timeLeft = origTimeLeft - (delta.seconds + adjustedTime)
		tempCmd = "echo \"" + str(timeLeft) + "\"> /tmp/timeLeft"
		os.system(tempCmd)			

		tempCmd = "echo \"" + str(adjustedTime) + "\"> /tmp/timeAdjusted"
		os.system(tempCmd)			
		
		tempCmd = 'sudo ps -ux| grep omxplayer.bin'
		#check if omxplayer is still running
		try:
			value = check_output(tempCmd, shell=True)
		except CalledProcessError as e:
			value = ""
		if not value:
			origTimeLeft = timeLeft
			forced = True
		else:
			if len(value) < 10:
				origTimeLeft = timeLeft
				forced = True
		skipFileExists = exists('/tmp/skipFile')
		changeIndexExists = exists('/tmp/newIndex')
		if skipFileExists:
			os.system('sudo rm /tmp/skipFile')
			forced = True
			skipFileExists = False
			mutex.acquire()
			if player is not None:
				player.quit()
				print("Skip file set player to None")
				player = None
				stopPlayer = True
			mutex.release()
		if changeIndexExists:
			fo = open("/tmp/newIndex", "rt")
			line = fo.read(10)
			print("I read " + line)
			try:
				curIndex = 0 #initial value
				curIndex = int(line) - 1
				forced = True
			except Exception as e:
				forced = False				
			fo.close()
			os.system('sudo rm /tmp/newIndex')
			mutex.acquire()
			if player is not None:
				player.quit()
				print("Skip file set player to None")
				player = None
				stopPlayer = True
			mutex.release()
		if stopPlayer:
			print("stopPlayer detected")
			forced = True
def playVideos():
	global curFile
	global videos
	global curIndex
	global stopPlayer
	global isWide
	global isLetterbox
	global isCommentary
	global isSimpsons
	global nextHeldCnt
	global volumeScale
	global curVolume
	global remoteOverride
	curIndex = 0
	vLength = 0
	global player
	global mutex
	global overlapTime
	if len(videos) == 0:
		getVideos()
		time.sleep(5)
		return
	#random.shuffle(videos)
	videos = random.sample(videos, len (videos))
	outputList()
	length = len(videos)
	endLoop = False
	while endLoop == False:
		endLoop = False
		if curIndex >= len(videos):
			curIndex = 0
			videos = random.sample(videos, len (videos))

		tempCmd = "echo " + str(curIndex) + " > /tmp/curIndex"
		os.system(tempCmd)			

		video = videos[curIndex]
		curFile = video
		tempCmd = 'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "%s"' % video
		value =  check_output(tempCmd, shell=True)
		vLength = int(float(value))
		Nextheldcnt = 0
		mutex.acquire()
		if player is not None:
			player.quit()
			player = None

		if isLetterBox:
			player = OMXPlayer(video,args='--no-osd --aspect-mode Letterbox')
		elif isWide:
			player = OMXPlayer(video,args='--no-osd --aspect-mode stretch')
		else: #zoom
			player = OMXPlayer(video,args='--no-osd --aspect-mode fill')
		print("Normal set player after opening")
		if (remoteOverride or isSimpsons) and isCommentary:
			curVolume = 2.5
			player.select_audio(2)
		else:
			curVolume = 1.25
		player.set_volume(curVolume * volumeScale)

		checkMute(True)
		if player is None:
			print("WTF! player is none!")
		mutex.release()
		endWait(vLength - overlapTime)
		curIndex = curIndex + 1
		if stopPlayer:
			stopPlayer = False
			mutex.acquire()
			if player is not None:
				player.quit()
				print("Stop player set player to None")
				player = None
			mutex.release()
			if length != len(videos): #changed mode
				length = len(videos)
				endLoop = True
			
def setup():
	devPaths = ['/dev/sda','/dev/sdb','/dev/sdc','/dev/sdd','/dev/sda1','/dev/sdb1','/dev/sdc1','/dev/sdd1',]
	j = 0
	for i in mountPaths:
		#Mount the stuff
		mountProcess = Popen(['mount', '-r', devPaths[j], i])
		mountProcess.wait()
		j = j + 1
	initVideoList()
	initVideoList2()

	myThread = threading.Thread(target=buttonWatcher)
	myThread.start()
	myRemoteThread = threading.Thread(target=remoteThread)
	myRemoteThread.start()

def buttonWatcher():
	global isSpecialDown
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
	isSpecialDown = GPIO.input(20)
	isLetterBox = GPIO.input(17)
	isWide = GPIO.input(27) # Wide = Stretched
	isMute = not GPIO.input(26)
	isScreenOn = GPIO.input(18)
	input = False
	initDone = True
	while(True):
		try:
			checkSimpsons()
			checkCommentary(False)
			checkLetterBox()
			checkWide(False)
			checkMute(False)
			checkScreenOn()
			if not stopPlayer:
				checkNext()
			checkSpecial()
			time.sleep(0.2)
		except Exception as e:
			print("Caught button exception")
def checkSimpsons():
	global isSimpsons
	global stopPlayer
	global initDone
	global remoteOverride
	input =  GPIO.input(22)

	if input != isSimpsons:
		isSimpsons = input
		if initDone:
			#print("isSimpsons changed to ", isSimpsons)
			remoteOverride = False
			getVideos()  
			stopPlayer = True

def checkCommentary(forced):
	global isCommentary
	global player
	global mutex
	global isSimpsons
	global initDone
	global remoteOverride
	global curVolume
	global volumeScale
	input = GPIO.input(16)
	#print("Commentary is ",isSimpsons, input)

	if remoteOverride and forced == False:
		return #do nothing
	if ((isSimpsons or (remoteOverride and forced)) or initDone == False):
		if input != isCommentary or initDone == False or forced:
			#print("Commentary is ",input)
			if not forced:
				isCommentary = input
				remoteOverride = False
			if initDone:
				mutex.acquire()
				if player is not None:
					if isCommentary:
						curVolume = 2.5
						player.select_audio(2)
					else:
						player.select_audio(0)
						curVolume = 1.25
					player.set_volume(curVolume * volumeScale)
				mutex.release()

def checkLetterBox():
	global isLetterBox
	global player
	global mutex
	global remoteAspectOverride
	global remoteOverride
	global remoteAspectOverride

	input = GPIO.input(17)
	input2 = GPIO.input(27)

	if remoteAspectOverride and remoteOverride:
		return
	if input != isLetterBox:
		remoteOverride = False
		RemoteAspectOverride = False
		isLetterBox = input
		mutex.acquire()
		if player is not None:
			if input:
				#print("Set to letterbox")
				player.set_aspect_mode('letterbox')
			#else should be handled by 4de
			else:
				mutex.release()
				checkWide(True)
				mutex.acquire()
		else:
			print("letter box player is none!")
		mutex.release()


def checkWide(isForced):
	global isWide
	global isLetterBox
	global player
	global mutex
	global RemoteAspectOverride 
	global remoteOverride
	input = GPIO.input(27) # Wide = Stretched

	if remoteAspectOverride and remoteOverride and isForced == False:
		return

	if (isWide != input and isLetterBox == False) or isForced == True:
		#print("isWide is now ", isWide)
		isWide = input
		print("Forced is " + str(isForced))

		mutex.acquire()
		if player is not None:
			remoteOverride = False
			RemoteAspectOverride = False

			if input:
				player.set_aspect_mode('stretch')
			else:
				player.set_aspect_mode('fill')
		else:
			print("wide player is none!")
		mutex.release()

def checkMute(isForced):
	global isMute
	global isMuteB
	global isDualScreen
	global player
	global remoteOverride
	input = not GPIO.input(26)
	muteChanged = False
	if input != isMuteB:
		isMuteB = input;
		remoteOverride = False
		muteChanged = True

	if (input != isMute) or isForced or (not remoteOverride and muteChanged):
		if muteChanged:
			isMute = isMuteB

		if isMute:
			if player is not None:
				player.mute()
				os.system('raspi-gpio set 19 ip')
		else:
			if player is not None:
				player.unmute()
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
	cmd = ""
	if val:
		cmd = 'sudo mount -o remount,ro / ; sudo mount -o remount,ro /boot'
	else:
		cmd = 'sudo mount -o remount,rw / ; sudo mount -o remount,rw /boot'
	os.system(cmd)
	

def checkScreenOn():
	global isDualScreen
	global isScreenOn	
	global initDone
	global isLCD
	isLCD = True
	shouldRestart = False
	if initDone == False:
		isDualScreen = not GPIO.input(21)
		hdmiFileExists = exists('/boot/hdmiFlag')
		dualFileExists = exists('/boot/dualFlag')
		if not isDualScreen:
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
			ReadOnly(False)
			if dualFileExists:
				os.system('sudo rm /boot/dualFlag')
			if not isLCD:
				if hdmiFileExists:
					print("External is connected and file is present")
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
		else:
			print("Dual Screen connected!")
			ReadOnly(False)
			if hdmiFileExists:
				os.system('sudo rm /boot/hdmiFlag')
				os.system('sudo cp -f /boot/hdmi/config.txt /boot/config.txt')
			os.system('sudo touch /boot/dualFlag')
			ReadOnly(True)			
	input = GPIO.input(18)
	if initDone == False or input != isScreenOn:
		isScreenOn = input
		if input:
			turnOnScreen()
		else:
			os.system('raspi-gpio set 19 ip')			
			if isLCD: #turn we'll only support turning off for the LCD
				os.system('tvservice -o')
def checkSpecial():
	global player
	global mutex
	global isSpecialDown
	global specialHeldCnt
	global adjustedTime
	global timeLeft
	global pausePlayer
	global initDone
	global nextHeldCnt
	global overlapTime
	global firstT
#	input = not GPIO.input(20) #disabled
	input = False
	if initDone:
		if input:
			specialHeldCnt = specialHeldCnt + 1
			computeLeft = specialHeldCnt % 5
			mutex.acquire()
			if specialHeldCnt > 15 and player is not None: #if 3 seconds have occurred and button is still pressed
				if timeLeft > 15 + overlapTime and computeLeft == 0:
					player.seek(-15)
					print("Skipping back by 15 seconds")

					adjustedTime = adjustedTime - 15
			mutex.release()
		else:
			if specialHeldCnt > 0 and specialHeldCnt < 15: #normal skip
				pausePlayer = not pausePlayer
			specialHeldCnt = 0
		
def checkNext():
	global stopPlayer
	global initDone
	global player
	global mutex
	global adjustedTime
#	input = not GPIO.input(6) #disable next button temporarily
	input = False
	global nextHeldCnt
	global overlapTime
	global firstT
	global timeLeft
	compute = 0
	if initDone:

		if input:
			nextHeldCnt = nextHeldCnt + 1
			computeLeft = nextHeldCnt % 5
			mutex.acquire()
			if nextHeldCnt > 15 and player is not None: 
				#if 3 seconds have occurred and button is still pressed
				if timeLeft > 15 + overlapTime and computeLeft == 0:
					player.seek(15)
					print("Skipping by 15 seconds")

					adjustedTime = adjustedTime + 15
			mutex.release()
		else:
			if nextHeldCnt > 0 and nextHeldCnt < 15: #normal skip
				print("Next track")
				stopPlayer = True
			nextHeldCnt = 0
		
		forwardFileExists = exists('/tmp/forwardFlag')
		if forwardFileExists:
			print("Forward flag check", forwardFileExists)
			print("Forward Exist")
			f = open("/tmp/forwardFlag","rt")
			skipLen = f.readline()
			try:
				timeLen = int (skipLen)
			except:
				timeLen = 15
			os.system('rm -rf /tmp/forwardFlag')
			if timeLeft > timeLen + overlapTime and player is not None:
				mutex.acquire()
				print("Skipping by " + str(timeLen) + " seconds")
				player.seek(timeLen)
				mutex.release()
				adjustedTime = adjustedTime + timeLen

def getBinary():
	global remotePin
	#Internal vars
	num1s = 0 #Number of consecutive 1s read
	binary = 1 #The bianry value
	command = [] #The list to store pulse times in
	previousValue = 0 #The last value
	value = GPIO.input(remotePin) #The current value
	
	#Waits for the sensor to pull pin low
	while value:
		value = GPIO.input(remotePin)
		
	#Records start time
	startTime = datetime.now()
	
	while True:
		#If change detected in value
		if previousValue != value:
			now = datetime.now()
			pulseTime = now - startTime #Calculate the time of pulse
			startTime = now #Reset start time
			command.append((previousValue, pulseTime.microseconds)) #Store recorded data
			
		#Updates consecutive 1s variable
		if value:
			num1s += 1
		else:
			num1s = 0
		
		#Breaks program when the amount of 1s surpasses 10000
		if num1s > 10000:
			break
			
		#Re-reads pin
		previousValue = value
		value = GPIO.input(remotePin)
		
	#Converts times to binary
	for (typ, tme) in command:
		if typ == 1: #If looking at rest period
			if tme > 1000: #If pulse greater than 1000us
				binary = binary *10 +1 #Must be 1
			else:
				binary *= 10 #Must be 0
			
	if len(str(binary)) > 34: #Sometimes, there is some stray characters
		binary = int(str(binary)[:34])
		
	return binary
	
def convertHex(binaryValue):
	tmpB2 = int(str(binaryValue),2) #Tempary propper base 2
	return hex(tmpB2)

def remoteThread():	
	global altChannel
	global player
	global adjustedTime
	global timeLeft
	global overlapTime
	global Buttons
	global ButtonsNames
	global origTimeLeft
	global remoteOverride
	global remoteChannel
	global channelIndex
	global stopPlayer
	global curIndex
	global videos
	global channelChanged
	global curVolume
	global volumeScale
	global isCommentary
	global curFile
	global isWide
	global isLetterBox
	global remoteAspectOverride
	global ZombieVideos
	global pausePlayer
	global isMute
	while True:
		try:
			inData = convertHex(getBinary()) #Runs subs to get incomming hex value
			oldchannelIndex = remoteChannel

			for button in range(len(Buttons)):#Runs through every value in list
				if hex(Buttons[button]) == inData: #Checks this against incomming
					if ButtonsNames[button] == "FORWARD15":
						if timeLeft > 15 + overlapTime and player is not None:
							player.seek(15)
							print("Skipping by 15 seconds")
		
							adjustedTime = adjustedTime + 15
							break
					elif ButtonsNames[button] == "BACK15":
						if origTimeLeft - timeLeft > (15 + overlapTime) and player is not None:
							player.seek(-15)
							print("Skipping back by 15 seconds")
							adjustedTime = adjustedTime - 15
							break

					elif ButtonsNames[button] == "NEXT":
						os.system('sudo touch /tmp/skipFile')
						break

					elif ButtonsNames[button] == "PREVIOUS":
						curIndex -= 2
						if curIndex == 0:
							curIndex = len(videos) - 2
						elif curIndex == 1:
							curIndex = len(videos) - 1
						stopPlayer = True
						break


					elif ButtonsNames[button].find("UP") != -1:
						if volumeScale < 1.5:
							volumeScale += 0.1
							if player is not None:
								player.set_volume(curVolume * volumeScale)
								if (isMute):
									isMute = False
									checkMute(True)
						break
					elif ButtonsNames[button].find("DOWN") != -1:
						if volumeScale > 0.1:
							volumeScale -= 0.1
							if player is not None:
								player.set_volume(curVolume * volumeScale)
								if (isMute):
									isMute = False
									checkMute(True)
						break

					elif ButtonsNames[button].find("CHANNEL") != -1:
						chanVal = ButtonsNames[button][7:len(ButtonsNames[button])]
						chanVal = int(chanVal)
						altChannelChanged = False
						if chanVal == oldchannelIndex:
							if chanVal > 5:
								break
							altChannel = not altChannel
							altChannelChanged = True
						else:
							altChannel = False
						if player is not None and player.playback_status() == "Playing":
							player.pause()
						remoteOverride = True
						remoteChannel = chanVal
						getVideos()  
						channelChanged = True
						stopPlayer = True
						curIndex = 999999
						break

					elif ButtonsNames[button] == ("Digits"):
						chanVal = 10
						if chanVal == oldchannelIndex:
							break
						Altchannel = False

						if player is not None and player.playback_status() == "Playing":
							player.pause()
						remoteOverride = True
						remoteChannel = chanVal
						getVideos()  
						channelChanged = True
						stopPlayer = True
						break
					elif ButtonsNames[button] == ("Last"):
						chanVal = 11
						if chanVal == oldchannelIndex:
							break
						altChannel = False

						if player is not None and player.playback_status() == "Playing":
							player.pause()
						remoteOverride = True
						remoteChannel = chanVal
						getVideos()  
						channelChanged = True
						stopPlayer = True
						break

					elif ButtonsNames[button] == "CH+":
						remoteOverride = True
						remoteChannel = -1
						channelIndex += 1
						if channelIndex >= len (listPrograms):
							channelIndex = 0
						if player is not None and player.playback_status() == "Playing":
							player.pause()

						getVideos()  
						channelChanged = True
						stopPlayer = True
						break
					elif ButtonsNames[button] == "CH-":
						remoteOverride = True
						remoteChannel = -1
						channelIndex -= 1
						if channelIndex < 0:
							channelIndex = len (listPrograms) - 1
						if player is not None and player.playback_status() == "Playing":
							player.pause()

						getVideos()  
						channelChanged = True
						stopPlayer = True
						break
					elif ButtonsNames[button] == "Green":
						print ("GREEN")
						remoteOverride = True
						isMute = not isMute
						checkMute(True)

					elif ButtonsNames[button] == "Red":
						remoteOverride = True
						if curFile.find("mkv") != -1:
							isCommentary = not isCommentary
						else:
							isCommentary = False
						checkCommentary(True)
					elif ButtonsNames[button] == "PLAY":
						pausePlayer = not pausePlayer
					elif ButtonsNames[button] == "Blue":
						remoteOverride = True
						remoteAspectOverride = True
						if isLetterBox:  #currently 4:3 -> Stretch
							isLetterBox = False
							isWide = False
							if player is not None:
								player.set_aspect_mode('fill')
						elif isLetterBox == False and isWide: 
							isLetterBox = True
							isWide = False
							if player is not None:
								player.set_aspect_mode('letterbox')

						else:
							isLetterBox = False
							isWide = True
							if player is not None:
								player.set_aspect_mode('stretch')

		except Exception as e:
			print("Remote exception caught")
rng = secrets.SystemRandom()
#seedV = rng.randint(0, 262144*2)
current_date = datetime.now()
seedV = current_date.year * 10000000000 + current_date.month * 100000000 + current_date.day * 1000000 + current_date.hour*10000 + current_date.minute*100 + current_date.second
print("Seed is " + str(seedV))
random.seed(seedV)
checkScreenOn()
setup()
while (True):
	playVideos()