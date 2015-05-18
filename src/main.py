import projectconfig
import configparser
import listprint


config_data = projectconfig.get_config()

if not config_data:
    print 'No .pjconfig file found'
    exit()

file_list = configparser.get_file_list(config_data)

listprint.print_list(file_list)

