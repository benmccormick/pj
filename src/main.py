import configreader
import projectbuilder
import printer
import os
import sys

ignored_files = ['.DS_Store']
ignored_folders = ['.git', 'node_modules']


filter = sys.argv[1] if len(sys.argv) >= 2 else None

try:
    [config_data, base_dir] = configreader.get_config()

    if not config_data:
        print('No .pjconfig file found')
        exit()

    file_list = projectbuilder.get_file_list(config_data, base_dir, filter, ignored_files, ignored_folders)

    printer.print_list(file_list)
except: 
    print('Exiting...')

