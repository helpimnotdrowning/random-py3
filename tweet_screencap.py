import tweepy
import get_frame
import cv2
import schedule
import os
import time
import random
import datetime as dt

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
video = r"path/to/video/file.mkv"


# helper functions to make code prettier
def write_file(file, content):
    with open(file, 'w+') as file_:
        file_.write(str(content))
        
        
def read_file(file):
    with open(file, 'r') as file_:
        return file_.read()

# if its the first time running the bot (at least in current directory), make a "pick up" file,
# so in case the bot crashes, pc crashes, blackout, the bot can pick up where it left off

if not os.path.exists("pick_up_time.txt"):
    write_file("pick_up_time.txt", "0") # start at beginning of video
    
# read pickup file and set video time to it
sec = int(read_file("pick_up_time.txt"))
print("picking up at " + str(sec))


# main function
def job():
    # use as global to access the saved time
    # at least i think so, i haven't tried.
    global sec
    
    # save frame
    # currently will probably crash when it tries to go beyond the end of the video
    cv2.imwrite("tmp.png", get_frame.get_frame(video, sec)[1])
    
    # TODO: replace above with
    #
    # success, frame = get_frame.get_frame(video, sec)
    #     if success:
    #         send_the_tweet
    #     else if not_success:
    #         switch_to_next_video
    #
    # or something like that
    
    # upload frame to twitter, then get the media ID from that upload and tweet the image
    api.update_status(media_ids=[api.media_upload(filename="tmp.png").media_id_string])
    
    # delete the image locally
    os.remove("tmp.png")
    
    # go forwards 4-8 seconds in the video
    # its what the old bot did
    # change to  sec += 1  if you want to go every 1 second,  sec += 5  for 5 seconds, etc.
    sec += random.randrange(4,8)
    
    # save the time to the pick up file
    write_file("pick_up_time.txt", sec)
    
    # log that tweet has been sent to console
    print("frame at " + str(sec) + " sent at " + str(dt.datetime.now().time()))
    
    
# schedule tweet to be sent at XX:00 and XX:30 every hour
schedule.every().hour.at(":00").do(job)
schedule.every().hour.at(":30").do(job)

while True:
    # send tweet on schedule
    schedule.run_pending()
    # if it doesnt time.sleep it uses 100% CPU
    time.sleep(1)
    
