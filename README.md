# pj - Projects for the command line

pj is a tool for defining projects on the command line, inspired by Sublime Text's projects feature.  

It is currently under development and not ready for use yet.  



### Development Instructions

To work on pj, simply clone this repo `git clone https://github.com/benmccormick/pj.git` somewhere.  You'll then be able to call the pj script at the root of the repo directly.  If you want to use it anywhere without giving the full path, you'll need to symlink it somewhere in your PATH like this: `ln -s /<path>/<to>/<pj>/pj /usr/local/bin/pj`. You should then be able to call `pj` directly to execute. 

The only other thing you'll need is a .pjconfig file.  You can define a simple one right in the repo that looks like this:

```
{
    "folders": [{
        "path": "src"
    }]
}
```

That should then list the files in the src directory when you run pj locally.  Of course you'll want a more complex example to test in.
