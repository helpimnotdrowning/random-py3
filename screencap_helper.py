import re
import pyautogui as phk 

from numpy import asarray
from pyperclip import copy as to_clipboard
from pytesseract import image_to_string


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
        raise RuntimeError('Time could not be stripped.')
        
    check_time = re.fullmatch('(\d\d:){1,2}\d\d\.\d\d\d', stripped_time)
    
    # if the video is longer than an hour, MPC-HC will add a XX: to the start of the video elapsed time
    # it does not remove a XX: if the video is shorter than a minute, however.
    if re.fullmatch('(\d\d:){1}\d\d\.\d\d\d', stripped_time):
        fixed_time = ','.join(['0', fix_int(stripped_time[0:2]), fix_int(stripped_time[3:5]), fix_int(stripped_time[6:9])])
        
    elif re.fullmatch('(\d\d:){2}\d\d\.\d\d\d',stripped_time):
        fixed_time = ','.join([fix_int(stripped_time[0:2]), fix_int(stripped_time[3:5]), fix_int(stripped_time[6:8]), fix_int(stripped_time[9:12])])
        
    else:
        raise RuntimeError('Time could not be fixed.')
        
    # paste directly into tweet_screencap.py
    return f'''sec = time_to_seconds({fixed_time})
                elif sec == time_to_seconds({fixed_time}):
                    '''
    
    
if __name__ == '__main__':
    to_clipboard(fix_time(find_time()))
    
