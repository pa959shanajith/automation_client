#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      wasimakram.sutar
#
# Created:     29-08-2016
# Copyright:   (c) wasimakram.sutar 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------



from Tkinter import *
import Tkinter


import threading

##import logger


class App():
   def __init__(self):
       self.root = Tkinter.Tk()
       self.root.title( 'SLK Nineteen68 - Pause')
##       win = Tkinter.Toplevel(self.root)
       self.root.geometry("300x150")
##       self.root.iconbitmap(default='C:\Users\wasimakram.sutar\Desktop\ForLoggers\Nineteen68\Nineteen68\plugins\Core\slk.ico')
       button = Tkinter.Button(self.root, text = 'OK',   command=self.quit,width= 100, height = 50)
##       button.place(relx=6.5, rely=6.5,)
##       button.place(bordermode=OUTSIDE, height=100, width=100)

       button.pack()
       self.center(self.root)
       self.root.mainloop()

   def quit(self):
       self.root.destroy()
       self.root = None

   def center(self,toplevel):
        toplevel.update_idletasks()
        w = toplevel.winfo_screenwidth()
        h = toplevel.winfo_screenheight()
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))


def execute():
    app = App()




class App2():
   def __init__(self,input):
        self.w = Tkinter.Tk()
        self.w.title( 'SLK Nineteen68 - DisplayVariable')
        self.w.geometry("300x150")
        self.w.iconbitmap(default='C:\Users\wasimakram.sutar\Desktop\ForLoggers\Nineteen68\Nineteen68\plugins\Core\slk.ico')
        label = Label(self.w, text=input )
        label.pack()
        button = Tkinter.Button(self.w, text = 'OK', command = self.quit,  width= 100, height = 50)
        button.pack()
        self.center(self.w)
        self.w.after(10000, lambda: self.w.destroy()) # Destroy the widget after 30 seconds
        self.w.mainloop()

   def quit(self):
       self.w.destroy()

   def center(self,toplevel):
        toplevel.update_idletasks()
        w = toplevel.winfo_screenwidth()
        h = toplevel.winfo_screenheight()
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))



def display_value(input):
    app = App(input)








