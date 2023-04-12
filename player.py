import os
import time
from subprocess import PIPE, Popen, STDOUT

#directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'videos')
root_path = "/home/pi/simpsonstv/videos/"
Directories = ["spongebob", "trigun","mlp"]
directory_pointer = 0
cur_directory = Directories[directory_pointer]
video_pointer = 0


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

#-----------------------------------------------------------------------------------------------------------------
# switchDirectory(): Select the next channel (directory) in the Directories string array - also point to the first
#                    video in this newly selected channel.
#                    Returns nothing
def switchDirectory():
    #Must specify "global" variables - otherwise, the routine would create its own unique copy
    # of these variables when they are used.
    global video_pointer
    global Directory_Pointer
    global cur_directory
    global Directories
    global manualSelect
    global player
    manualSelect=True   #Set the flag to indicate the next video was manually selected
    player.quit()       #Stop the currently playing video - this kills the current OMXPlayer instance
    video_pointer = 0   #Set video pointer to the first video in the newly specified channel
    Directory_Pointer +=1 #Increment the Channel Pointer
    if(Directory_Pointer > (len(Directories)-1)):
      Directory_Pointer = 0  #Loop the Channel pointer back around once end of channels is reached
    cur_directory = Directories[Directory_Pointer]  #Set current channel specified by the Directory_Pointer
    getVideos()         #Identify all videos in the newly specified channel (directory)
    #displayDirectoryVideo()  #Display Channel and Selected Video on the LCD screen

# def getVideos():
#     global videos
#     videos = []
#     files = [f for f in os.listdir(directory) if f.lower().endswith('.mp4')]
#     files.sort()  # sort files alphabetically
#     for file in files:
#         videos.append(os.path.join(directory, file))

def getVideos():
    global videos
    global cur_directory
    
    videos = []
    vidpath = cur_directory
    for currentpath, folders, files in os.walk(vidpath):
        for file in files:
            if isVideo(file):
               videos.append(os.path.join(root_path + cur_directory, file))


def playVideos():
    global videos
    global video_pointer
    if len(videos) == 0:
        getVideos()
        time.sleep(5)
        return
    video = videos[video_pointer]
    playProcess = Popen(['omxplayer', '--no-osd', '--aspect-mode', 'fill', video])
    playProcess.wait()
        #add code for switching directories
        #switchDirectory()

#-----------------------------------------------------------------------------------------------------------------
# nextVideo(): Select the next video by incrementing the video_pointer;  Loops around once the end is reached
#              Returns nothing
def nextVideo():
    #Must specify "global" variables - otherwise, the routine would create its own unique copy
    # of these variables when they are used.
    global video_pointer
    global videos
    global manualSelect
    global player
    manualSelect = True  #Set the flag to indicate the next video was manually selected
    player.quit()        #Stop the currently playing video - this kills the current OMXPlayer instance
    video_pointer += 1   # Increment video_pointer
    if(video_pointer > (len(videos)-1)):
      video_pointer = 0  #Loop video_pointer back around once end of videos is reached
    #displayDirectoryVideo() #Display Channel and Selected Video on the LCD screen


while (True):
    playVideos()
    nextVideo()
