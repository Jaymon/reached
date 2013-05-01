'''
handles dialog for terminal invokes
'''
import os

class Dialog(object):
    '''
    all interaction and notification of the user goes through a Dialog class
    '''
    def __init__(self, *args, **kwargs):
        self.nl = os.linesep
        self.make_change = False
        self.make_silent = False
        self.cancel = False

    def confirm_change(self, old_line, new_line, old_tuple=(), new_tuple=(), filepath = ''):
        '''
        prompt the user to confirm the change

        this will set the class variables make_change, make_silent, and cancel according to choices
        the user makes

        old_line -- unicode -- the original line
        new_line -- unicode -- the line with replacements made
        old_tuple -- tuple -- (start, stop) where the replaced text resides in the old_line
        new_tuple -- tuple -- (start, stop) where the replaced text resides in the new_line
        filepath -- string -- the file path
        '''
        print "*" * 80
        print "*    {}".format(filepath)
        print "*    Change:"
        print "*" * 80, self.nl
        print "\t", old_line.encode('utf-8')
        print self.nl
        print "*" * 80
        print "*    To:"
        print "*" * 80, self.nl
        print "\t", new_line.encode('utf-8')
        print self.nl
        print "*" * 80
        response = raw_input("Yes (Y), No (N), Yes to All (A), Cancel (C): ")
        response = response.lower()[0]
        if response == 'y':
            self.confirm_accept()

        if response == 'n':
            self.confirm_decline()

        elif response == 'c':
            self.confirm_cancel()

        elif response == 'a':
            self.confirm_silence()


    def confirm_silence(self):
        self.make_change = True
        self.make_silent = True

    def confirm_cancel(self):
        self.make_change = False
        raise CancelAll("C was selected")

    def confirm_accept(self):
        self.make_change = True

    def confirm_decline(self):
        self.make_change = False

    def update(self, msg):
        print msg.encode('utf-8')

class CancelSilent(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)
    
class CancelAll(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)
