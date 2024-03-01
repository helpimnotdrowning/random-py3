import sys

import PIL.Image

from datetime import datetime

class ANSICol:
	# special codes
	reset = '\033[0m'

ASCII_CHARS = list("  ´`':_-;!~+>=</*|?lt()yR1}[N{FJ7i]cv3A2zx4suKh5eBWP96Mo#d%08G&$Q@")
ASCII_CHARS = list("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#################################")
pixels = {}
asciiLines = {}

##
	# Convert RGB values to ANSI escape sequence
	#
	# @param red, green, blue Respective color channels
	# @param isBackground Should escape color the character background or foreground?
	#
	# @return Escape sequence as string
#
def RGB2ANSI(red, green, blue, isBackground=False):
	if isBackground:
		ansiColor = f"\033[48;2;{red};{green};{blue}m"
		
	else:
		ansiColor = f"\033[38;2;{red};{green};{blue}m"
		
	return ansiColor
	
##
	# Rescale image to width, accoriding to character size ratio
	#
	# @param image Target PIL Image
	# @param new_width Target width for image
	# @param Ratio to squish/stretch image by, should be about width/height of your font, or 
	#
	# @return Resized image
#
def scale_to_width(image, new_width, ratio = 3/5):
	width, height = image.size
	new_height = round(new_width * height // width * ratio)
	
	return image.resize((new_width, new_height))
	
def to_grayscale(image):
	return image.convert("L")

def img_to_ascii(image):
	ascii_str = ""
	column = 0;
	
	gray_pixels = to_grayscale(image).getdata()
	color_pixels = image.getdata()
	
	pixels = zip(gray_pixels, color_pixels)
	
	for pixel_tuple in pixels:
		ascii_str += RGB2ANSI(pixel_tuple[1][0], pixel_tuple[1][1], pixel_tuple[1][2], False)
		ascii_str += ASCII_CHARS[pixel_tuple[0]//4]
		column += 1
		
		if column == image.width:
			ascii_str += "\n"
			column = 0
	
	return ascii_str
	
def main():
	# check if file was passed as arg
	if sys.argv[1]:
		path = sys.argv[1]
		
	else:
		path = input("Enter the path to the image fiel : \n")
		
	# try to load
	try:
		image = PIL.Image.open(path)
		
	except:
		print("Couldn't load image")
		exit(2);
		
	#resize image, ratio for Berkeley Mono
	image = scale_to_width(image, 1024, 1/2)
	width, height = image.size
	
	ascii_str = img_to_ascii(image)
	
	print(ascii_str)
	print(ANSICol.reset)
	
main()

