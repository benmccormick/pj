import projectconfig
import configparser
import listprint
import os

ignored_files = ['.git', 'node_modules', '.DS_Store']

config_data = projectconfig.get_config()

if not config_data:
    print 'No .pjconfig file found'
    exit()

base_dir = os.getcwd()
file_list = configparser.get_file_list(config_data, base_dir, ignored_files)

listprint.print_list(file_list)

