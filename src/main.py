import os
import projectconfig


config_data = projectconfig.get_config()

if not config_data:
    print 'No .pjconfig file found'
    exit()

project = config_data['files']

print os.listdir(project[0]['included_folders'][0])
