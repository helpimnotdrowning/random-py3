# extracts individual frames from a video file to folder
import cv2
import datetime as dt
from pathlib import Path as path


def extractor(video_filepath, frame_output_path, start_time = 0, fps = 2, frame_limit = -1):
    frame_rate = 1 / fps
    
    count = 1
    time_counter = start_time

    video_filepath = str(path(video_filepath))
    
    frame_output_path = str(path(frame_output_path)) + '/'
    
    if int(frame_limit) > 0:
        enable_frame_limit = True
    else:
        enable_frame_limit = False

    vidCap = cv2.VideoCapture(video_filepath)

    # I have no idea what this does but it works
    # thank you medium.com for letting me steal your code
    def get_frame(time_counter):
        vidCap.set(cv2.CAP_PROP_POS_MSEC, time_counter * 1000)
        has_frames, image = vidCap.read()
        if has_frames:
            o = str(dt.timedelta(seconds=time_counter))
            cv2.imwrite(frame_output_path + "frame_" + str(count) + "_@_time_" + o.replace(":", "'") + ".png", image)
        return has_frames

    success = get_frame(time_counter)

    print("Operation started at " + str(dt.datetime.now().time()))

    while success:
        if enable_frame_limit == True:
            # if count is greater than/equal to $frame_limit
            if count >= int(frame_limit):
                exit_intent = input("Final frame {0} exported at {1}\npress ENTER to exit or ANY KEY and ENTER to go again...".format(str(count), str(dt.datetime.now().time())))
                 # if any key was pressed to restart
                if exit_intent != "":
                    extractor()  # BROKEN RN THIS WONT WORK LMAO
                else:
                    exit()
                    
            # normal operation
            elif count < int(frame_limit):
                #
                count += 1
                # go to next time of frame
                time_counter += frame_rate
                # round time to hundreths place, no weird decimals here
                time_counter = round(time_counter, 2)
                success = get_frame(time_counter)
                
        # normal operation when no frame limit
        elif enable_frame_limit == False:  
            count += 1
            # go to next time of frame
            time_counter += frame_rate
            # round time to hundreths place, no weird decimals here
            time_counter = round(time_counter, 2)
            success = get_frame(time_counter)
            
    exit_intent = input("Final frame {0} exported at {1}\npress ENTER to exit or ANY KEY and ENTER to go again...".format(str(count), str(dt.datetime.now().time())))
    # if any key was pressed to restart
    if exit_intent != "":
        extractor()  # BROKEN RN THIS WONT WORK LMAO
    else:
        exit()
        

target_video_path = input('Target video path : ')
outpur_frames_path = input('Output frames path : ')

custom_frame_rate = input('Input custom frames/second (empty for 2) : ')
custom_frame_rate = custom_frame_rate if custom_frame_rate != '' else 2

custom_start_time = input('Input custom start time (empty for 0)    : ')
custom_start_time = custom_start_time if custom_start_time != '' else 0

custom_frame_limit = input('Input custom frame limit (empty for none): ')
custom_frame_limit = custom_frame_limit if custom_frame_limit != '' else -1

extractor(target_video_path, outpur_frames_path, float(custom_start_time), float(custom_frame_rate), int(custom_frame_limit))
