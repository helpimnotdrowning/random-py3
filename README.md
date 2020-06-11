
# python3

cool and epic:tm: collection of python 3 scripts i've made
### [frame-extractor.py](frame-extractor.py)
- Takes frames from a specified video file and saves them as images to a directory.
- You can specify the framerate that they're extracted at.
###  [img-converter.py](img-converter.py)
- Batch image converter from any format to one format (ex folder of png, bmp, jpg to jpg)
- Can specify compression quality of output format when appplicable.
- Orgin folder can only contain images or else it breaks. might fix.
###  [pinger.py](pinger.py)
- Pings things. Windows only.
###  [wallpaper_changer.py](wallpaper_changer.py)
- Changes your Windows wallpaper to random wallpaper in specified folder when idle for specified time (default 20 seconds)
- This is because the default Windows wallpaper shuffle locks up the whole computer untill the fade effect finishes, and I didn't like it.
- No fade effect. But it doesn't lock up the system and still lets Windows pick the accent color automatically. michaelsoft pls fix 
###  [pyfetch.py](pyfetch.py)
- An implementation of neofetch in python for Windows systems.
- Currently requires either Powershell 5.1+ or [Powershell Core](https://github.com/PowerShell/PowerShell#-powershell) (because of the Get-ConputerInfo powershell command and use of ANSI color escape sequences)
- Incomplete
