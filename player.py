import os
import random
import time
import RPi.GPIO as GPIO
from subprocess import PIPE, Popen, STDOUT

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)

directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'videos')

videos = []


def getVideos():
    global videos
    videos = []
    for file in os.listdir(directory):
        if file.lower().endswith('.mp4'):
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
