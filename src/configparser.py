# Long term this should handle a full project configuration
# For now it just processes a single included folder, without recursing it

import os

base_dir = os.getcwd()

def get_file_list(config_data):

    project = config_data['files']

    file_list = os.listdir(project['included_folders'][0])

    file_list = map(lambda f: base_dir + '/' + f, file_list)

    return file_list
