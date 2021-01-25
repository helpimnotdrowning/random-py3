# Changes Windows wallpaper on startup/login and once idle for more than $idle_wait_time seconds
# Change extension to .pyw and place in %userprofile%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\

from ctypes import Structure, windll, c_uint, sizeof, byref
import time
import random
import glob

# idle time to wait to change wallpapers in seconds
idle_wait_time = 5

# file to save full path to wallpaper (not image itself)
wallpaper_path_save = r"C:\Users\Admin2\landing\currentWallpaper.txt"

# root folder holding all files (will search recursivley)
wallpaper_root_dir = r"C:\Users\User\Pictures\\"

# dont change these
wallpaper_full_path = ""
valid_image_types = ("png", "bmp", "jpg", "jpeg", "tiff", "tif")
all_wallpapers = []
allow_wallpaper_change = 0


# set wallpaper so it doesnt look complicated in random_wallpaper()
def set_wallpaper(file):
    SPIF_UPDATEINIFILE = 0x2
    SPI_SETDESKWALLPAPER = 0x14
    windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, file, SPIF_UPDATEINIFILE)


def refresh_wallpapers():
    global all_wallpapers
    all_wallpapers = []
    
    # for every supported filetype
    for file_type in valid_image_types:
        # create wildcard to select images of that filetype
        file_wildcard = '**/*.' + file_type
        
        # find and add it to $all_wallpapers
        # ty https://stackoverflow.com/a/45172387 <3
        all_wallpapers.extend(glob.iglob(wallpaper_root_dir + file_wildcard, recursive=True))
    print("Refreshed wallpaper list.")


def random_wallpaper():
    global wallpaper_full_path, allow_wallpaper_change, wallpaper_path_save
    
    # choose random wallpaper
    wallpaper_full_path = random.choice(all_wallpapers)
    
    set_wallpaper(wallpaper_full_path)
    
    # mark as changed so it doesnt change on loop
    allow_wallpaper_change = 1
    
    # save image path if wallpaper_path_save is set
    if wallpaper_path_save != '': 
        with open(wallpaper_path_save, 'w') as f:
            f.write(str(wallpaper_full_path))
       
    print("Wallpaper set to " + wallpaper_full_path)


# from https://stackoverflow.com/a/30018577
class LASTINPUTINFO(Structure):
    _fields_ = [
        ('cbSize', c_uint),
        ('dwTime', c_uint)
    ]


# also from https://stackoverflow.com/a/30018577
def get_idle_duration():
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = sizeof(lastInputInfo)
    windll.user32.GetLastInputInfo(byref(lastInputInfo))
    millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
    return millis / 1000.0


if __name__ == '__main__':
    # set wallpaper on login
    refresh_wallpapers()
    random_wallpaper()

    while True:
        print("idle for " + str(get_idle_duration()))
        
        # if it doesnt sleep it uses 100% CPU
        time.sleep(1)
        
        # if the wallpaper has been changed AND the user is not idle anymore (used within last 2 seconds)
        if allow_wallpaper_change == 1 and get_idle_duration() <= 2:
            # mark as wallpaper unchanged and allow to change again
            allow_wallpaper_change = 0
            
        # if the wallpaper is allowed to be reset AND the user is idle longer than $idle_wait_time seconds
        elif allow_wallpaper_change == 0 and get_idle_duration() >= idle_wait_time:
            # refresh and reset
            refresh_wallpapers()
            random_wallpaper()
