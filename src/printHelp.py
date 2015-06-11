print '''
pj - Projects for the Command Line

Usage: pj [--help] [--version] [--python3] [--debug] [--filter|-f filtername] [--relative-path|-r]

Options

--help                   Prints help documentation
--version                Prints version information
--python3                Tries to use `python3` instead of `python` to run pj
--debug                  Prints the location of the pj script
--filter | -f            Use a filter to limit the files shown
--relative-path | -r     Display the output file paths as relative to the current directory

Information

pj uses a project configuration syntax based on sublime text's project configuration.

When executed, it prints a list of files in the project

To define a new project create a .pjconfig file inside a directory.

A .pjconfig file consists of a json based project definition in the following format:

{
    "folders": [{
        "path": "sublime",
        "folder_exclude_patterns": ["SublimeLinter"],
        "file_exclude_patterns": ["*.sublime-settings", "*.sublime-snippet", "*.tmTheme"]
    }]
}

Each JSON object in the folder list can contain a path key as well as folder exclude and file exclude patterns.

*path* can be relative to the base directory or absolute paths, and do not necessarily need to be within the base directory.
*folder_exclude_pattern* accepts a list of folder names which match if a directory name occurs anywhere in the path of a file
*file_exclude_pattern* accepts a list of file patterns which match a file name using unix file matching conventions.

Example usage:

Open all files in a editor like vim

vim $(pj)

With a file search tool like ack

pj | ack -x <search term>

With a fuzzy finder like fzf

pj | fzf | vim

With a file picker like fpp

pj | fpp

'''
