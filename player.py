import os
import random
import time
import RPi.GPIO as GPIO
from subprocess import PIPE, Popen, STDOUT

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)

directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'videos')
directoryS = os.path.join(directory, 'The Simpsons')
simpsonsOnly = False
videos = []


def isVideo(videofile):
	if videofile.lower().endswith('.mp4'):
		return True
	if videofile.lower().endswith('.mkv'):
		return True
	if videofile.lower().endswith('.mov'):
		return True
	if videofile.lower().endswith('.avi'):
		return True
	if videofile.lower().endswith('.mpg'):
		return True
	if videofile.lower().endswith('.mpeg'):
		return True
	if videofile.lower().endswith('.wmv'):
		return True
	return False

def getVideos():
    global videos
    videos = []
    vidpath = directory
    if (simpsonsOnly):
        vidpath = simpsonsOnly
    for currentpath, folders, files in os.walk(vidpath):
        for file in files:
            if isVideo(file):
               videos.append(os.path.join(directory, file))

def playVideos():
    global videos
    if len(videos) == 0:
        getVideos()
        time.sleep(5)
        return
    random.shuffle(videos)
    for video in videos:
        playProcess = Popen(['omxplayer', '--no-osd', '--aspect-mode', 'fill', video])
        playProcess.wait()


while (True):
    playVideos()
