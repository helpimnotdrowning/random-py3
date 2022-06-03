import os
from shlex import split
from subprocess import Popen
from time import sleep

############## change these to your liking:

# java path; if the path to your preferred java.exe is different (not 1st on path, not on path at all, different version, debugging, etc.)
# you can specify it here. OTHERWISE, you don't need to change it from just 'java'
JAVA = 'java'

# ram amount; can be specified like '4096M' or '4G'
RAM = '4G'

# ONLY CHANGE THIS if you need to use a specific file that doesn't get picked up or is in a different directory
# OTHERWISE, this script will automatically detect your JAR file
JAR_NAME = None

##############

# SyntaxError: f-string expression part cannot include a backslash
# f strings are funny, so i have to make the '\' its own variable
BACKSLASH = '\\'

# automatically detect the server jar in the folder where this script is (no subfolders)
def get_server_jar():
    if JAR_NAME:
        return JAR_NAME

    ### common server disributions (the ones that I hear about) vv

    vanilla = ['minecraft_server', 'mojang']

    bukkit = ['paper', 'glowstone', 'cloudspigot', 'tacospigot', 'spigot', 'bukkit']

    paper_forks = ['tuinity', 'purpur', 'pufferfish', 'akarin', 'empirecraft', 'origami']

    modded = ['fabric', 'forge', 'sponge', 'magma', 'thermos', 'crucible']

    ###

    # in order of importance
    server_types = [paper_forks, bukkit, modded, vanilla]

    jar_list = []

    # make list of server executables
    for file in os.listdir(os.getcwd()):
        # some legacy server jars were released as an exe, and some** people build their server jars as
        # native exe with graalvm, so exe is included in the autodetect
        if file.endswith('jar') or file.endswith('exe'):
            jar_list.append(file.lower())
            
    # get server jar
    for distro_group in server_types:
        for distro in distro_group:
            valid_jars = []
            for jar in jar_list:
                valid_jars.append(jar) if distro in jar else None
                
            if valid_jars != []:
                # this replacment (\ -> /) is because shlex.split() strips the windows slashes from strings
                # it doesn't strip the normal slashes though
                return (os.getcwd() + "/" + valid_jars[-1]).replace('\\','/')

# automatically accept the EULA file ( https://account.mojang.com/documents/minecraft_eula )
with open(os.getcwd() + '/eula.txt', 'w') as eula_file:
    eula_file.write('eula=true')

def append(tarlist, *strings):
    for string in strings:
        tarlist.append(string)

args = []

# launch Windows Terminal with pwsh in server root
append(args, *split(f'wt -p "PowerShell" -d "{os.getcwd().replace(BACKSLASH,"/")}"'))
# java path, ram stuff
append(args, *split(f'{JAVA} -Xmx{RAM} -Xms{RAM}'))
# anything not spigot-based has problems launching if the default windows text encoding is UTF8, this should fix that
# comment this out if text looks weird
append(args, *split('-Dsun.stdout.encoding=UTF-8'))
# aikars flags from https://docs.pufferfish.host/optimization/how-to-apply-aikars-flags/
append(args, *split('-XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:InitiatingHeapOccupancyPercent=15'))
# performance increases when using Pufferfish and Purpur JARs, shouldn't affect anything otherwise
append(args, *split('--add-modules=jdk.incubator.vector'))
# the minecraft jar
append(args, *split(f'-jar {get_server_jar()}'))
append(args, *split('nogui'))

if __name__ == '__main__':
    print("Launching with:\n" + args)
    sleep(3)
    Popen(args)
