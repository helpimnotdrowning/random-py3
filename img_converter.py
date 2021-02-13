from PIL import Image
from os import listdir
from pathlib import Path as path

lossy_image_formats = ("jpg", "jpeg", "tiff", "tif", "webp")
lossy_compression_quality = 100
new_file_extension = input("What extension should be used? (do not include . ) : ").lower()

if new_file_extension in lossy_image_formats:
    ask_compression_quality = True
else:
    ask_compression_quality = False

input_path = str(path(input("Input path of the images : ")))
if not input_path.endswith("/"):
    input_path = input_path + "/"
# get list of files in $input_path
file_list = listdir(input_path)

output_path = str(path(input("Output path of the images : ")))
if not output_path.endswith("/"):
    output_path = output_path + "/"

if ask_compression_quality == True:
    lossy_compression_quality = int(input("What should the compression quality be? (1-100) : "))

for i in file_list:
    # open image
    im = Image.open(input_path + i)
    # save image
    im.convert('RGB').save(output_path + i + "." + new_file_extension, quality=lossy_compression_quality)
    print("converted " + i + " to ." + new_file_extension + " in " + output_path)
    
input("Done! Press ENTER to exit...\n")
