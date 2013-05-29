import os

# gui/dialog support...
import tkFileDialog
import Tkinter
from Tkconstants import *
import tkMessageBox
from ScrolledText import ScrolledText

import ui
##import config

class Dialog(ui.Dialog):
  
    def __init__(self, frame=None):
        self.parent_frame = frame # set the parent frame
        self.confirm_frame = None
        self.make_change = False
        self.new_line = u''
        self.status_text = u''
        self.make_silent = False
        self.cancel = False

        # set screen position...
        x = 0
        y = 0
        ##x = config.get('status_x',0)
        ##y = config.get('status_y',0)
        ##if x and y:
        ##    self.parent_frame.geometry("+%d+%d" % (int(x),int(y)))

        # create a status message widget and bind it to the parent...
        #self.status_text = ScrolledText(self.parent_frame, height=20, width=80, state=DISABLED)
        #self.status_text.pack()
        self.status_text = ScrolledText(self.parent_frame, wrap=WORD, pady=2, padx=3, state=DISABLED)
        self.status_text.pack(fill=BOTH, expand=Y)
        self.parent_frame.protocol("WM_DELETE_WINDOW", self.destroy)
        self.parent_frame.bind("<Escape>", self.destroy)
        self.parent_frame.bind("<Configure>", self.save_pos)
        self.status_text.update()

    def confirm_change(self, old_line, new_line, old_tuple=(), new_tuple=(), filepath = ''):
        self.confirm_frame = Tkinter.Toplevel(self.parent_frame, padx=10, pady=10)
        #self.confirm_frame.grid(padx=10,pady=10)

        self.confirm_frame.protocol("WM_DELETE_WINDOW", self.confirm_decline)

        # set screen position...
        ##x = config.get('dialog_x', (self.parent_frame.winfo_rootx() + 50))
        ##y = config.get('dialog_y', (self.parent_frame.winfo_rooty() + 50))
        x = self.parent_frame.winfo_rootx() + 50
        y = self.parent_frame.winfo_rooty() + 50
        if x and y:
            self.confirm_frame.geometry("+%s+%s" % (x,y))

        # bind enter to ok and escape to cancel buttons...
        self.confirm_frame.bind("<Return>", self.confirm_accept)
        self.confirm_frame.bind("<Escape>", self.confirm_decline)
        self.confirm_frame.bind("<Configure>", self.save_pos)
        # make the new dialog a part of the parent...
        self.confirm_frame.transient(self.parent_frame)
        # focus onto the dialog...
        self.confirm_frame.focus_set()

        label = Tkinter.Label(self.confirm_frame, text=filepath)
        label.pack()

        label = Tkinter.Label(self.confirm_frame, text="Change:")
        #label.grid(row=row_i, column=0, sticky=W)
        label.pack()

        #entry = Tkinter.Text(self.confirm_frame, width=75, height=5)
        #entry = ScrolledText(self.confirm_frame, width=75, height=5)
        entry = ScrolledText(self.confirm_frame, height=5, wrap=WORD, pady=2, padx=3)
        entry.insert(Tkinter.INSERT, old_line.encode('utf-8'))
        # highlight the text to be changed...
        if len(old_tuple) == 2:
            entry.tag_add('found', '1.%s' % (old_tuple[0]), '1.%s+%sc' % (old_tuple[0], old_tuple[1] - old_tuple[0]))
            entry.tag_config('found', foreground='red')

        entry.config(state=DISABLED)
        entry.pack(fill=BOTH, expand=Y)

        label = Tkinter.Label(self.confirm_frame, text="To:")
        label.pack()

        self.new_entry = ScrolledText(self.confirm_frame, height=5, wrap=WORD, pady=2, padx=3)
        self.new_entry.insert(Tkinter.INSERT, new_line.encode('utf-8'))
        # highlight the text to be changed...
        if len(new_tuple) == 2:
            self.new_entry.tag_add('found', '1.%s' % (new_tuple[0]), '1.%s+%sc' % (new_tuple[0], new_tuple[1] - new_tuple[0]))
            self.new_entry.tag_config('found', foreground='red')

        self.new_entry.config(state=DISABLED)
        self.new_entry.pack(fill=BOTH, expand=Y)

        btnDisplay = Tkinter.Button(self.confirm_frame, text="Yes", command=self.confirm_accept, default=ACTIVE)
        #btnDisplay.grid(row=row_i, column=0)
        btnDisplay.pack(side=LEFT, padx=5, pady=5)

        btnDisplay = Tkinter.Button(self.confirm_frame, text="No", command=self.confirm_decline)
        #btnDisplay.grid(row=row_i, column=1)
        btnDisplay.pack(side=LEFT, padx=5, pady=5)

        btnDisplay = Tkinter.Button(self.confirm_frame, text="Cancel", command=self.confirm_cancel)
        #btnDisplay.grid(row=row_i, column=1)
        btnDisplay.pack(side=LEFT, padx=5, pady=5)

        btnDisplay = Tkinter.Button(self.confirm_frame, text="Yes to All", command=self.confirm_silence)
        #btnDisplay.grid(row=row_i, column=1)
        btnDisplay.pack(side=LEFT, padx=5, pady=5)

        self.confirm_frame.update()
        try:
            self.parent_frame.wait_window(self.confirm_frame)
        except Tkinter.TclError:
            # sometimes the wait_window fails, I'm not sure why, but it seems to be
            # safe to just ignore it *shrug*
            pass

        self.confirm_frame = None
      
    def confirm_silence(self):
        self.make_change = True
        self.make_silent = True
        self.clean_up()
  
    def confirm_cancel(self):
        self.make_change = False
        self.cancel = True
        self.clean_up()
      
    def confirm_accept(self):
        #self.new_line = self.new_entry.get(1.0, END)
        self.make_change = True
        self.clean_up()

    def confirm_decline(self):
        self.make_change = False
        self.clean_up()

    def clean_up(self,event = None):
        self.save_pos()
        #print self.screen_pos_x,self.screen_pos_y
        self.parent_frame.focus_set()
        self.confirm_frame.destroy()

    def destroy(self,event = None):
        self.parent_frame.destroy()
  
    def save_pos(self,event = None):
        return
        ## save the screen position of the dialog box
        #if self.confirm_frame:
            #try:
                #config.add('dialog_x',(self.confirm_frame.winfo_rootx() - 4))
                #config.add('dialog_y',(self.confirm_frame.winfo_rooty() - 30))
            #except:
                #pass

        ## save the status box's position
        #if self.parent_frame:
            #try:
                #config.add('status_x',self.parent_frame.winfo_rootx() - 4)
                #config.add('status_y',self.parent_frame.winfo_rooty() - 30)
            #except:
                #pass  
    
    def update(self,msg):
        # if the window no longer exists, its text can't be updated
        try:
            self.status_text.config(state=NORMAL)
            # Add the new message
            self.status_text.insert(END, msg.encode('utf-8') + os.linesep)
            # Scroll down to the bottom again
            self.status_text.see(END)
            # Make the display uneditable
            self.status_text.config(state=DISABLED)
            self.status_text.update()
        except:
            pass

