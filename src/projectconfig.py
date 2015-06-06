import os.path
import json

project_config = '.pjconfig'

# Look for a .pjconfig file
def get_config():
    current_dir = os.getcwd()
    config_path = find_config_path(current_dir)
    if not config_path:
        print('No .pjconfig file found')
        raise
    try:
        cf = open(config_path, 'r')
        config_text = cf.read()
        cf.close()
    except: 
        print('Unable to read the .pjconfig file')
        raise
    try:
        config_data = json.loads(config_text)
    except:
        print('Your .pjconfig file is not valid JSON.  Please fix it and try again.')
        raise
    base_dir = os.path.dirname(config_path)

    return [config_data, base_dir]

def find_config_path(potential_dir):
    potential_path = os.path.join(potential_dir, project_config)
    if os.path.isfile(potential_path):
        return potential_path
    elif potential_dir != os.path.dirname(potential_dir):
        return find_config_path(os.path.dirname(potential_dir))
    else:
        return False
