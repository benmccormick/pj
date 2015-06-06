# pj - Projects for the command line

pj is a tool for defining projects on the command line, inspired by Sublime Text's projects.  

### Features

- Define a set of files that make up a project
- Use "filters" to narrow down file list: To source code for a feature, blog post text files that haven't been published yet, a specific filetype, or any other meaningful subset
- Combine with other *nix programs for project search, editing, or to easily find a specific file

### Installation

#### Homebrew

pj isn't in the official homebrew repo, but you can install it using the formula in this repo directly

    brew install https://raw.githubusercontent.com/benmccormick/pj/master/pj.rb

#### Manual

```
# Go to /usr/local or whatever directory you use for installing scripts
cd /usr/local
# clone the repository from github
git clone https://github.com/benmccormick/pj
# symlink pj to /usr/local/bin or somewhere else in your path
ln -s /usr/local/pj/pj /usr/local/bin/pj
```

### Usage

pj is simple to use.  In the simplest case, you can just run 

```
pj
```

to list out all of the files in a project.  That's not super useful on its own, but it becomes powerful when combined with other programs.

You can have project wide search by combining pj with a search program like [grep](http://www.gnu.org/software/grep/), [ack](http://beyondgrep.com/), or [ag](https://github.com/ggreer/the_silver_searcher).

```
pj |ack foo # lists all occurences of foo within files in the project
```

You can list out the project files and then pick the one(s) you want using a file picker like Facebook's [PathPicker](https://facebook.github.io/PathPicker/)

```
pj | fpp # pick a file or several files to open in an editor or handle other tasks
```

You can use a fuzzy finder like [fzf](https://github.com/junegunn/fzf) to select a file from the project list and open it up in an editor like Vim.

```
vim $(pj | fzf)
```

For larger projects, you can also use filters to select a subset of the project.  For instance if you've created a filter named `analytics` that limits selection to files related to an analytics feature, you can pick from those files like this:

```
pj -f analytics | fpp
```

### Configuration

To define a project with pj, you'll need a .pjconfig file.  You should place that project file at the root of your project's primary directory (below wherever you expect to execute pj from).  

.pjconfig files contain 2 main items, a list of folders and a set of filters.  A typical .pjconfig might look something like this:

```
{
    "folders": [{
        "path": "wcui/app/js",
        "folder_exclude_patterns": ["vendor"],
        "file_exclude_patterns": []
    }, {
        "path": "wcui/app/css",
        "folder_exclude_patterns": ["vendor"]
    }, {
       "path": "wcui/views",
       "file_exclude_patterns": ["*.pyc"]
    }, {
        "path": "wcui/tests/nightwatch"
    }, {
        "folder_exclude_patterns": ["wcui", "docs"]
    }],

    "filters": {
        "js": {
            "include_patterns": ["*.js", "*.es6"]
        },
        "nightwatch": {
            "include_patterns": ["*nightwatch.json", "*/tests/nightwatch*"]    
        }
    }
}
```

Each item in the `folders` list corresponds to a set of files included in the project. Each folder includes a path (if no path is specified, the path is assumed to be the base directory), and may optionally include a list of `folder_exclude_patterns` and `file_exclude_patterns`.  

Filters have a key value that you can use to reference them later, and then can contain an `include_patterns property` and an `exclude_patterns property`.  These take a pattern which is matched against the whole path for each file.
