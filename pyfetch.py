import platform
import getpass
import winreg
import psutil
import re
import subprocess as sp
from datetime import datetime
from winreg import ConnectRegistry, OpenKey, QueryValueEx


def RGB2ANSI(red=0, green=0, blue=0, isBG=0):
    if isBG == 0:
        ansiColor = "\033[38;2;{};{};{}m".format(red, green, blue)
    else:
        ansiColor = "\033[48;2;{};{};{}m".format(red, green, blue)
    return ansiColor


class ANSICol:
    # special codes
    reset = '\033[0m'
    invert = '\033[7m'
    # basic colors
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    yellow = '\033[33m'
    blue = '\033[34m'
    magenta = '\033[35m'
    cyan = '\033[36m'
    white = '\033[37m'
    # extended colors
    lblack = '\033[90m'
    lred = '\033[91m'
    lgreen = '\033[92m'
    lyellow = '\033[93m'
    lblue = '\033[94m'
    lmagenta = '\033[95m'
    lcyan = '\033[96m'
    lwhite = '\033[97m'
    # custom
    wred = RGB2ANSI(255, 87, 34)
    wgreen = RGB2ANSI(124, 179, 66)
    wblue = RGB2ANSI(3, 169, 244)
    wyellow = RGB2ANSI(255, 193, 7)


col = ANSICol

user = getpass.getuser()  # (hopefully) your username
machineName = platform.node().upper()  # the machine host name

pcinfo = sp.Popen('''pwsh -c 
"$gci = Get-ComputerInfo

$gci.WindowsBuildLabEx
$gci.WindowsVersion
$gci.OsName"''', stdout = sp.PIPE).communicate()[0].decode('utf-8').splitlines()

OSVer = pcinfo[2] + ' release ' + pcinfo[1]

key = OpenKey(ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE), r'SOFTWARE\Microsoft\Windows NT\CurrentVersion')
OSBuild = QueryValueEx(key, 'ReleaseId')[0]  # get OS version, NOT the build number

key = OpenKey(ConnectRegistry(None, winreg.HKEY_CURRENT_USER), r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Accent')
accentCol = hex(QueryValueEx(key, 'StartColorMenu')[0])[4:]  # gets and reads accent color, converts to hex and cuts off
                                                             #    '0x' at the start of value
# these next three lines get the 2 bytes of each color channel and converts them from hex (base 16, numbers 0-F) to an
#   int (base 10, numbers 0-9), then is passed to RGB2ANSI() create a custom ANSI color code based on the current
#   windows accent color.
# am doing it like this because windows is [REDACTED] and saves the accent color in BBGGRR format instead of RRGGBB
accentColB = int(accentCol[0:2], 16)
accentColG = int(accentCol[2:4], 16)
accentColR = int(accentCol[4:6], 16)

accentColANSI = RGB2ANSI(accentColR, accentColG, accentColB)
accentColInvANSI = RGB2ANSI(255 - accentColR, 255 - accentColG, 255 - accentColB)

print('''
{r}        ,.=:!!t3Z3z.,                  {FG}{TIME}{x}
{r}       :tt:::tt333EE3                  {FG}{USR}{w}@{FG}{MNAME}{x}
{r}       Et:::ztt33EEEL {g}@Ee.,      ..,   {FG}{DASHES}{x}
{r}      ;tt:::tt333EE7 {g};EEEEEEttttt33#   {FG}OS: {OS}{x}
{r}     :Et:::zt333EEQ. {g}$EEEEEttttt33QL   
{r}     it::::tt333EEF {g}@EEEEEEttttt33F 
{r}    ;3=*^```"*4EEV {g}:EEEEEEttttt33@. 
{b}    ,.=::::!t=., {r}` {g}@EEEEEEtttz33QF  
{b}   ;::::::::zt33)   {g}"4EEEtttji3P*   
{b}  :t::::::::tt33 {y}:Z3z..  {g}``{y} ,..g.   
{b}  i::::::::zt33F {y}AEEEtttt::::ztF    
{b} ;:::::::::t33V {y};EEEttttt::::t3     
{b} E::::::::zt33L {y}@EEEtttt::::z3F     
{b}{{3=*^```"*4E3) {y};EEEtttt:::::tZ`     
{b}             ` {y}:EEEEtttt::::z7      
{y}                 "VEzjt:;;z>*`{x}     '''.format(
    x=col.reset,
    r=col.wred,
    g=col.wgreen,
    b=col.wblue,
    y=col.wyellow,
    w=col.white,
    IN=col.invert,
    FG=accentColInvANSI,
    BG=accentColInvANSI,
    TIME=datetime.now().strftime("%H:%M:%S"),
    USR=user,
    MNAME=machineName,
    DASHES='-' * (len(user + machineName) + 1),
    OS=OSVer,
    ))
    
print(accentColR,accentColG,accentColB)
print(255 - accentColR, 255 - accentColG, 255 - accentColB)
print(pcinfo)