class Gui(object):
    """This is the main GUI"""
  
    def __init__(self, fr, basedir, ext, find, replace, silent, find_options, *args, **kwargs):
        self.tk = Tkinter.Tk()
        self.tk.protocol("WM_DELETE_WINDOW", self.destroy)
        self.tk.bind("<Return>", self.submit)
        self.tk.bind("<Escape>", self.destroy)
        self.tk.bind("<Configure>",self.save_pos)
        # restore screen position...
        x = 0
        y = 0
        ##x = config.get('main_x',0)
        ##y = config.get('main_y',0)
        ##if x and y:
        ##    self.tk.geometry("+%d+%d" % (int(x),int(y)))

        frame = Tkinter.Frame(self.tk)
        frame.pack()

        # set defaults...
        self.fr = fr
        self.find = find
        self.replace = replace
        self.basedir = basedir
        self.ext = ext
        self.silent = silent
        self.find_options = find_options
        self.args = args
        self.kwargs = kwargs

        """Set the Window Title"""
        self.tk.title("Reached - Find / Replace")
        #self.tk.iconbitmap(os.path.join(os.path.abspath(os.path.dirname(__file__)),'icon.ico'))

        """Display the main window
        with a little bit of padding"""
        frame.grid(padx=10,pady=10)
        self.create_widgets(frame)
        self.tk.mainloop()
        #print "callback ",self.tk.report_callback_exception
     
    def create_widgets(self, frame):
        """Create all the widgets that we need"""

        row_i = 0

        ### dir label...
        self.dInput = Tkinter.Label(frame, text="Directory to search:")
        self.dInput.grid(row=row_i, column=0, sticky=W)
        row_i += 1

        # dir input...
        self.dText = Tkinter.Entry(frame)
        self.dText.insert(0, self.basedir)
        self.dText.grid(row=row_i, column=0, columnspan=6, sticky=W+E+N+S, padx=5, pady=5)

        #dir change button...
        self.btnDisplay = Tkinter.Button(frame, text="Change", command=self.dir_dialog)
        self.btnDisplay.grid(row=row_i, column=7)
        row_i += 1

        ### ext label...
        self.extInput = Tkinter.Label(frame, text="Extensions to check (eg, txt), use | to include more (eg, txt|py):")
        self.extInput.grid(row=row_i, column=0, sticky=W)
        row_i += 1

        # ext input...
        self.extText = Tkinter.Entry(frame)
        self.extText.insert(0, self.ext)
        self.extText.grid(row=row_i, column=0, columnspan=6, sticky=W+E+N+S, padx=5, pady=5)
        row_i += 1

        ### find label...
        self.fInput = Tkinter.Label(frame, text="find text/regex:")
        self.fInput.grid(row=row_i, column=0, sticky=W)
        row_i += 1

        # find input...
        self.fText = Tkinter.Entry(frame)
        self.fText.insert(0, self.find)
        self.fText.grid(row=row_i, column=0, columnspan=6, sticky=W+E+N+S, padx=5, pady=5)
        row_i += 1

        ### replace label...
        self.rInput = Tkinter.Label(frame, text="Replace text:")
        self.rInput.grid(row=row_i, column=0, sticky=W)
        row_i += 1

        # replace input...
        self.rText = Tkinter.Entry(frame)
        self.rText.insert(0, self.replace)
        self.rText.grid(row=row_i, column=0, columnspan=6, sticky=W+E+N+S, padx=5, pady=5)
        row_i += 1

        # silent checkbox
        self.sText = Tkinter.IntVar()
        self.sCheck = Tkinter.Checkbutton(frame, text="Perform Silent Operation", variable=self.sText)
        self.sCheck.grid(row=row_i, column=0, columnspan=6, sticky=W, pady=5)
        if self.silent > 0:
            self.sCheck.select() # set the button to on
        row_i += 1
      
        # Submit Button...
        btnDisplay = Tkinter.Button(frame, text="OK", command=self.submit, default=ACTIVE)
        btnDisplay.grid(row=row_i, column=0)
  
    def dir_dialog(self):
        '''display a folder select dialog, record selection to class val'''
        dirname = tkFileDialog.askdirectory(initialdir=self.dText.get(),title='Please select a directory To Check')
        if len(dirname) > 0:
            self.dText.delete(0, END)
            self.dText.insert(0,dirname)
  
    def submit(self, *_, **__):
        self.tk.update()
        top_frame = Tkinter.Toplevel(self.tk) # http://www.pythonware.com/library/tkinter/introduction/dialog-windows.htm
        top_frame.transient(self.tk)

        # save new vals...
        self.basedir = self.dText.get()
        self.ext = self.extText.get()
        self.find = self.fText.get()
        self.replace = self.rText.get()
        self.silent = self.sText.get()

        # we take our passed in class instance, and invoke it here
        self.fr.find(
            self.basedir,
            self.ext,
            self.find,
            self.replace,
            self.silent,
            dialog=Dialog(top_frame),
            find_options=self.find_options,
            *self.args,
            **self.kwargs
        )
        self.tk.wait_window(top_frame)
      
    def destroy(self,event = None):
        self.tk.destroy()
  
    def save_pos(self,event = None):
        return
        #print "saving app pos"
        ##config.add('main_x',self.tk.winfo_rootx() - 4)
        ##config.add('main_y',self.tk.winfo_rooty() - 30)

    
