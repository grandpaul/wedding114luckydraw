#!/usr/bin/env python
import hashlib
import logging
import Tkinter as tk
import ttk
import tkFont


class ApplicationSecretString(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        self.font1 = tkFont.Font(size=64)
        self.createWidgets()

    def createWidgets(self):
        top=self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.columnconfigure(0, weight=1)

        self.label1 = tk.Label(self, text='Secret string hash', font=self.font1)
        self.label1.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        secrettext = ''
        try:
            secretfile = open('secret.txt', 'r')
            secrettext = secretfile.read()
        except:
            pass
        
        text2 = hashlib.sha256(secrettext.strip()).hexdigest()
        self.label2 = tk.Label(self, text=text2[0:16], font=self.font1)
        self.label2.grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.label3 = tk.Label(self, text=text2[16:32], font=self.font1)
        self.label3.grid(row=2, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.label4 = tk.Label(self, text=text2[32:48], font=self.font1)
        self.label4.grid(row=3, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.label5 = tk.Label(self, text=text2[48:64], font=self.font1)
        self.label5.grid(row=4, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

class ApplicationPublicRandom(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        self.font1 = tkFont.Font(size=64)
        self.createWidgets()

    def onKeyRelease(self, event):
        publicrandomfile = None
        publicrandom = ''
        try:
            publicrandomfile = open('publicrandom.txt', 'w')
        except:
            pass

        if (publicrandomfile != None):
            publicrandom = self.textarea.get("1.0",tk.END)
            publicrandomfile.write(publicrandom.strip())
        
        if (publicrandomfile != None):
            publicrandomfile.close()
        
    def createWidgets(self):
        top=self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        publicrandomfile = None
        publicrandom = ''
        try:
            publicrandomfile = open('publicrandom.txt', 'r')
            publicrandom = publicrandomfile.read().strip()
        except:
            pass

        if (publicrandomfile != None):
            publicrandomfile.close()
    
        self.textarea = tk.Text(self, font=self.font1)
        self.scrollbar = ttk.Scrollbar(self)
        self.scrollbar.config(command=self.textarea.yview)
        self.textarea.config(yscrollcommand=self.scrollbar.set)
        self.textarea.bind('<KeyRelease>', self.onKeyRelease)

        self.textarea.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.scrollbar.grid(row=0, column=1)

        self.textarea.insert(tk.INSERT,publicrandom)

class ApplicationDraw(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        self.font1 = tkFont.Font(size=90)
        self.counter = 0
        self.N = 150
        self.createWidgets()

    def calculateNumber(self, c):

        secrettext = ''
        try:
            secretfile = open('secret.txt', 'r')
            secrettext = secretfile.read()
            secretfile.close()
        except:
            pass
        
        text2 = secrettext.strip()

        try:
            publicrandomfile = open('publicrandom.txt', 'r')
            publicrandom = publicrandomfile.read().strip()
            text2 = text2 + publicrandom
            publicrandomfile.close()
        except:
            pass

        value1 = 0

        if (c <= 0 or c>self.N):
            return 0


        logfile = open('log.txt', 'w')
        
        seed = text2
        list1 = []

        while (c>0):
            logfile.write("Seed = %s\n"%(seed))
            sha512sum = hashlib.sha512(seed).hexdigest()
            logfile.write("sha512(seed) = 0x%s = %d\n"%(sha512sum,int(sha512sum, 16)))
            value1 = int(sha512sum, 16) % self.N + 1
            logfile.write("%d mod %d + 1 = %d\n"%(int(sha512sum, 16), self.N, value1))
            if (not(value1 in list1)):
                list1.append(value1)
                c = c-1
                logfile.write("Lucky number: %d\n"%(value1));
                logfile.write("-------------------------------------\n")
            else:
                logfile.write("%d is already drawn\n"%(value1));
            seed = sha512sum

        logfile.close()
        return value1

    def createWidgets(self):
        top=self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.label1var = tk.StringVar()
        self.label1 = tk.Label(self, textvariable=self.label1var, font=self.font1)
        self.label1var.set("%s"%(self.calculateNumber(self.counter)))
        self.label1.grid(row=0, column=0, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)

        self.button1 = tk.Button(self, text='Prev', font=self.font1, command=self.subCounter)
        self.button1.grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.button2 = tk.Button(self, text='Next', font=self.font1, command=self.addCounter)
        self.button2.grid(row=1, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

    def addCounter(self):
        if (self.counter < self.N):
            self.counter = self.counter + 1
        self.label1var.set("%s"%(self.calculateNumber(self.counter)))

    def subCounter(self):
        if (self.counter > 0):
            self.counter = self.counter - 1
        self.label1var.set("%s"%(self.calculateNumber(self.counter)))
        
        
        

class Application01(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        self.createWidgets()
        
    def createWidgets(self):
        top=self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.notebook_top = ttk.Notebook(self)
        self.notebook_top.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        self.frame1 = ApplicationSecretString()
        self.notebook_top.add(self.frame1, text='Secret string hash')
        self.frame2 = ApplicationPublicRandom()
        self.notebook_top.add(self.frame2, text='Public random string')
        self.frame3 = ApplicationDraw()
        self.notebook_top.add(self.frame3, text='Draw')




app = Application01()
app.master.title('Sample application')   
app.mainloop()  
