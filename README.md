This project is mostly completed. 

To do:
1. Add code to support incerasing the volume for commentary tracks if they're playing.
2. Automatically restart Pi if user switches between LCD or external screen

Things I hate:
1. Looks ugly
2. Sound quality is pretty bad even after adjust a lot of settings. Thankfully earphones still work. I would look for better speakers and amplifier than the one the original author propsoed

A modified version of the Simpsons TV with the following modifications:

1. Will not need 3d printing at all
2. Uses Pi 3B
3. Uses 7 inch 16:9 screen
4. 2 switches to toggle between follow 4:3 ratio, stretch horizontally, zoom in
5. Supports sub folders in playback
6. Seamless playing of videos between files
7. Loading from multiple USB drives
8. Support for USB drives
9. Support for using LCD or a different screen
10. Supports mode to play Simpsons only content
11. Supports playing of Simpsons commentary while in Simpsons mode (Issue is if commentary is weaker in volume and omxplayer can't adjust gain on the fly). Can be used to swap between audio tracks

Requirements:
A. Encoding Videos
1. Some kind of PC
2. FFMpeg installed
3. ffmpeg-normalizer installed

B. Minimum Hardware
1. A Raspberry Pi of sorts (preferably a Pi 3B)
2. Some kind of screen, preferably the 2.8 in screen that has a way to short PWM and GPIO 18. For ease, I recommend the 2.8 inch monitor with breakout pins for easy access to ground and 3.3V and GPIO25 and it has a jumper pin for shorting the pwm and gpio18.
3. An SD card
4. A USB-C/Micro USB female to breakout board
5. A Micro USB male connector
6. 22 AWG wires (red and black)

C. Optional Hardware
1. 1k resistor (For the directory enable feature)
2. 3 3 pin sliding switch (For the directory enable feature)
4. A micro usb to usb female connector (External USB port)
5. A push button (For turning on/off screen, will probably work only for the 2.8 in screen with PWM shorted to GPIO 18)
6. A 5W mono speaker (For sound if your screen has no speakers)
7. A 1K ohm potentiometer (For adjust sound outputted on the speaker
8. A PAM8302 board (For amplifying the mono sound that will be output by the speaker)
9. A USB mosfet relay (Allow pi to power on/off an external screen)
10. 2 USB C female breakout boards
11. 2 USB A female breakouts board
 
Absolute minimum would probably be like:
A portable monitor (with speakers, power and volume control) connected to the Pi via HDMI. Both are powered separately or portable monitor powers Pi itself.

D. Minimum Software installed
1. omxplayer
2. omxplayer-wrapper
3. ffmpeg (For ffprobe)
