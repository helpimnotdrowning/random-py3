import re
import pyautogui as phk

from io import BytesIO
from numpy import asarray
from base64 import b64decode
from PIL.Image import open
from pyperclip import copy as to_clipboard
from pytesseract import image_to_string


# store images as base64 for ease of transport
# if you decide to run this on your computer, you will probably need to remake these,
# but idk how MPC-HC handles different resolutions and resizing stuff
find1 = b'iVBORw0KGgoAAAANSUhEUgAAABQAAAAJBAMAAADA7xF7AAAAKlBMVEUEBAT//wDAwMBCQkIcHBwWFhbMzMzX19eysrL///8zMzPx8fGAgACGhobhABxjAAAARElEQVR4nGNgEGAyZmBgUHEMBZJs5QwM5S0ODCDmTK1FuyFMjnKtRWBRGQGOu1qL7rY4HgSJgpkQBUjMDgaGDjATbi4ADyYV53Bwg2wAAAAASUVORK5CYII='
find2 = b'iVBORw0KGgoAAAANSUhEUgAAABQAAAAJBAMAAADA7xF7AAAAHlBMVEUAAAAEBAS/v7++vr59fQD+/v77+wDAwMCFhYX4+ADa1Qx6AAAAMklEQVR4nGNgAAFBIUMRAQYIU9UwAcosDzUUhDEjEMwOw5QJcCaSKIwpqGGYCGOCzAUAw1gJqN+0gBIAAAAASUVORK5CYII='


# base64 bytes to PIL Image
def b64_2_PIL_Image(b64):
    im_bytes = b64decode(b64)
    im_file = BytesIO(im_bytes)
    return open(im_file)
    
    
# fixes int strings like '003' -> '3' so python doesnt SyntaxError me
def fix_int(string):
    return str(int(string))
    
    
# finds MPC-HC timestamp in screen
def find_time():
    screenshot = phk.screenshot()
    
    fimg_coords = phk.locate('find.png', screenshot)
    
    if not fimg_coords:
        fimg_coords = phk.locate('find2.png', screenshot)
        
    if not fimg_coords:
        raise RuntimeError('Couldn\'t locate find.png on-screen. Make sure MPC-HC is open and the timestamp is visible.')
        
    time_img = screenshot.crop((fimg_coords[0]-175,fimg_coords[1]-6,fimg_coords[0]-6,fimg_coords[1] + fimg_coords[3]+6))
    
    return image_to_string(asarray(time_img), config="-c tessedit_char_whitelist=0123456789:.\/")
    
    
# fixes up timestamp to be directly pasted into tweet_screencap.py
def fix_time(time):
    # using DOTALL because sometimes tesseract will also send some extra characters on a newline, 
    # and I want to strip those out too
    stripped_time = re.sub('/.*','',time, flags=re.DOTALL)
    
    # if the regex fails, it return the string unchanged, so this comparison is perfectly valid
    if stripped_time == time:
        print(f'\n\n{time}\n\n')
        raise RuntimeError('Time could not be stripped.')
        
    # if the video is longer than an hour, MPC-HC will add a XX: to the start of the video elapsed time
    # it does not remove a XX: if the video is shorter than a minute, however.
    if re.fullmatch('(\d\d:){1}\d\d\.\d\d\d', stripped_time):
        fixed_time = ','.join(['0', fix_int(stripped_time[0:2]), fix_int(stripped_time[3:5]), fix_int(stripped_time[6:9])])
        
    elif re.fullmatch('(\d\d:){2}\d\d\.\d\d\d',stripped_time):
        fixed_time = ','.join([fix_int(stripped_time[0:2]), fix_int(stripped_time[3:5]), fix_int(stripped_time[6:8]), fix_int(stripped_time[9:12])])
        
    else:
        print(f'\n\n{stripped_time}\n\n')
        raise RuntimeError('Time could not be fixed.')
        
    # paste directly into tweet_screencap.py
    return f'''sec = time_to_seconds({fixed_time})
                elif sec == time_to_seconds({fixed_time}):
                    '''
    
    
if __name__ == '__main__':
    to_clipboard(fix_time(find_time()))
    
