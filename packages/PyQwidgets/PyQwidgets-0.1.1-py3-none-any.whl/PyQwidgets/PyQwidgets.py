from tkinter import *
from tkinter import messagebox

def QError(name, text):
	messagebox.showerror(name, text)

def QWarning(name, text):
	messagebox.showwarning(name, text)

def QInfo(name, text):
	messagebox.showinfo(name, text)

print('PyQwidgets Version 0.1.1')