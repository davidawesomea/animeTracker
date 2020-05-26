#this file is for creating a profile/data for a show. it will take inputs such as length, length per season, episode length.

import os
from tkinter import Tk, Label, Button, StringVar, Entry, messagebox

if os.path.exists('Profiles') == False:
    os.mkdir('Profiles')

class Main():
    def __init__(self, master):
        
        self.master = master
        master.title("Profile Creator")
        
        self.name = StringVar()
        self.length = StringVar()
        self.eplength = StringVar()
        self.watched = StringVar()
        self.watched.set(0)

        self.l1 = Label(master, text="Anime Name")
        self.l1.pack()
        self.e1 = Entry(master, textvariable=self.name, justify='center')
        self.e1.pack()

        self.l2 = Label(master, text="Total Episodes")
        self.l2.pack()
        self.e2 = Entry(master, textvariable=self.length, justify='center')
        self.e2.pack()

        self.l3 = Label(master, text="Episode Length (Minutes)")
        self.l3.pack()
        self.e3 = Entry(master, textvariable=self.eplength, justify='center')
        self.e3.pack()

        self.l4 = Label(master, text="Episodes Watched")
        self.l4.pack()
        self.e4 = Entry(master, textvariable=self.watched, justify='center')
        self.e4.pack()
        
        self.e2 = Button(master, text = "Create", command = self.create)
        self.e2.pack()
        
    def create(self):
        banned = ['\\','/','"','*','?','<','>','|']
        legal = True
        if os.path.exists("Profiles/" + self.name.get() + ".txt"):
            messagebox.showinfo("Oops!", "This profile already exists!")
        elif set('\\/:"*?<>|').intersection(self.name.get()):
            messagebox.showinfo("Oops!", "This name contains banned characters! (\\, /, :, \", *, ?, <, >, |)")
        else:
            f=open("Profiles/" + self.name.get() + ".txt","w+")
            f.write("LENGTH:" + self.length.get() + "\n")
            f.write("EPLENGTH:" + self.eplength.get() + "\n")
            f.write("WATCHED:" + self.watched.get() + "\n")
            f.close()
            messagebox.showinfo("Success!", "This profile has been created!")

root = Tk()
root.resizable(width=False, height=False)
my_gui = Main(root)
root.geometry("250x300")
root.mainloop()
