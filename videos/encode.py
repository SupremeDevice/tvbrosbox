import os

newFiles = []
directory = os.path.dirname(os.path.realpath(__file__))
toencdirectory = os.path.join(directory, 'ToEncode')
destinationDirectory = os.path.join(directory, 'encoded')
normDirectory = os.path.join(directory, 'normalized')

if not os.path.exists(destinationDirectory):
	os.mkdir(destinationDirectory)


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

newFiles = [os.path.join(dp, f) for dp, dn, filenames in os.walk(directory) for f in filenames if isVideo(f)]

for filepath in newFiles:
	video = os.path.basename(filepath)
	videoName = os.path.splitext(video)[0]
	newFile = '%s.mp4' % videoName
	i = filepath
	o = os.path.join(destinationDirectory, newFile)
	n = os.path.join(normDirectory, newFile)
	if os.path.isfile(n):
		continue
	encodeCommand = 'ffmpeg -y -i "%s" -vf scale=640:480 -c:v libx264 -profile:v baseline -level 3.0 -preset faster -crf 23 -pix_fmt yuv420p "%s"' % (i, o)
	print('Encoding %s' % newFile)
	encode = os.popen(encodeCommand).read()
	print ('Normalize %s' % video)
	normCommand = 'ffmpeg-normalize "%s" -ext mp4 -c:a aac' % (o)
	norm = os.popen(normCommand).read()
	os.remove(o)
