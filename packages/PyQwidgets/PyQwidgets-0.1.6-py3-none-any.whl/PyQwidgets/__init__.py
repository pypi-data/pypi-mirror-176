from tkinter import *
from tkinter import ttk 
from tkinter import messagebox

def QError(name, text):
	# Error window
	messagebox.showerror(name, text)

def QWarning(name, text):
	# Warning window
	messagebox.showwarning(name, text)

def Info(name, text):
	# Information window
	messagebox.showinfo(name, text)

print('PyQwidgets Version 0.1.6\n')