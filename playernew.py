import os
import time
from subprocess import PIPE, Popen, STDOUT
from omxplayer.player import OMXPlayer


#directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'videos')
root_path = "/home/pi/simpsonstv/videos/"
Directories = ["trigun","spongebob","mlp"]
directory_pointer = 0
cur_directory = Directories[directory_pointer]
video_pointer = 0
playNew = False   #When true, triggers playing a new video


videos = []

def isVideo(videofile):
	if videofile.lower().endswith('.mp4'):
		return True
	if videofile.lower().endswith('.mkv'):
		return True
	if videofile.lower().endswith('.m4v'):
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
    displayDirectoryVideo()  #Display Channel and Selected Video on the LCD screen
    playNew = True

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
    global root_path
    
    videos = []
    vidpath = cur_directory
    #print(cur_directory)
    #print(root_path + cur_directory)
    #for currentpath, folders, files in os.walk(vidpath):
    for file in os.listdir(root_path + cur_directory):
        #for file in files:
        #print(file)
        if isVideo(file):
            videos.append(os.path.join(root_path + cur_directory, file))


def playVideos():
    global videos
    global video_pointer
    global player
    global playNew
    global manualSelect
    if len(videos) == 0:
        getVideos()
        time.sleep(5)
        return
    video = videos[video_pointer]
    if(playNew == True):
        player=OMXPlayer(video)
        player.set_aspect_mode('stretch')	
        player.exitEvent = lambda _, exit_code: autoPlayNext(exit_code) #Set OMXPlayer exit event handler to call the
                                                                     # autoPlayNext() routine when OMXPlayer exits
        playNew = False                #Reset the playNew flag
        print("playNew set to False")
        manualSelect = False           #Reset the manualSelect flag (indicates automatic play unless changed by user)
    #playProcess = Popen(['omxplayer', '--no-osd', '--aspect-mode', 'fill', video])
    #playProcess.wait()


# #-----------------------------------------------------------------------------------------------------------------
# # nextVideo(): Select the next video by incrementing the video_pointer;  Loops around once the end is reached
# #              Returns nothing
# def nextVideo():
#     #Must specify "global" variables - otherwise, the routine would create its own unique copy
#     # of these variables when they are used.
#     global video_pointer
#     global videos
#     global manualSelect
#     global player
#     manualSelect = True  #Set the flag to indicate the next video was manually selected
#     player.quit()        #Stop the currently playing video - this kills the current OMXPlayer instance
#     video_pointer += 1   # Increment video_pointer
#     if(video_pointer > (len(videos)-1)):
#       video_pointer = 0  #Loop video_pointer back around once end of videos is reached
#     displayDirectoryVideo() #Display Channel and Selected Video on the LCD screen
#     playNew = True
#-----------------------------------------------------------------------------------------------------------------
# autoPlayNext(): Executed when an instance of OMXPlayer exits.  It automatically starts playing the next video in
#                 the current channel if the last video played to completion.  It will not try to play a video if
#                 OMXPlayer was shutdown by the user manually (i.e. selecting through videos for the next video).
#                 In the case of a manual video selection, the video will be played in the main loop.
#                 Returns nothing
def autoPlayNext(code):
   #Must specify "global" variables - otherwise, the routine would create its own unique copy
   # of these variables when they are used.
   print(code)
   global video_pointer
   global videos
   global manualSelect
   global video_pointer
   if (manualSelect == True):  #If this routine was entered by the user manually selecting the next video,
     manualSelect = False      # clear the manualSelect flag and,
     return                    # return doing nothing else - the main loop will handle manual select operations
   video_pointer +=1 # If this routine was entered due to a video completing playback, increment the video_pointer
   if(video_pointer > (len(videos)-1)):  #Loop the video pointer back around once the end of videos is reached
     video_pointer = 0
   displayDirectoryVideo()     #Display Channel and Selected Video on the LCD screen
   playNew = True
   print("playNew set to true in autoPlayNext")

#-----------------------------------------------------------------------------------------------------------------
# displayDirectoryVideo():  Displays the currently selected Video and Channel on the LCD
#                           Returns nothing
def displayDirectoryVideo():
    #Must specify "global" variables - otherwise, the routine would create its own unique copy
    # of these variables when they are used.
    global root_path
    global cur_directory
    global Current_Video
    global VIDEO_PATH
    global PlayTimer
    global playNew
    global video_pointer
    global videos
    #os.system("clear")  #clear the LCD screen
    #print(videos)
    #print(video_pointer)
    Current_Video = videos[video_pointer]  #Set current video to that specified by the video_pointer
    #VIDEO_PATH = Path(root_path + cur_directory + "/" + Current_Video)
    VIDEO_PATH = Current_Video
    print("")
    print("")
    print("")
    print("  Channel: " + cur_directory)  #Print the "Channel" (directory) on the LCD screen
    print("  " + Current_Video[0:len(Current_Video)-4])  #Print the video selected on the LCD screen
    #PlayTimer = millis()
    playNew = True  #Trigger starting the play of the new video in 1.5 seconds
    print("playNew set to true in displayDirectoryVideo")

getVideos()
displayDirectoryVideo()
while (True):
    #add code for switching channels, checking for skipping to next video, etc.
    #switchDirectory()    
    playVideos()


    #nextVideo()
