'''
recursively go through all the folders of the specified directory (default to current
working dir) and find and replace, prompting the user for each replace unless the
user specifies silent operation
'''
import sys
import os
import re
import codecs
##import config

import ui

__version__ = "0.7"

class FindAndReplace(object):
    def find(self, basedir, ext, find, replace, silent, dialog, find_options=0, dry_run=False, *args, **kwargs):
        '''
        recursively check every file and subfolder for the find and replace string...
        '''
        self.silent = silent
        self.replace_text = replace.decode('utf-8')
        self.total_changes = 0
        self.total_found = 0

        # assure ext is the correct format...
        ext = ur'|'.join(re.split(ur'[\|,\s]+', ext.decode('utf-8')))

        # compile the regexes...
        file_regex = re.compile(ur'\.(?:{})$'.format(ext), re.I)
        find_regex = re.compile(ur'{}'.format(find.decode('utf-8')), find_options | re.U)
    
        self.dialog = dialog

        if dry_run:
            msg = u'{}'.format(os.linesep).join([
                u'Checking: {}'.format(basedir),
                u'For file extensions: {}'.format(file_regex.pattern),
                u'Find regex pattern: {}'.format(find_regex.pattern),
                u'With options: {}'.format(find_options),
                u'Replace text: {}'.format(self.replace_text),
                u'Prompting for replacements: {}'.format('No' if silent else 'Yes'),
            ])
            self.dialog.update(msg)

        else:
            msg = u'checking "{}" files inside {} and all sub-folders for "{}" to replace with "{}"'.format(
                ext,
                basedir,
                find_regex.pattern,
                self.replace_text
            )
            self.dialog.update(msg)

            # iterate over all the folders and files...
            for root, dirs, files in os.walk(basedir):
                for name in files:
                    if not file_regex.search(name): continue

                    self.filepath = os.path.join(root, name)

                    # update user on status...
                    msg = u"checking: {}".format(self.filepath)
                    self.dialog.update(msg)
                    # http://docs.python.org/2/howto/unicode.html
                    # we use r+ so we don't truncate the file
                    f = codecs.open(self.filepath, encoding='utf-8', mode='r+')
                    self.text = f.read()
                    self.text_changes = 0
          
                    # do the actual find and replace...
                    try:  
                        (self.text, total_found) = find_regex.subn(self.replace, self.text)
                        self.total_found += total_found

                        # write out the new file text if a match was found...
                        if (self.text_changes > 0):
                            self.total_changes += self.text_changes
                            try:
                                f.truncate(0) # erase the file since we are going to write it out again
                                f.seek(0) # go to the beginning of the file
                                f.write(self.text)
                                msg = u"{} was changed {}/{} times".format(name, self.text_changes, total_found)
                            except:
                                msg = u"ERROR {} on file {}, couldn't write new text out, so no changes were made".format(
                                    sys.exc_info()[0],
                                    self.filepath
                                )

                            self.dialog.update(msg)
              
                        f.close() # close the current file to get ready for the next one
      
                    except ui.CancelAll:
                        msg = u"User aborted further searching{}Done".format(os.linesep)
                        self.dialog.update(msg)
                        f.close()
                        return;
              
            self.dialog.update(u"Made {}/{} total changes".format(self.total_changes, self.total_found))
            self.dialog.update(u"Done")
  
    def replace(self, match):
        '''
        find and replace things

        this is a callback meant to be invoked from a regex sub() or subn() call
        '''
        ret_str = match.group(0)
        make_change = True # make the change, unless the user says not to
        if not self.silent:
            # get a substring of the text...
            start = self.text.rfind(u"{}".format(os.linesep), 0, match.end(0)) + 1
            stop = self.text.find(u"{}".format(os.linesep), match.start(0), len(self.text))
            if start < 0: start = 0
            if stop < 0: stop = len(self.text)

            offset_start = match.start(0) - start

            orig_text = self.text[start:stop]
            orig_tuple = (offset_start, offset_start + len(match.group(0)))

            new_text = self.text[start:match.start(0)] + self.replace_text + self.text[match.end(0):stop]
            new_tuple = (offset_start, offset_start + len(self.replace_text))

            self.dialog.confirm_change(orig_text, new_text, orig_tuple, new_tuple, self.filepath)
            make_change = self.dialog.make_change

            # if the user pressed the cancel button, end everything...
            if (self.dialog.cancel == True):
                raise ui.CancelAll(u"User Cancelled all checks")

            # if the user pressed yes to all, then silence the remaining prompts...
            if (self.dialog.make_silent == True):
                self.silent = True

        if make_change:
            self.text_changes += 1
            ret_str = self.replace_text

        return ret_str
    
