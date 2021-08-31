A modified version of the Simpsons TV with the following modifications:

1. External USB port
2. External HDMI port
3. A switch to toggle between playing a certain folder to be played, all folders to be played
4. Supports sub folders in playback
5. Supports sub folders in encoding
6. Encoded video audio is normalized

Requirements:
A. Encoding Videos
1. Some kind of PC
2. FFMpeg installed
3. ffmpeg-normalizer installed

B. Minimum Hardware
1. A Raspberry Pi of sorts
2. Some kind of screen, preferably the 2.8 in screen that has a way to short PWM and GPIO 18
3. An SD card
4. A USB-C/Micro USB female to breakout board
5. A Micro USB male connector
6. 22 AWG wires (red and black)

C. Optional Hardware
1. 1k resistor (For the directory enable feature)
2. A 104 capacitor (For the directory enable feature)
3. A 3 pin sliding switch (For the directory enable feature)
4. A micro usb to usb female connector (External USB port)
5. A short HDMI extension cable (External hdmi port)
6. A push button (For turning on/off screen, will probably work only for the 2.8 in screen with PWM shorted to GPIO 18)
7. A 5W mono speaker (For sound if your screen has no speakers)
8. A 1K ohm potentiometer (For adjust sound outputted on the speaker
9. A PAM8302 board (For amplifying the mono sound that will be output by the speaker)

Absolute minimum would probably be like:
A portable monitor (with speakers, power and volume control) connected to the Pi via HDMI. Both are powered separately or portable monitor powers Pi itself.
