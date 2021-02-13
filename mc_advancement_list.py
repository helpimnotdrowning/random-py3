'''
Gets advancement list from minecraft generated data, to fix a shared advancements datapack.
To generate data, use this command -->  java -cp path/to/server.jar net.minecraft.data.Main --server --reports  <-- in a terminal
on a minecraft server JAR, then point script to the /generated/ folder
'''

import os

generated_advancement_path = input("Minecraft generated data dump path (use .../generated/ folder): ")

print('\n\n')

# if the path doesnt end in a slash, put one there
if not generated_advancement_path.endswith("/"):
    generated_advancement_path += "/" 

# adds advancement at the end
generated_advancement_path = generated_advancement_path + 'data/minecraft/advancements/'  

# for each advancement folder
for i in os.listdir(generated_advancement_path):
    # leave out recepies. i dont think they need to be shared, so they get left out
    # if you want to keep them, comment out the next two lines
    if i == 'recipes':
        continue
        
    # gets list of each advancement in subfolder
    advancements_list = os.listdir(generated_advancement_path + i + '\\')
    
    # empty line to separate adv. folders
    print()
    
    # for each advancement there is in the folder,
    for j in advancements_list:
        # delete file extensions
        j = j.replace('.json','')
        # make advancement path, like "nether/get_wither_skull"
        advancement_path = i + '/' + j
        # print command
        print('execute as @a[advancements={{minecraft:{0}=true}}] run advancement grant @a[advancements={{minecraft:{0}=false}}] only minecraft:{0}'.format(advancement_path))
input('\n\npress ENTER to exit')