def console():
    import argparse
    # http://docs.python.org/library/argparse.html#module-argparse
    parser = argparse.ArgumentParser(description='REACHED (REplace seArCHED) - Search and Replace all files in a folder')
    parser.add_argument("-e", "--ext", dest="ext", action='append', default=[], help="Extension (eg, py)")
    parser.add_argument("--version", action='version', version="%(prog)s {}".format(__version__))
    parser.add_argument("-f", "--find", dest="find", default="", help="The regex or text to be found and eventually replaced")
    parser.add_argument("-r", "--replace", dest="replace", default="", help="Every find will be replaced with this text")
    parser.add_argument("--silent", dest="silent", action='store_true', help="Don't prompt on every replace")
    parser.add_argument("-d", "--dir", dest="basedir", default=os.getcwd(), help="Directory to check, defaults to current working directory")
    parser.add_argument("-g", "--gui", dest="gui", action='store_true', help="Activate the gui")

    #parser.add_argument("find", default="", metavar="FIND_REGEX", help="The regex or text to be found and eventually replaced")
    # find regex options (correspond to re.I, re.S, re.M)
    parser.add_argument("-i", "--ignorecase", dest="find_options", action='append_const', const=re.I, help="--find regex will ignore case")
    parser.add_argument("-m", "--multiline", dest="find_options", action='append_const', const=re.M,  help="--find regex ^ and $ will match at each line")
    parser.add_argument("-s", "--dotall", dest="find_options", action='append_const', const=re.S, help="--find regex will ignore case")
    parser.add_argument("--dry-run", dest="dry_run", action='store_true', help="dry run, don't actually do anything")

    options = parser.parse_args()

    find_options = 0
    if options.find_options:
        find_options = reduce(lambda x, y: x | y, options.find_options)

    run_prog = True
    fr = FindAndReplace()
    callback = fr.find
    kwargs = {
        'basedir': options.basedir,
        'ext': '|'.join(options.ext),
        'find': options.find,
        'replace': options.replace,
        'silent': options.silent,
        'dialog': options,
        'find_options': find_options,
        'dry_run': options.dry_run,
    }

    if not options.dry_run and (options.gui or re.search('.pyw$', __file__.lower())):

        import gui # we import here since we don't want to invoke the TK gods if we don't have to
        kwargs['fr'] = fr
        callback = gui.Gui

        # restore last values if they aren't set, this is only done in gui mode since command line this would
        # be way unexpected behavior that the user couldn't change before running the command...
        #if not options.basedir:
            #options.basedir = config.get('last_basedir','');
        #if not options.ext:
            #options.ext = config.get('last_ext','');
          
        # dialog = ui.Gui()
        # gui.ui(options.find,options.replace,options.basedir,options.ext,options.silent)
        # save some of the values...
        ## config.add('last_basedir',basedir);
        ##config.add('last_ext',ext);
        ##config.set()

    else:
        # set defaults by hand if they weren't specified in the call...
        if not options.find:
            #options.find = raw_input("Enter find regex pattern or text:{}".format(os.linesep))
            print "please pass in --find"
            run_prog = False
        if not options.replace:
            #options.replace = raw_input("Enter replace text:{}".format(os.linesep))
            print "please pass in --replace"
            run_prog = False

        kwargs['dialog'] = ui.Dialog()
        
    if run_prog:
        callback(**kwargs)

    else:
        parser.print_help()
if __name__=="__main__":
    console()

