
# python3

cool and epic:tm: collection of python 3 scripts i've made
### [frame_extractor.py](frame_extractor.py)
- Takes frames from a specified video file and saves them as images to a directory.
- Specify framerate, start time and a frame limit.

###  [img_converter.py](img_converter.py)
- Batch image converter from any format to one format (ex folder of png, bmp, jpg to jpg)
- Can specify compression quality of output format when appplicable.
- Origin folder can only contain images or else it breaks. might fix.

###  [pinger.py](pinger.py)
- Pings things. Windows only.

###  [wallpaper_changer.py](wallpaper_changer.py)
- Changes your Windows 10 (untested on 7,8) to a random image in a folder when idle for a specified time (default 20 seconds)
- No fade effect between two wallpapers, was too laggy for me
- Still lets Windows pick the accent color

###  [pyfetch.py](pyfetch.py)
- An implementation of neofetch in python for Windows systems.
- Currently requires either Powershell 5.1+ or [Powershell Core](https://github.com/PowerShell/PowerShell#-powershell) (because of the Get-ConputerInfo powershell command and use of ANSI color escape sequences)
- Incomplete

### [auto_img2ascii.py](auto_img2ascii.py)
- Takes an image file as input and outputs ascii art of it.
- No, its not done. Looks like hot garbage, i'll get around to it.

### [mc_advancement_list.py](mc_advancement_list.py)
- Create list of all advancements (excluding recipes) from a generated data dump from a Minecraft server jar
- Instructions to create data dump in file
- Made for updating a [shared advancements datapack](https://www.planetminecraft.com/data-pack/shared-advancements/) for 1.16.1

### [cuboid_panorama_splitter.py](cuboid_panorama_splitter.py)
- Splits a cuboid panorama generated by the [Fabrishot](https://github.com/ramidzkh/fabrishot) mod into a title screen compatible panorama
