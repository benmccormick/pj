import os
import os.path
import fnmatch

"""
This file is responsible for parsing a .pjconfig file and translating it into a list of paths

For now it uses a rather inefficient algorithm, grabbing all files recursively from each base
folder, then streaming them through a set of filters before deduplicating and sorting the result.

Long term we should probably not walk any excluded subdirectories, but the current implementation
is easier to read/write, and optimizations can come later

Public Functions

- get_file_list
"""


def get_file_list(config_data, base_dir, filter_str, ignored_files, ignored_folders):
    """Get a full list of the files specified by the config_data"""

    filtered_files = get_filtered_files(config_data, base_dir, filter_str, ignored_files, ignored_folders)
    # put the generator in a set then convert to a list to clean it up
    file_list = deduplicate(filtered_files)
    file_list.sort()
    return file_list

def get_filtered_files(config_data, base_dir, filter_str, ignored_files, ignored_folders):
    """Get a generator stream of the files, filtered through all specified include/exclude rules"""

    filter_data = get_filter_data(config_data, filter_str)
    if 'folders' not in config_data:
        for path in get_base_files(base_dir, base_dir):
            yield path
    else:
        for folder in config_data['folders']:
            path = folder.get('path', base_dir)
            paths = get_base_files(path, base_dir)
            exclude_folders = folder.get('folder_exclude_patterns', []) + ignored_folders
            exclude_files = folder.get('file_exclude_patterns', []) + ignored_files
            exclude_patterns = filter_data.get('exclude_patterns', [])
            include_patterns = filter_data.get('include_patterns', [])
            import pdb; pdb.set_trace()
            filtered_paths = filter_paths(paths, base_dir,
                exclude_folders=exclude_folders,
                exclude_files=exclude_files,
                exclude_patterns=exclude_patterns,
                include_patterns=include_patterns)
            for path in filtered_paths:
                yield path

def get_base_files(folder, base_dir):
    """Do an initial walk of a folder and pull out all files in the directory recursively"""
    returned_files = []
    full_path = normalize_path(folder, base_dir)
    file_walk = os.walk(full_path)
    for directory in file_walk:
        [path, dir_list, file_list] = directory
        for file_name in file_list:
            file_path = path + '/' + file_name
            yield file_path

def filter_paths(paths, base_dir, exclude_folders, exclude_files, exclude_patterns, include_patterns):
    """Takes a set of paths, along with the include and exclude rules, and filters the paths"""

    for path in paths:
        is_included = included(path, include_patterns)
        if is_included:
            is_excluded = excluded(path, base_dir, exclude_folders, exclude_files, exclude_patterns)
            if not is_excluded:
                yield path

def excluded(path, base_dir, exclude_folders, exclude_files, exclude_patterns):
    """Given a set of exclude rules, determines if a path should be excluded"""
    if exclude_folders and any([path_contains_folder(path, folder, base_dir) for folder in exclude_folders]):
        return True
    if exclude_files and any([path_matches_file_pattern(path, pattern) for pattern in exclude_files]):
        return True
    if exclude_patterns:
        return any([path_matches_pattern(path,pattern) for pattern in exclude_patterns])
    return False


def included(path, include_patterns):
    """Given a set of include rules, determines if a path should be included"""
    if not include_patterns:
        return True
    return any([path_matches_pattern(path,pattern) for pattern in include_patterns])

def get_filter_data(config_data, filter_str):
    """Parses the config to grab information for the current filter if one exists"""
    filter_data = {}
    if filter_str:
        if 'filters' in config_data and filter_str in config_data['filters']:
           filter_data = config_data['filters'][filter_str]
        else:
            #TODO: This should be treated as an error
            print('Invalid Filter')
    return filter_data


def normalize_path(path, base_dir):
    """This takes a relative or absolute path and normalizes it to be abbsolute"""
    full_path = ''
    if path and path[0] == '/':
       full_path = path
    else:
       full_path = base_dir + '/' + path
    return full_path

def deduplicate(files):
    """This takes a generator, list or other collection and deduplicates it, returning a list"""
    return list(set(files))

def path_contains_folder(path, folder, base_dir):
    """
    This function takes a path and looks to see if it contains a folder pattern
    It excludes matches that happen on the basedir, if the current path includes the base directory
    """

    # TODO: This really should probably be the **folder base** not the **base_dir** of the project
    if path.startswith(base_dir):
        path = path[len(base_dir):]
    path_parts = path.split('/')
    clean_folder = folder.strip()
    return clean_folder in path_parts

def path_matches_file_pattern(path, pattern):
    """
    checks to see if a path matches a file pattern
    """
    file_name = path.split('/')[-1]
    return fnmatch.fnmatch(file_name, pattern)

def path_matches_pattern(path, pattern):
    """checks to see if a path matches a unix glob pattern"""
    return fnmatch.fnmatch(path, pattern)
