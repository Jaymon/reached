# Reached

REplace seArCHED - Commandline search and replace over an entire directory

I originally wrote this about five years ago and then forgot about it, but just recently I needed to go through
and search/replace a large body of code and this just happened to be in an old Dropbox folder, 
so I've pulled it out, dusted it off, and cleaned it up a bit, and now I'm putting it on
Github so I'll remember it exists in the future.

## Install

Use pip:

    $ pip install git+https://github.com/Jaymon/reached#egg=reached

You could also just clone the repo and run, in the repo directory:

    $ python setup.py install

as described [here](http://docs.python.org/2/install/)

## Use

After installation, you should be able to use this on the command line using:

    $ reached --find=<FIND REGEX> --replace=<REPLACE TEXT> --dir=/path/to/search

You can also invoke it with a gui if you have TKinter Python bindings installed

    $ reached --gui

It will fail spectacularly if you don't have the TKinter modules installed. The GUI
also doesn't have the capability to set flags like ignore case, etc.

See all the options:

    $ reached --help

## Example

Let's say you have a folder of 500 python files and you have changed a module's name
from foo to bar, so you need to change all `import foo` statements to `import bar` statements,
you can do that by running:

    $ reached --find=foo --replace=bar --dir=/path/to/folder

`Reached` will prompt for each replacement, so you don't have to worry about it changing something
you didn't mean to change.

## License

MIT
