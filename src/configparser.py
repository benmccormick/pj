import os
import os.path
import fnmatch

#
# This file is responsible for parsing a .pjconfig file and translating it into a list of paths
#


def get_file_list(config_data, base_dir, filter_str, ignored_files, ignored_folders):

    file_list = []
    for folder in config_data['folders']:
        folder_list = []
        path = ''
        if 'path' in folder:
            path = folder['path']
        else:
            # assume this is a base level folder
            path = base_dir
        folder_list.extend(include_folder(path, base_dir))
        # then add included files, bypassing the ignored files list since they were
        # added explicitly
        if 'folder_exclude_patterns' in folder:
            folder_list = exclude_folders(folder_list, folder['folder_exclude_patterns'] + ignored_folders, base_dir)
        if 'file_exclude_patterns' in folder:
            folder_list = exclude_files(folder_list, folder['file_exclude_patterns'] + ignored_files, base_dir)
        file_list.extend(folder_list)
    file_list = deduplicate(file_list)
    file_list = filter_list(file_list, filter_str, config_data)
    file_list.sort()
    return file_list
    

def include_folder(folder, base_dir):
    returned_files = []
    full_path = normalize_path(folder, base_dir)
    file_walk = os.walk(full_path) 
    for directory in file_walk:
        path = directory[0]
        file_list = directory[2]
        for file_name in file_list:
            file_path = path + '/' + file_name
            returned_files.append(file_path)

    return returned_files

def exclude_folders(paths, excluded_folders, base_dir):
    # we're just matching folder names if they occur at any level in the path
    for excluded_folder in excluded_folders:
        paths = filter(lambda path: not path_contains_folder(path, excluded_folder, base_dir), paths)
    return paths

def exclude_files(paths, excluded_files, base_dir):
    # We're just matching file names, not paths
    for exclude_file in excluded_files:
        paths = filter(lambda path: not path_matches_file_pattern(path, exclude_file), paths)
    return paths

def filter_list(file_list, filter_str, config_data):
    filter_data = {}
    if not filter_str:
        return file_list
    if 'filters' in config_data and filter_str in config_data['filters']:
       filter_data = config_data['filters'][filter_str]
    else: 
        #TODO: This should be treated as an error
        print('Invalid Filter')
    filtered_list = file_list

    if 'include_patterns' in filter_data:
        filtered_list = []
        #TODO: Assuming this is an array, should throw an error if its not
        for pattern in filter_data['include_patterns']: 
            filtered_list.extend(filter(lambda path: path_matches_pattern(path, pattern), file_list))
    if 'excluded_patterns' in filter_data:
        filtered_list = []
        #TODO: Assuming this is an array, should throw an error if its not
        for pattern in filter_data['include_patterns']: 
            filtered_list.extend(filter(lambda path: not path_matches_pattern(path, pattern), file_list))
    return filtered_list

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

def path_contains_folder(path, folder, base_dir):
    # this is not normalized off of base_dir, so exclude patterns
    # that occur further up the tree will also be caught for now
    if path.startswith(base_dir):
        path = path[len(base_dir):]
    path_parts = path.split('/')
    clean_folder = folder.strip()
    return clean_folder in path_parts

def path_matches_file_pattern(path, pattern):
   file_name = path.split('/')[-1]
   return fnmatch.fnmatch(file_name, pattern)

def path_matches_pattern(path, pattern):
   return fnmatch.fnmatch(path, pattern)
