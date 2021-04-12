# REQUIRES FFMPEG + FFPROBE IN PATH ( install instructions here --> https://video.stackexchange.com/a/20496 )
# IF YOU DONT HAVE FFMPEG INSTALLED IT WILL CRASH

# TODO: Add check to see if ffmpeg/ffprobe is installed

import os # check for pick up time
import cv2 # save frame temporarily
import tweepy # twitter api 
import logging
import schedule # schedule send tweets
import tenacity # easy retry uploading image/sending tweet incase of bad internet
try: # check if get_frame is downloaded
    import get_frame # get frame
except ModuleNotFoundError:
    print('get_frame.py not in current directory. Download from https://github.com/helpimnotdrowning/random-py3/blob/master/get_frame.py')
    exit()
import subprocess # use ffprobe to check video length

from time import sleep, strftime, gmtime # make cpu not explode, time formatting
from random import choices # for choosing how much time to proceed each frame

# setup tweepy auth
# get yer own keys
consumer_key = "0"
consumer_secret = "0"

access_token = "0"
access_token_secret = "0"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# will make so it swiches to the next video automatically later*.
video = r"path/to/video.file"

# setup logging
logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(logging.Formatter('[%(asctime)s.%(msecs)03d] [%(name)s/%(levelname)s]: %(message)s', '%H:%M:%S'))
logger.addHandler(ch)


# helper functions to make code prettier
def write_file(file, content):
    with open(file, 'w+') as file_:
        file_.write(str(content))
        
        
def read_file(file):
    with open(file, 'r') as file_:
        return file_.read()
        
        
def seconds_to_time(seconds):
    return strftime("%H:%M:%S", gmtime(seconds))
    
    
# if its the first time running the bot (at least in current directory), make a "pick up" file,
# so in case the bot crashes, pc crashes, blackout, the bot can pick up where it left off

if not os.path.exists("pick_up_time.txt"):
    write_file("pick_up_time.txt", "0") # start at beginning of video
    
# read pickup file and set video time to it
sec = int(read_file("pick_up_time.txt"))
logger.info('Next frame will be %s (%s)', seconds_to_time(sec), str(sec))


# upload image to twitter, keep retrying untill success
@tenacity.retry
def upload_image_to_twitter(path):
    return api.media_upload(filename=path).media_id_string
    

# send tweet, keep retrying untill success
@tenacity.retry
def send_tweet(media_id):
    api.update_status(media_ids=[media_id])
    
    
# https://stackoverflow.com/a/3844467
def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)
    
    
# main function
def job():
    # use as global to access the saved time
    # at least i think so, i haven't tried.
    global sec
    
    # get frame from video
    logger.info('Extracting frame at %s (%s)...', seconds_to_time(sec), str(sec))
    success, frame = get_frame.get_frame(video, sec)
    logger.info('Extracted.')
    
    if sec <= get_length(video):
        if success:
            # save frame
            cv2.imwrite("tmp.png", frame)
            
            # upload frame to twitter, then get the media ID from that
            logger.info('Uploading image to Twitter...')
            image_id = upload_image_to_twitter("tmp.png")
            logger.info('Uploaded.')
            
            # tweet the image
            logger.info('Sending Tweet...')
            send_tweet(image_id)
            logger.info('Sent.')
            
            # log that tweet has been sent to console
            logger.info('Tweet sent with frame %s (%s)', seconds_to_time(sec), str(sec))
            
            # delete the image locally
            os.remove("tmp.png")
            
            # go forwards 4-8 seconds in the video
            # the current bot has a different range
            # change to  sec += 1  if you want to go every 1 second,  sec += 5  for 5 seconds, etc.
            sec += randrange(4, 8)
            
            # save the time to the pick up file
            write_file("pick_up_time.txt", sec)
            
            logger.info('Next frame will be %s (%s)', seconds_to_time(sec), str(sec))
        else:
            logger.critical('VIDEO FAILED TO DECODE!!!')
    else:
        # self descriptive
        # replace recipient ID with your own twitter ID
        api.send_direct_message(recipient_id=0, text='HEY DUMBASS THE EPISODE ENDED AND AUTO EPISODE SWITCHING HASNT BEEN ADDED')
        logger.critical("THE EPISODE IS OVER AND THERE ISNT AUTO EPISODE SWITCHING")
        logger.critical("THAT MESSAGE SHOULD NEVER HAVE BEEN PRINTED. MAKE AN ISSUE AT https://github.com/helpimnotdrowning/random-py3/issues !!!!!")
        logger.critical('exiting so it doesnt loop the episode')
        exit()
    
# schedule tweet to be sent at XX:00 and XX:30 every hour
schedule.every().hour.at(":00").do(job)
schedule.every().hour.at(":30").do(job)

while True:
    # send tweet on schedule
    schedule.run_pending()
    # if it doesnt time.sleep it uses 100% CPU
    sleep(1)
    
