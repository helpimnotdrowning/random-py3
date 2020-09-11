# ment for making minecraft panoramas

from PIL import Image
from datetime import datetime
import os
import forest as for

# list of image extensions
imgextlist = (".png", ".jpg", ".bmp", ".jpeg", ".tga", ".tif", ".tga")

img = input("Enter path to panorama : ")

try:
    im = Image.open(img)
except:
    input("This image does't exist.")
    input("Press ANY KEY to exit.")

im = Image.open(img)

width, height = im.size

if width/4 != height/3:
    input("This image can't be divided up into squares")
    input("Press ANY KEY to exit.")

width = width/4
height = height/3

timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
os.mkdir(timestamp)
log("created directory \"" + timestamp + "\"")

# visualization to represent the corners of the squares
# ↓XA is the top left corner of the square and cropping origin
# ↑XB is the bottom right corner of the square and where cropping ends
#
#        ↓4A
# ┌      ┌──────┐             ┐
#        │      │              
# ↓0A    ↓1A    ↓2A    ↓3A     
# ┌──────┼──────┼──────┬──────┐
# │      │      ↑4B    │      │
# │      ↓5A    │      │      │
# └──────┼──────┼──────┴──────┘
#        ↑0B    ↑1B    ↑2B    ↑3B
#        │      │              
# └      └──────┘             ┘
#               ↑5B

# top left corner of crop is 1st 2 args, bottom right is the other 2 args.

# pano 0
pano0 = im.crop((0, height, width, height*2)).save(timestamp + "/panorama_0.png","png")
log("saved cube face 0 at " + timestamp + "/panorama_0.png")
# pano 1
pano1 = im.crop((width, height, width*2, height*2)).save(timestamp + "/panorama_1.png","png")
log("saved cube face 1 at " + timestamp + "/panorama_1.png")
# pano 2
pano2 = im.crop((width*2, height, width*3, height*2)).save(timestamp + "/panorama_2.png","png")
log("saved cube face 2 at " + timestamp + "/panorama_2.png")
# pano 3
pano3 = im.crop((width*3, height, width*4, height*2)).save(timestamp + "/panorama_3.png","png")
log("saved cube face 3 at " + timestamp + "/panorama_3.png")
# pano 4
pano4 = im.crop((width, 0, width*2, height)).save(timestamp + "/panorama_4.png","png")
log("saved cube face 4 at " + timestamp + "/panorama_4.png")
# pano 5
pano5 = im.crop((width, height*2, width*2, height*3)).rotate(-90).save(timestamp + "/panorama_5.png","png")
log("saved cube face 5 at " + timestamp + "/panorama_5.png")
