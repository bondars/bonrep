# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 21:20:01 2017

@author: sbondar
"""
import tkinter as tk
import ipaddr

class Application(tk.Frame):
    """
    This is the application itself
    All the logic behind finding the subnets is in the ipaddr.py
    """    
    def __init__(self, master=None):
        #Draw the app window qnd the UI
        super().__init__(master)
        self.pack()
        self.input = ""
        self.create_widgets()
        self.master.minsize(300,250)
        self.master.title("Subnet Calc v1.0")


    def create_widgets(self):
        """ Draw the GUI elements and assigns actions to them """
        self.quit = tk.Button(self, text="QUIT",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")
        self.inpt = tk.Entry(self,width=60)
        self.inpt.bind("<Return>",self.pressenter)
        self.inpt.pack(side = "top")
        self.calc = tk.Button(self, text = "Calculate",
                                command = self.calculate)
        self.calc.pack(side = "top")
        self.txt = tk.Text(self, height=20, width=70, state = "disabled")
        self.txt.pack(side="left")
        self.scroll = tk.Scrollbar(self)
        self.scroll.pack(side="right", fill = tk.Y)
        self.scroll.config(command = self.txt.yview)
        self.txt.config(yscrollcommand = self.scroll.set)

    def pressenter(self,event):
        """ Function handling the Enter key """
        self.calculate()

    def calculate(self):
        """
        Creates the Inpt and IPAdd objects and then initiates the output
        """
        
        self.input = self.inpt.get()
        self.inobj = ipaddr.Inpt(self.input)
        if self.inobj.iscorrect():
            self.inaddr = ipaddr.IPAdd(self.inobj.getaddr())
            self.inpt.delete(0,tk.END)
            self.output1()
        else:
            self.inpt.delete(0,tk.END)
            self.output2()            

    def output1(self):
        """ Shows the output if the input is correct """
        addr = [str(x) for x in self.inaddr]
        mask = [str(x) for x in self.inaddr.iterMask()]
        pref = self.inaddr.getPref()
        numhosts = self.inaddr.getNumHosts()
        subnet = [str(x) for x in self.inaddr.iterSubnet()]
        bcast = [str(x) for x in self.inaddr.iterBcast()]
        fh = [str(x) for x in self.inaddr.iterFirstHost()]
        lh = [str(x) for x in self.inaddr.iterLastHost()]
        otpl = ["Input IP address: {}","Input subnet mask: {}"]
        otpl.append("Input prefix length: {}")
        otpl.append("Subnet address: {}")
        otpl.append("Directed Broadcast address: {}")
        otpl.append("Number of hosts in subnet: {}")
        otpl.append("First usable address: {}")
        otpl.append("Last usable address: {}")
        otpt = "\n".join(otpl).format(".".join(addr),".".join(mask),pref,".".join(subnet),".".join(bcast),numhosts,".".join(fh),".".join(lh))
        self.txt.configure(state = "normal")
        self.txt.insert(tk.END,"{:=^70}".format(""))
        self.txt.insert(tk.END,otpt)
        self.txt.insert(tk.END,"\n")
        self.txt.configure(state = "disabled")
        
    def output2(self):
        """ Shows the output if the input is incorrect """
        otpt = "Incorrect input. Please enter an IP address as A.B.C.D X.Y.Z.W or A.B.C.D/nn"
        self.txt.configure(state = "normal")
        self.txt.insert(tk.END,"{:=^70}".format(""))
        self.txt.insert(tk.END,otpt)
        self.txt.insert(tk.END,"\n")
        self.txt.configure(state = "disabled")
        
if __name__ == "__main__":        
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()