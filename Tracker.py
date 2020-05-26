import os
import tempfile
import shutil
from tkinter import Tk, Label, Button, StringVar, OptionMenu, Frame, PhotoImage, messagebox

if os.path.exists("Profiles") == True:
    profiles = [f[:len(f)-4] for f in os.listdir("Profiles") if os.path.isfile(os.path.join("Profiles", f))]
else:
    messagebox.showinfo("Oops!", "Please run \"Create.exe\" first!")
    destroy()
config = []
if os.path.isfile("config.txt") == False:
    with open("config.txt","w") as f:
        f.write("#0=MINUTES 1=HOURS,MINUTES 2=HOURS\n")
        f.write("TIMEFORMAT:0\n")
        f.close()
with open("config.txt") as f:
    for line in f:
        if len(line) > 0 and line[0] != '#':
            name, value = line.split(":")
            config.append((name, int(value)))
for item in config:
    if item[0] == 'TIMEFORMAT':
        timeFormat = item[1]

class Main():
    def __init__(self, master):
        global profiles
        
        self.master = master
        master.title("Anime Tracker")

        topFrame = Frame(master,width=300,height=250)
        topFrame.grid()
        bottomFrame = Frame(master)
        bottomFrame.grid()

        if os.path.isfile("bg.png") == True:
            background_image=PhotoImage(file="bg.png")
            background_label=Label(master,image=background_image)
            background_label.photo=background_image
            background_label.place(x=0,y=0,relwidth=1,relheight=1)

        self.eps = StringVar(master)
        self.time = StringVar(master)

        self.var = StringVar(master)
        self.var.trace("w", self.crawl)
        self.var.set(profiles[0])
        o = OptionMenu(master, self.var, *profiles)
        o.grid(sticky='s',pady=5,column=0,row=0)

        self.l1 = Label(master, textvariable = self.eps)
        self.l1.grid(column=0,row=1,pady=2,sticky='s')
        
        self.l2 = Label(master, textvariable = self.time)
        self.l2.grid(column=0,row=2,pady=2,sticky='s')

        self.b = Button(master, text = "+1", command = self.add)
        self.b.grid(column=0,row=3,pady=10)

    def crawl(self, *args):
        global timeFormat
        
        for i in range(len(profiles)):
            if profiles[i] == self.var.get():
                f = open("Profiles/" + profiles[i] + ".txt","r")
        data = []
        for line in f:
            if len(line) > 0 and line[0] != '#':
                linesplit = line.split(":")
                data.append(linesplit[1][:len(linesplit[1])-1])
        f.close()
        complete = False
        if int(data[0])-int(data[2]) == 0:
            complete = True
        if complete == True:
            epsvar = "Complete!)"
            timevar = "Complete!)"
        else:
            epsvar = str(int(data[0])-int(data[2])) + " remaining)"
            if timeFormat == 0:
                timevar = str((int(data[0])*int(data[1]))-(int(data[1])*int(data[2]))) + " remaining)"
            elif timeFormat == 1:
                timevar = str(int(((int(data[0])*int(data[1]))-(int(data[1])*int(data[2])))/60)) + " hours " + str(((int(data[0])*int(data[1]))-(int(data[1])*int(data[2])))%60) + " minutes remaining)"
            elif timeFormat == 2:
                timevar = str(((int(data[0])*int(data[1]))-(int(data[1])*int(data[2])))/60) + " hours remaining)"
        self.eps.set(data[2] + '/' + data[0] + " episodes watched (" + epsvar)
        if timeFormat == 0:
            self.time.set(str(int(data[1])*int(data[2])) + "/" + str(int(data[0])*int(data[1])) + " minutes watched (" + timevar)
        elif timeFormat == 1:
            self.time.set(str(int(int(data[1])*int(data[2])/60)) + "h" + str(int(data[1])*int(data[2])%60) + "m/" + str(int(int(data[0])*int(data[1])/60)) + "h" + str(int(data[0])*int(data[1])%60) + "m (" + timevar)
        elif timeFormat == 2:
            self.time.set(str(int(data[1])*int(data[2])/60) + "h/" + str(int(data[0])*int(data[1])/60) + "h (" + timevar)

    def add(self):
        all_data = []

        with open("Profiles/" + self.var.get() + ".txt") as f:
            for line in f:
                name, value = line.split(":")
                all_data.append((name, int(value)))
        a=all_data[0]
        b=all_data[2]
        if a[1] == b[1]:
            messagebox.showinfo("Oops!", "This is already complete!")
        else:
            if os.path.exists('temp') == False:
                os.mkdir('temp')
            with tempfile.NamedTemporaryFile(mode='w', delete=False, dir="temp") as f:
                for name, value in all_data:
                    if name == "WATCHED":
                        print(f"{name}:{value + 1}", file=f)
                    else:
                        print(f"{name}:{value}", file=f)
            os.replace(f.name, "Profiles/" + self.var.get() + ".txt")
            self.crawl
            shutil.rmtree('temp')
            self.var.set(self.var.get())

root = Tk()
root.resizable(width=False, height=False)
my_gui = Main(root)
root.mainloop()
