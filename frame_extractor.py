# extracts individual frames from a video file to folder
import cv2
import datetime as dt
from pathlib import Path as path


def extractor(videoFilepath, frameOutputPath, startTime = 0, FPS = 2, frameLimit = -1):
    frameRate = 1 / FPS
    
    count = 1
    timeCounter = startTime

    videoFilepath = str(path(videoFilepath))
    
    frameOutputPath = str(path(frameOutputPath)) + '/'
    
    if int(frameLimit) > 0:
        enableFrameLimit = True
    else:
        enableFrameLimit = False

    vidCap = cv2.VideoCapture(videoFilepath)

    # I have no idea what this does but it works
    # thank you medium.com for letting me steal your code
    def get_frame(timeCounter):
        vidCap.set(cv2.CAP_PROP_POS_MSEC, timeCounter * 1000)
        hasFrames, image = vidCap.read()
        if hasFrames:
            o = str(dt.timedelta(seconds=timeCounter))
            cv2.imwrite(frameOutputPath + "frame_" + str(count) + "_@_time_" + o.replace(":", "'") + ".png", image)
        return hasFrames

    success = get_frame(timeCounter)

    print("Operation started at " + str(dt.datetime.now().time()))

    while success:
        if enableFrameLimit == True:
            if count >= int(frameLimit):  # If count is greater than or equal to frameLimit
                exitIntent = input("Final frame {0} exported at {1}\npress ENTER to exit or ANY KEY and ENTER to go again...".format(str(count), str(dt.datetime.now().time())))
                if exitIntent != "":  # if any key was pressed to restart
                    extractor()  # BROKEN RN THIS WONT WORK LMAO
                else:
                    exit()
            elif count < int(frameLimit):  # normal operation
                count += 1  # Current frame + 1
                timeCounter += frameRate  # Current time + frameRate
                timeCounter = round(timeCounter, 2)  # Rounds sec to 2nd decimal place
                success = get_frame(timeCounter)
                
        elif enableFrameLimit == False:  # normal operation when no frame limit
            count += 1  # Current frame + 1
            timeCounter += frameRate  # Current time + frameRate
            timeCounter = round(timeCounter, 2)  # Rounds sec to 2nd decimal place
            success = get_frame(timeCounter)
    exitIntent = input("Final frame {0} exported at {1}\npress ENTER to exit or ANY KEY and ENTER to go again...".format(str(count), str(dt.datetime.now().time())))
    if exitIntent != "":  # if any key was pressed to restart
        extractor()  # BROKEN RN THIS WONT WORK LMAO
    else:
        exit()
        

targetVideoPath = input('Target video path : ')
outputFramesPath = input('Output frames path : ')
customFrameRate = 2
customStartTime = 0
customFrameLimit = -1

customFrameRate = input('Input custom frames/second (empty for 2) : ')

customStartTime = input('Input custom start time (empty for 0)    : ')
    
customFrameLimit = input('Input custom frame limit (empty for none): ')

extractor(targetVideoPath, outputFramesPath, float(customStartTime), float(customFrameRate), int(customFrameLimit))
