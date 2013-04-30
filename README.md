# Reached

REplace seArCHED - Commandline search and replace over an entire directory

I originally wrote this about five years ago and then forgot about it, but just recently I needed to go through
and search/replace a large body of code and this just happened to be in an old Dropbox folder, 
so I've pulled it out, dusted it off and cleaned it up a bit, and now I'm putting it on
Github so I'll remember it exists in the future.

## Install

Use pip:

You could also just clone the repo and run, in the repo directory:

    $ python setup.py install

as described [here](http://docs.python.org/2/install/)


## Use

After installation, you should be able to use this on the command line using:

    $ reached --find=<FIND REGEX> --replace=<REPLACE TEXT> --dir=/path/to/search

You can also invoke it with a gui if you have TKinter Python bindings installed

    $ reached --gui

It will fail spectacularly if you don't have the TKinter modules installed.

See all the options:

    $ reached --help


