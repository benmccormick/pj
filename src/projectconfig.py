import os.path
import json
# Long Term this should look recursively down a directory path to 
# find a config, for now we'll just look in the current directory

project_config = '.pjconfig'

# Look for a .pjconfig file
def get_config():
    
    if not os.path.isfile(project_config):
        return False
    cf = open(project_config, 'r')
    config_text = cf.read()
    cf.close()
    config_data = json.loads(config_text)

    return config_data
