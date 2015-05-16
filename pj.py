#!/usr/bin/python

# pj API

# pj init
# pj ls - list projects
# pj ch <projectname> - change current project
# pj pwp - print working project
# pj <content> - show files matching <content>
# pj  - Show all files in current project

import json;
import os.path

config = '/Users/ben/.pjrc'
workspace = '/Users/ben/.pjworkspace'

if not os.path.isfile(config):
    print "Can't find config file '" + config + "'"
    exit()
if not os.path.isfile(workspace):
    print "No project is set yet"
    exit()
cf = open(config, 'r')
config_text = cf.read()
cf.close()
wf = open(workspace, 'r')
workspace_text = wf.read()
wf.close()
config_data = json.loads(config_text)
workspace_data = json.loads(workspace_text)
curr_project = workspace_data['current_project']

project_data = filter(lambda x:x['name'] == curr_project, config_data['projects'])
if not len(project_data):
    print 'No project matches ' + curr_project

project = project_data[0]

print os.listdir(project['included_folders'][0])
