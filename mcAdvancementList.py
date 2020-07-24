'''Gets advancement list from minecraft generated data, to fix a shared advancements datapack.
To generate data, use this command -->  java -cp SERVER/FILE/PATH/AND/NAME.jar net.minecraft.data.Main --server --reports  <-- in a terminal
on a minecraft server JAR, then point script to the /generated/ folder'''

import os

generatedAdvancementPath = input("Minecraft generated data dump path (use .../generated/ folder): ")

print('\n\n')

if not generatedAdvancementPath.endswith("/"): generatedAdvancementPath = generatedAdvancementPath + "/"  # if it doesnt end in a slash, put one there

generatedAdvancementPath = generatedAdvancementPath + 'data/minecraft/advancements/'  # adds advancement at the end

for i in os.listdir(generatedAdvancementPath): # for each advancement folder
    if i == 'recipes':  # i dont want to fill up the file with recepies, and they arent even important to the game, so I leave them out here.
        continue	    # if you want to keep the recepies, delete these two lines
    advancementsList = os.listdir(generatedAdvancementPath + i + '\\')  # gets list of each advancement in subfolder
    
    print()  # empty line to separate adv. folders
    
    for j in advancementsList:         # for each advancement there is in the folder,
        j = j.replace('.json','')      # replace the file endings with nothing
        advancementPath = i + '/' + j  # make advancement path, like "nether/get_wither_skull"
        # next line prints the commands
        print('execute as @a[advancements={{minecraft:{0}=true}}] run advancement grant @a[advancements={{minecraft:{0}=false}}] only minecraft:{0}'.format(advancementPath))
input('\n\npress ENTER to exit')
