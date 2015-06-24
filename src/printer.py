import os.path

"""
This module is responsible for printing the list of files to standard out
"""

#print the list of files to screen
def print_list(file_list, use_relative_path):
    for file_path in file_list:
        if use_relative_path:
            print(os.path.relpath(file_path))
        else:
            print(file_path)
