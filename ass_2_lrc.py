from re import sub, split


def ass_to_lrc(input_filepath, output_path = ''):
    with open(input_filepath, 'r') as ass_file:
        ass_file_lines = ass_file.read().splitlines()
        
    # if no custom output filename is passed, take the input filename and replace the '.ass' with '.lrc'
    if output_path == '':
        output_path = sub('.ass', '.lrc', input_filepath)
        
    with open(output_path, 'w+') as lrc_file:                     
        for line in ass_file_lines:
        # parse the [Events] format line to get location of starting time for line and the text of the line itself
            if line.startswith('[Events]'):
                # the format line will always be on the line after the [Events], so it gets the index of the [Events] line +1
                # this doesnt look for the index of the format line because thee are multiple format lines, and index() only gets the first occurance
                format_line = ass_file_lines[ass_file_lines.index('[Events]') + 1]
                
                # removes the Format: part of the line
                format_line = sub('Format: ', '', format_line)
                # splits it up by commas
                format_list = split(', ', format_line)
                
                # gets number of fields in format
                format_fields = int(len(format_list))
                # gets the index number of the Start and Text fields, assigns them
                time_start_location = format_list.index('Start')
                dialogue_start_location = format_list.index('Text')
                
            # check if line is a dialogue line
            if line.startswith('Dialogue: '):
                # delete Dialogue: part of line
                dialogue_line = sub('Dialogue: ', '', line)
                # split up line by number of elements in format -1 (because itd go an extra comma if not -1'd)
                dialogue_element_list = split(',', dialogue_line, maxsplit = format_fields - 1)
                # get dialogue start time from index
                dialogue_start_time = dialogue_element_list[time_start_location]
                # get actual dialogue start from index
                dialogue_words = ''.join(dialogue_element_list[dialogue_start_location:])
                
                # write the line to lrc file
                lrc_file.write('[' + dialogue_start_time + '] ' + dialogue_words + '\n')
            
    
        
ass_filepath = input("path to .ass file     : ")
lrc_filepath = input("path to new .lrc file (empty to copy and change extension: ")

ass_to_lrc(ass_filepath)
input()
