# Changes Windows wallpaper on startup/login and once idle for more than 'waitTime' seconds
# Change extension to .pyw and place in %userprofile%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\

from ctypes import Structure, windll, c_uint, sizeof, byref
import time
import random
import glob

# dont change these
file = ""
imgTypes = ("png", "bmp", "jpg", "jpeg", "tiff", "tif")
wallpaperPathAll = []
SPIF_UPDATEINIFILE = 0x2  # even do
SPI_SETDESKWALLPAPER = 0x14  # what does this
wallpaperAlreadyChanged = 0
wallpaperChangesCounter = 0

# you can change these 
waitTime = 15  # idle time to wait to change wallpapers
wallpaperPathSave = r"C:\Users\Admin2\landing\currentWallpaper.txt"  # place to save full path of wallpaper as text
                                                                     #     if you want to. i want to.
                                                                     #     set empty if you dont want/need this
wallpaperPathList = [  # put your wallpaper paths in here
    r"C:\Users\User\Pictures\\",  # first example
    r"C:\Users\Admin\Desktop\Wallpapers\\",  # second example
    r"C:\Users\Dave3\Downloads\wallpapers-march2020\\"  # last example
]


def refreshwallpapers():
    global wallpaperPathAll, wallpaperChangesCounter
    wallpaperPathAll = []
    for i in range(len(wallpaperPathList)):  # for every item in wallpaperPathList,
        for j in imgTypes:  # for each image format in imgTypes,
            wallpaperPathAll.extend(glob.glob(wallpaperPathList[i].lower() + "*." + j))  # add image path to list of
            # images. this avoids black wallpapers by filtering out invalid file types
    print("Refreshed wallpaper list.")


def randwallpaper():
    global file, wallpaperAlreadyChanged, wallpaperPathSave, wallpaperChangesCounter
    if wallpaperChangesCounter >= 5:
        wallpaperChangesCounter = 0 ;  refreshwallpapers()  # gets all wallpapers
    file = random.choice(wallpaperPathAll)
    windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, str(file), SPIF_UPDATEINIFILE)
    wallpaperAlreadyChanged = 1
    if wallpaperPathSave != '': 
        Z = open(wallpaperPathSave, 'w') ; Z.write(str(file)) ; Z.close()
    print("Wallpaper set to " + file)


# from https://stackoverflow.com/a/30018577
class LASTINPUTINFO(Structure):
    _fields_ = [
        ('cbSize', c_uint),
        ('dwTime', c_uint),
    ]


# also from https://stackoverflow.com/a/30018577
def get_idle_duration():
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = sizeof(lastInputInfo)
    windll.user32.GetLastInputInfo(byref(lastInputInfo))
    millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
    return millis / 1000.0


refreshwallpapers()
randwallpaper()  # runs when started

while True:  # timer to change when idle for 'waitTime' seconds
    print("idle for " + str(get_idle_duration()))
    time.sleep(1)  # here so script doesnt use 30% cpu
    # if the wallpaper has been changed AND the mouse / keyboard has been used in last 3 seconds
    if wallpaperAlreadyChanged == 1 and get_idle_duration() <= 2:
        wallpaperAlreadyChanged = 0  # resets wallpaper status
    # if the wallpaper hasn't been changed or been reset AND the kb / mouse hasn't been use in 'timer' seconds
    elif wallpaperAlreadyChanged == 0 and get_idle_duration() >= waitTime:
        randwallpaper()  # set random wallpaper
