import os
from subprocess import Popen

# java executable, replace with path if not in PATH
java_path = 'java'
max_ram = '3G'

# specify jar name if you want to use somehting else
explicit_jar_name = None

def get_server_jar():
    # vanilla server
    vanilla = ['minecraft_server']
    # bukkit and bukkit forks
    bukkit = ['paper','glowstone','cloudspigot','tacospigot','spigot','bukkit']
    # paper/tuinity forks
    paper_forks = ['tuinity','purpur','yatopia','akarin','empirecraft','origami','purplane']
    # modded servers
    modded = ['fabric','forge','sponge','magma','thermos','crucible']

    # in order of importance 
    server_types = [paper_forks,bukkit,modded,vanilla]
    
    jars_list = []
    
    # make list of jar and exe files
    for file in os.listdir(os.getcwd()):
        if file.endswith('jar') or file.endswith('exe'):
            jars_list.append(file.lower())
            
    # get server jar
    for server_apis in server_types:
        for modding_api in server_apis:
            for jar in jars_list:
                if modding_api in jar:
                    return jar

# auto accept eula file
# https://account.mojang.com/documents/minecraft_eula
with open(os.getcwd() + '/eula.txt', 'w') as eula_file:
    eula_file.write('eula=true')
    
args = [
# windows terminal
'wt',
# set profile
'-p',
'"Powershell Core"',
# set directory
'-d',
'.\\',
# java
java_path,
# set min/max ram
'-Xmx' + max_ram,
'-Xms' + max_ram,
# anything not spigot-based has problems launching if the default windows text encoding is UTF8,
# this flag fixes that
'-Dsun.stdout.encoding=UTF-8'
# aikars flags
'-XX:+UseG1GC',
'-XX:+ParallelRefProcEnabled',
'-XX:MaxGCPauseMillis=200',
'-XX:+UnlockExperimentalVMOptions',
'-XX:+DisableExplicitGC',
'-XX:+AlwaysPreTouch',
'-XX:G1NewSizePercent=30',
'-XX:G1MaxNewSizePercent=40',
'-XX:G1HeapRegionSize=8M',
'-XX:G1ReservePercent=20',
'-XX:G1HeapWastePercent=5',
'-XX:G1MixedGCCountTarget=4',
'-XX:InitiatingHeapOccupancyPercent=15',
'-XX:G1MixedGCLiveThresholdPercent=90',
'-XX:G1RSetUpdatingPauseTimePercent=5',
'-XX:SurvivorRatio=32',
'-XX:+PerfDisableSharedMem',
'-XX:MaxTenuringThreshold=1',
# server jar
'-jar',
explicit_jar_name if explicit_jar_name != None else set_server_jar(),
'nogui'
]

if __name__ == '__main__':
    Popen(args)