# Converts images, self explanitory

from PIL import Image
from os import listdir
from pathlib import Path as path

lossyImgType = ("jpg", "jpeg", "tiff", "tif", "webp")
compressionQuality = 100
extension = input("What extension should be used? (do not include . )\n").lower()

if extension in lossyImgType: qualityInput = 1
else: qualityInput = 0

inputPath = str(path(input("Input path of the images:\n")))
if not inputPath.endswith("/"): inputPath = inputPath + "/"
fileDirList = listdir(inputPath)  # gets list of files in input directory

outputPath = str(path(input("Output path of the images:\n")))
if not outputPath.endswith("/"): outputPath = outputPath + "/"

if qualityInput == 1: compressionQuality = int(input("What should the compression quality be? (1-100)\n"))

for i in fileDirList:
    im = Image.open(inputPath + i)  # set im to the file contents
    im.convert('RGB').save(outputPath + i + "." + extension, quality=compressionQuality)  # saves image
    print("converted " + i + " to ." + extension + " in " + outputPath)
input("Done! Press ENTER to exit...\n")
