# if you have problems, make an issue here --> https://github.com/helpimnotdrowning/random-py3/issues/new <-- and ill try to help

# REQUIRES FFMPEG + FFPROBE IN PATH ( install instructions here --> https://video.stackexchange.com/a/20496 )
# IF YOU DONT HAVE FFMPEG INSTALLED IT WILL CRASH

# TODO: Add check to see if ffmpeg/ffprobe is installed

import os # check for pick up time
import cv2 # save frame temporarily
import sys
import tweepy # twitter api 
import logging
import schedule # schedule send tweets
try: # check if get_frame is downloaded
    import get_frame # get frame
except ModuleNotFoundError:
    raise ModuleNotFoundError('get_frame.py not in current directory. Download from https://github.com/helpimnotdrowning/random-py3/blob/master/get_frame.py')
import subprocess # use ffprobe to check video length

from time import sleep, strftime, gmtime # make cpu not explode, time formatting
from random import choices, random # for choosing how much time to proceed each frame
from socket import timeout # catch some errors hopefully

# setup tweepy auth
# get yer own keys
consumer_key = "0"
consumer_secret = "0"

access_token = "0"
access_token_secret = "0"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, timeout=120)

sec = 1
video_index = 0
season_index = 0

s1 = [
    'put/path_to/1st_video.here',
    'and_the/second_one.here',
    'and_just_keep/doing.that',
    'and_dont/put/a_comma_after_the/last.item'
]
s2 = [
    'you_can/also_make_another/set/season_after_the/last.one',
    'you_can_name_the_sets/whatever/you.like',
]

movie = [
    'just_remember_to/put_them_in_the_correct.order',
    r'and\for_windows_paths\with_the_other_slashes_you\need_to_have_an_r_before\the.quote'
]

# if they arent in correct order, it will mess up
series = [ s1, s2, movie ]

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
        
        
def read_image(file):
    return cv2.imread(file)
    
    
def delete_file(file):
    try:
        os.remove(file)
    except FileNotFoundError:
        pass
        
        
def time_to_seconds(hours=0, minutes=0, seconds=0, ms = 0):
    hour_in_minutes = hours * 60
    minutes += hour_in_minutes
    seconds += (minutes * 60) + (ms * .001)
    return float(seconds)
    
    
def seconds_to_time(seconds):
    seconds = float(seconds)
    return strftime("%H:%M:%S", gmtime(seconds)) + str(round(seconds % 1, 3))[1:]
    
    
def read_state():
    global sec
    global season_index
    global video_index
    
    # if its the first time running the bot (at least in current directory), make a "pick up" file,
    # so in case the bot crashes, pc crashes, blackout, the bot can pick up where it left off
    if not os.path.exists("pick_up_time.txt"):
        write_file("pick_up_time.txt", "1") # start at beginning of video
        
    if not os.path.exists('pick_up_video.txt'):
        write_file("pick_up_video.txt", '0') # start at first video
        
    if not os.path.exists('pick_up_season.txt'):
        write_file("pick_up_season.txt", "0") # start at first season
        
    _sec = read_file("pick_up_time.txt")
    
    # check if pick_up_time.txt is a tuple, if it is separate the 4 numbers expected into a list
    if str(_sec).startswith('('):
        time_split = str(_sec).replace('(','').replace(')','').split(',')
        
        # convert them all to numbers
        for i in range(len(time_split)):
            time_split[i] = int(time_split[i])
            
        # set sec to that
        sec = float(time_to_seconds(time_split[0], time_split[1], time_split[2], time_split[3]))
    
    # else, if its just a normal number like what this script saves, dont do funny stuff with it
    else:
        sec = float(_sec)
        
    season_index = int(read_file("pick_up_season.txt"))
    video_index = int(read_file("pick_up_video.txt"))
    
    logger.debug('Picking up at season %s, video %s at %s (%s)', season_index + 1, video_index + 1, seconds_to_time(sec), sec)
    
    
def save_state():
    logger.debug('Saving state...')
    
    if dont_save == True:
        logger.debug('State not saved.')
    else:
        write_file("pick_up_time.txt", sec)
        write_file("pick_up_video.txt", video_index)
        write_file("pick_up_season.txt", season_index)
    
    
def reset_state():
    logger.warning('Clearing state...')
    delete_file("pick_up_time.txt")
    delete_file("pick_up_video.txt")
    delete_file("pick_up_season.txt")


# upload image to twitter, keep retrying untill success
#@tenacity.retry
def upload_image_to_twitter(path):
    logger.debug('Uploading image to Twitter...')
    
    if api == None:
        cv2.imwrite('upload.png', read_image(path))
        return 0
    else:
        logger.warning('ACTUALLY UPLOADING FOR REAL THIS TIME!!!!')
        try:
            return api.media_upload(filename=path).media_id_string
        except timeout:
            raise timeout('Timed out.')
        
