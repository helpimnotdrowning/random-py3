import platform
import getpass
import winreg
import subprocess as sp
from datetime import datetime
from winreg import ConnectRegistry, OpenKey, QueryValueEx


def GetWinRegKeyValue(HKEYS, key, value):
    HANDLES = {"CLASSES_ROOT": winreg.HKEY_CLASSES_ROOT,
               "CURRENT_USER": winreg.HKEY_CURRENT_USER,
               "LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
               "USERS": winreg.HKEY_USERS,
               "PERFORMANCE_DATA": winreg.HKEY_PERFORMANCE_DATA,
               "CURRENT_CONFIG": winreg.HKEY_CURRENT_CONFIG
               }
    key = key.replace('/', '\\')
    return QueryValueEx(OpenKey(ConnectRegistry(None, HANDLES[HKEYS]), key), value)


def RGB2ANSI(red=0, green=0, blue=0, isBG=0):
    if isBG == 0:
        ansiColor = "\033[38;2;{};{};{}m".format(red, green, blue)
    else:
        ansiColor = "\033[48;2;{};{};{}m".format(red, green, blue)
    return ansiColor


class ANSIColors:
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
    winRed = RGB2ANSI(255, 87, 34)
    winGreen = RGB2ANSI(124, 179, 66)
    winBlue = RGB2ANSI(3, 169, 244)
    winYellow = RGB2ANSI(255, 193, 7)


user = getpass.getuser()  # (hopefully) your username
machineName = platform.node().upper()  # the machine host name

pcInfo = sp.Popen('''pwsh -c 
"$gci = Get-ComputerInfo

$gci.WindowsBuildLabEx
$gci.WindowsVersion
$gci.OsName"''', stdout=sp.PIPE).communicate()[0].decode('utf-8').splitlines()

OSVer = pcInfo[2] + ' v' + pcInfo[1]

# get OS version, NOT the build number
OSBuild = GetWinRegKeyValue("LOCAL_MACHINE", 'SOFTWARE/Microsoft/Windows NT/CurrentVersion', 'ReleaseId')[0]

# gets and reads accent color, converts to hex and cuts off '0x' at the start of value
accentCol = hex(GetWinRegKeyValue("CURRENT_USER", 'SOFTWARE/Microsoft/Windows/CurrentVersion/Explorer/Accent', 'StartColorMenu')[0])[4:]

# get the 2 bytes of each color channel and converts them from hex to int
accentColB = int(accentCol[0:2], 16)
accentColG = int(accentCol[2:4], 16)
accentColR = int(accentCol[4:6], 16)

# pas to to RGB2ANSI() and create a custom ANSI color code based on the current windows accent color.
# doing it like this because windows is [REDACTED] and saves the accent color in BGR format instead of RGB
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
    x=ANSIColors.reset,
    r=ANSIColors.winRed,
    g=ANSIColors.winGreen,
    b=ANSIColors.winBlue,
    y=ANSIColors.winYellow,
    w=ANSIColors.white,
    IN=ANSIColors.invert,
    FG=accentColInvANSI,
    BG=accentColInvANSI,
    TIME=datetime.now().strftime("%H:%M:%S"),
    USR=user,
    MNAME=machineName,
    DASHES='-' * (len(user + machineName) + 1),
    OS=OSVer))
