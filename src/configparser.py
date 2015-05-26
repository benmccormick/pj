# Long term this should handle a full project configuration
# For now it just processes a single included folder, without recursing it

import os
import os.path


def get_file_list(config_data, base_dir, ignored_files):

    file_list = []
    for folder in config_data['folders']:
        folder_list = []
        if 'path' in folder:
            folder_list.extend(include_folders(folder['path'], base_dir, ignored_files))
        else:
            #TODO: Throw Error here
            print 'invalid config'
        # then add included files, bypassing the ignored files list since they were
        # added explicitly
        if 'folder_exclude_patterns' in folder:
            folder_list = exclude_folders(folder_list, folder['folder_exclude_patterns'], base_dir)
        if 'file_exclude_patterns' in folder:
            folder_list = exclude_files(folder_list, folder['file_exclude_patterns'], base_dir)
        file_list.extend(folder_list)
    
    return deduplicate(file_list)


def include_folders(folder, base_dir, ignored_files):
    returned_files = []
    full_path = normalize_path(folder, base_dir)
    file_walk = os.walk(full_path) 
    for directory in file_walk:
        path = directory[0]
        file_list = directory[2]
        for file_name in file_list:
            file_path = path + '/' + file_name
            if not should_be_ignored(file_path, ignored_files):
                returned_files.append(file_path)

    return returned_files

def exclude_folders(paths, excluded_folders, base_dir):
    # this could be optimized later if the  paths were sorted in some way
    excluded_folders = map(lambda f: normalize_path(f, base_dir), excluded_folders)
    for exclude_folder in excluded_folders:
        paths = filter(lambda p: not p.startswith(exclude_folder), paths)
    return paths

def exclude_files(paths, excluded_files, base_dir):
    # this could be optimized later if the  paths were sorted in some way
    excluded_files = map(lambda f: normalize_path(f, base_dir), excluded_files)
    for exclude_file in excluded_files:
        paths = filter(lambda p: not p == exclude_file, paths)
    return paths



def should_be_ignored(file_path, ignored_files):
    for ignore_str in ignored_files:
        if ignore_str in file_path:
            return True
    return False

def normalize_path(path, base_dir):
    full_path = ''
    if path and path[0] == '/':
       full_path = path 
    else:
       full_path = base_dir + '/' + path
    return full_path

def deduplicate(files):
    return list(set(files))