# send tweet, keep retrying untill success
#@tenacity.retry
def send_tweet_with_media(media_id):
    logger.debug('Sending Tweet...')
    
    if api == None:
        logger.info('Tweet would have been sent here.')
    else:
        try:
            api.update_status(media_ids=[media_id])
        except timeout:
            raise timeout('Timed out.')
    
    
# send tweet, keep retrying untill success
#@tenacity.retry
def send_tweet_with_text(status_text):
    logger.debug('Sending Tweet...')
    
    if api == None:
        logger.info('Tweet would have been sent here.')
    else:
        try:
            api.update_status(status=str(status_text))
        except timeout:
            raise timeout('Timed out.')
        #except tweepy.error.TweepError as e:
            #if e.api_code == '
            
            
def randrange_OLD():
    seq = [ 1, 2, 3, 4, 5, 6]
    wgt = [18,22,23,13,12,10]
    rand_choice = choices(seq, weights = wgt)
    return rand_choice[0]
    
    
def randrange():
    seq = [1,  2,  3,  4,  5 ]
    wgt = [14, 28, 28, 20, 10]
    #wgt = [16,42,42] 
    #wgt = [12,28,28,28] # out of 100
    rand_choice = choices(seq, weights = wgt)
    # choices returns a list
    return rand_choice[0] + round(random(), 2) # tack on some milliseconds so it cant only send frames on the 0
    
    
# https://stackoverflow.com/a/3844467
def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)
    
    
# TODO: WHY DOES THIS WORK SO WELL?????
def get_video():
    global sec
    global video_index
    global season_index
    
    # try to set season, if more seasons than exist (series over), exit
    try:
        season = series[season_index]
    except IndexError:
        exit()
    
    # try to set video, if more videos than exist (season over), go to next season and reset video to 0
    try:
        video = season[video_index]
    except IndexError:
        season_index += 1
        video_index = 0
        video = get_video()
    
    return video
    
    
def next_video_please():
    global video_index
    global sec
    
    video_index += 1
    sec = 0
    logger.info("Episode over, switching to next.")
    
    
# main function
def tweet_frame():
    global sec
    global video
    global season_index
    global video_index
    
    video = get_video()
    vid_length = get_length(video)
    
    if sec <= vid_length:
    
        time_string = f'frame {seconds_to_time(sec)} ({str(sec)}) from season {str(season_index + 1)}, video {str(video_index + 1)}'
        
        # get frame from video
        logger.info('Extracting frame at %s (%s)...', seconds_to_time(sec), str(sec))
        success, frame = get_frame.get_frame(video, sec)
        
        logger.debug('sec of %s is less than or equal to length %s', str(sec), str(vid_length))
        
        if success:
            cv2.imwrite("tmp.png", frame)
            
            # upload frame to twitter, then get the media ID from that
            image_id = upload_image_to_twitter("tmp.png")
            
            # tweet the image
            send_tweet_with_media(image_id)
            logger.info('Tweet sent with %s', time_string)
            
            delete_file("tmp.png")
            
            # go forward for next frame
            sec += randrange()
            
            time_string = f'frame {seconds_to_time(sec)} ({str(sec)}) from season {str(season_index + 1)}, video {str(video_index + 1)}'
            
            save_state()
            
            if sec > vid_length:
                logger.info('Next run should switch to next episode, sec %s is greater than video length %s', str(sec), str(vid_length))
            else:
                logger.info('Next frame will be %s', time_string)
                
        else:
            if sec >= (vid_length - 1.5):
                next_video_please()
            else:
                raise RuntimeError("Failed to extract frame at {sec}, Dont know how to deal with this.")
                
    else:
        video_index += 1
        sec = 0
        logger.warning("Episode over, switching.")
        #exit()
    sleep(1)
    
    
if __name__ == '__main__':
    print(sys.argv)
    
    read_state()
    
    if '-test' in sys.argv:
        api = None
        dont_save = True
        logger.warning('Starting in test mode.')
        
    if '-reset' in sys.argv:
        if '-test' in sys.argv:
            logger.warning('State not cleared. Exiting anyway.')
            exit()
            
        elif '-y' in sys.argv:
            reset_state()
            
        else:
            ask_reset = input('Reset state and start over at video 0? This cannot be undone. (y/n) : ')
            if ask_reset.lower() == 'y':
                reset_state()
                
            else:
                logger.warning('State not cleared. Exiting anyway.')
                exit()
            
    if '-tweet_now' in sys.argv:
        if '-test' in sys.argv:
            tweet_frame()
            
        else:
            ask_tweet = input('Send tweet now? (y/n) : ')
            if ask_tweet.lower() == 'y':
                tweet_frame()
                
            else:
                logger.info('Tweet not sent. Starting normally.')
        
    schedule.every().hour.at(":00").do(tweet_frame)
    schedule.every().hour.at(":30").do(tweet_frame)
    
    while True:
        schedule.run_pending()
        sleep(1)
        
