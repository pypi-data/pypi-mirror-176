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

def QInfo(name, text): # New information window 
	Icon = 'Icon.ico'

	root = Tk()
	root.iconbitmap(Icon)
	root.title(name)
	root.config(bg='white')
	root.geometry('400x200+500+250')
	root.resizable(0, 0)

	def exit():
		root.destroy()

	label = Label(root, text=text, bg='white', font='Arial 11')
	label.place(relx=0.5, y=90, anchor=CENTER)
	
	btn = ttk.Button(root, text='Понятно', command=exit)
	btn.place(relx=0.5, y=180, anchor=CENTER)
	
	root.mainloop()