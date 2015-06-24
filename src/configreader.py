import os.path
import json
import re

"""
This module is responsible for finding and reading .pjconfig files, and converting them
to a python dict

Public Functions

- get_config: Looks up a config and parses it
"""

### Constants

project_config = '.pjconfig'

# Regular expression for comments
comment_re = re.compile(
    '(^)?[^\S\n]*/(?:\*(.*?)\*/[^\S\n]*|/[^\n]*)($)?',
    re.DOTALL | re.MULTILINE
)

# Look for a .pjconfig file
def get_config():
    """Looks for a pjconfig file and then parses it"""
    current_dir = os.getcwd()
    config_path = find_config_path(current_dir)
    if not config_path:
        print('No .pjconfig file found')
        raise
    try:
        cf = open(config_path, 'r')
        config_text = cf.read()
    except:
        print('Unable to read the .pjconfig file')
        raise
    finally:
        cf.close()

    try:
        config_data = parse_json(config_text)
    except:
        print('Your .pjconfig file is not valid JSON.  Please fix it and try again.')
        raise
    base_dir = os.path.dirname(config_path)

    return [config_data, base_dir]

def find_config_path(potential_dir):
    """Looks recursively down directories for a pjconfig file"""
    potential_path = os.path.join(potential_dir, project_config)
    if os.path.isfile(potential_path):
        return potential_path
    elif potential_dir != os.path.dirname(potential_dir):
        return find_config_path(os.path.dirname(potential_dir))
    else:
        return False


# This function is adapted from http://www.lifl.fr/~damien.riquet/parse-a-json-file-with-comments.html
def parse_json(config_text):
    """This function is a replacement for json.loads that handles json with comments"""

    ## Look for stuff that looks like comments
    match = comment_re.search(config_text)
    while match:
        # single line comment
        config_text = config_text[:match.start()] + config_text[match.end():]
        match = comment_re.search(config_text)

    # Return json file
    return json.loads(config_text)