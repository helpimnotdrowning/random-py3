# extracts individual frames from a video file to folder
import cv2
import datetime as dt
from pathlib import Path as path


def extractor():
    secs = 0  # Sets sec (the video time i think) to 0
    frameRate = .5  # frameRate = 1 / desired extracted frames per second
    count = 1

    vidPath = str(path(input("Full path to video file (with file extension):\n")))

    framePath = str(path(input("Output path for the frames:\n")))
    if not framePath.endswith("/"): framePath = framePath + "/"

    enableFrameLimit = input("Enable frame limit? (0 or 1)\n")
    try: 
        int(enableFrameLimit)
    except:
        enableFrameLimit = 0
    if enableFrameLimit == 1:
        frameLimit = input("Input frame limit:\n")
    vidCap = cv2.VideoCapture(vidPath)

    # I have no idea what this does but it works
    # thank you medium.com for letting me steal your code
    def get_frame(secs):
        vidCap.set(cv2.CAP_PROP_POS_MSEC, secs * 1000)
        hasFrames, image = vidCap.read()
        if hasFrames:
            o = str(dt.timedelta(seconds=secs))
            cv2.imwrite(framePath + "frame_" + str(count - 1) + "_@_time_" + o.replace(":", "'") + ".png", image)
        return hasFrames

    success = get_frame(secs)

    print("Operation started at " + str(dt.datetime.now().time()))

    while success:
        if enableFrameLimit == 1:
            if count >= int(frameLimit):  # If count is greater than or equal to frameLimit
                x = input("Final frame " + str(count - 1) + " exported at " + str(dt.datetime.now().time()) + "\npress ENTER to exit or ANY KEY and ENTER to go again...")
                if x != "": extractor()
                else: exit()
            else:
                count += 1  # Current frame + 1
                secs += frameRate  # Current time + frameRate
                secs = round(secs, 2)  # Rounds sec to 2nd decimal place
                success = get_frame(secs)
        else:
            count += 1  # Current frame + 1
            secs += frameRate  # Current time + frameRate
            secs = round(secs, 2)  # Rounds sec to 2nd decimal place
            success = get_frame(secs)
    y = input("Final frame " + str(count - 1) + " exported at " + str(dt.datetime.now().time()) + "\npress ENTER to exit or ANY KEY and ENTER to go again...")
    if y != "": extractor()
    else: exit()


extractor()
