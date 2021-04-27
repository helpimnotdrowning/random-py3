# REQUIRES FFMPEG + FFPROBE IN PATH ( install instructions here --> https://video.stackexchange.com/a/20496 )
# IF YOU DONT HAVE FFMPEG INSTALLED IT WILL CRASH

# TODO: Add check to see if ffmpeg/ffprobe is installed

# extract a frame from video and return that
import cv2
import subprocess
from pathlib import Path as path # path formatting
from time import strftime, gmtime # time formatting
from os import remove as osremove


def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)
    
    
def seconds_to_time(seconds):
    return strftime("%H:%M:%S", gmtime(seconds)) + str(round(seconds % 1, 3))[1:]
    
    
# time should be in seconds, ex 13:21 -> 801
# you can use seconds.milliseconds too, ex 6:46.72 -> 406.72
def get_frame(video_filepath, time):
    # nornalize $video_filepath to avoid weird errors 
    video_filepath = str(path(video_filepath))
    
    # make sure $time is actually within the video
    if time > get_length(video_filepath):
        return (False, None)
    if time < 0:
        return (False, None)
        
    # use ffmpeg, this might seem like a weird descision, but i have a perfectly valid reason
    # using cv2 shifts the colors a bit so it looks different (i think it might be a limited vs full rgb thing but idk)
    # using ffmpeg makes the colors completley accurate, and only adds 0.1~ seconds to execution time
    result = subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', seconds_to_time(time), '-i', video_filepath, '-vframes', '1', 'tmpframe.png'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
        
    img = cv2.imread('tmpframe.png')
    osremove('tmpframe.png')
    
    # return tuple of (success value: bool, image: numpy nth dim. array)
    # save image using cv2.imwrite('image.png', get_frame.get_frame(...)[1])
    # this return a tuple still because i dont want to change other code
    return (True, img)
    
