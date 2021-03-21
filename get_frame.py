# extract a frame from video and return that
import cv2
from pathlib import Path as path

# time should be in seconds, ex 13:21 -> 801
# you can use seconds.milliseconds too, ex 6:46.72 -> 406.72
def get_frame(video_filepath, time):
    # nornalize $video_filepath to avoid weird errors 
    video_filepath = str(path(video_filepath))
    # set $vidCap to video file contents
    vidCap = cv2.VideoCapture(video_filepath)
    
    # set video to $time 
    vidCap.set(cv2.CAP_PROP_POS_MSEC, time * 1000)
    
    # return tuple of (success value: bool, image: numpy nth dim. array)
    # 1st value will be True if the frame exists, and False if it doesn't ($time passed is passed the end of the video)
    # 2nd value can be saved as an image using something like cv2.imwrite("image.png", get_frame.get_frame(video_file_path, time_in_seconds)[1]),
    #                                          call to save image ^       ^ file name  ^ call to get_frame()        get second part of tuple ^ 
    return vidCap.read()
