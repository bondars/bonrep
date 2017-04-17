# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 12:47:15 2017

@author: sbondar
"""
import re

class IPAdd():
    def __init__(self,inp):
        """
        Objects of this class are the IP addresses
        Input is a tuple, consists of:
        inp[0] - a tupple of 4 integers between 0 and 255 - IP address
        inp[1] - a tupple of 4 integers between 0 and 255 - Subnet mask
        inp[2] - integer from 0 to 32 - prefix length
        """
        self.addr = inp[0]
        self.mask = inp[1]
        self.pref = inp[2]
        #The number of hosts
        self.numhosts = self.calcnumhosts(inp[2])
        #The subnet address
        self.subnet = tuple(inp[0][x]&inp[1][x] for x in range(4))
        #The directed broadcast address
        self.bcast = tuple(self.subnet[x] | (~self.mask[x] & 0xFF) for x in range(4))
        #The first usable IP
        self.firsthost = list(self.subnet)
        #Special case - if the prefix length is 31 or 32, the first usable IP
        #equals the subnet addres
        if self.pref != 31 and self.pref != 32:
            self.firsthost[3] += 1
        self.firsthost = tuple(self.firsthost)
        #The last usable IP
        #Special case - if the prefix length is 31, the last usable IP
        #equals the subnet addres. If the prefix length is 32, the last usable
        #IP equals the directed broadcast address
        if self.pref == 32:
            self.lasthost = self.addr
        elif self.pref == 31:
            self.lasthost = self.bcast
        else:
            self.lasthost = list(self.bcast)
            self.lasthost[3] -= 1
            self.lasthost = tuple(self.lasthost)

    def __iter__(self):
        return iter(self.addr)
        
    def iterMask(self):
        return iter(self.mask)

    def __next__(self):
        return next(self.addr)

    def __getitem__(self,index):
        return self.addr[index]
    
    def getMask(self,index):
        return self.mask[index]
        
    def getPref(self):
        return self.pref
        
    def getNumHosts(self):
        return self.numhosts
        
    def getSubnet(self):
        return self.subnet()
        
    def getBcast(self):
        return self.bcast
        
    def getFirstHost(self):
        return self.firsthost
        
    def getLastHost(self):
        return self.lasthost
        
    def iterSubnet(self):
        return iter(self.subnet)
        
    def iterBcast(self):
        return iter(self.bcast)
        
    def iterFirstHost(self):
        return iter(self.firsthost)
        
    def iterLastHost(self):
        return iter(self.lasthost)

    @staticmethod
    def calcnumhosts(pref):
        """Calculate a number of hosts in the subnet"""
        #Special case - if the prefix length is 31, we have two usable addresses,
        #if the prefix length is 32, we have one usable address
        if pref == 31:
            numh = 2
        elif pref == 32:
            numh = 1
        else:
            numh = (2 ** (32 - pref)) - 2
        return numh
        
class Inpt():
    """
    Objects of this calss are the input provided by the user.
    They are used to validate the input and get the IP address and the
    subnet mask or the prefix length from the input
    
    inp is a string the contains an IP address and a subnet mask/prefix length
    """
    def __init__(self,inp):
        self.inp = inp
        self.correct = False
        #addrtype is 1 if inout contains the mask and 2 if input contains the
        #prefix length
        self.addrtype = 0
        self.findaddr()
    
    def findaddr(self):
        """ Find IP address, subnet mask, or prefix
        in the input and check the overall sanity
        """
        #First, check the format of the input and find the address using regexp
        ptrn1 = r"[0-9]?[0-9]?[0-9]\.[0-9]?[0-9]?[0-9]\.[0-9]?[0-9]?[0-9]\.[0-9]?[0-9]?[0-9]\s+[0-9]?[0-9]?[0-9]\.[0-9]?[0-9]?[0-9]\.[0-9]?[0-9]?[0-9]\.[0-9]?[0-9]?[0-9]"
        ptrn2 = r"[0-9]?[0-9]?[0-9]\.[0-9]?[0-9]?[0-9]\.[0-9]?[0-9]?[0-9]\.[0-9]?[0-9]?[0-9]/[0-9]?[0-9]"
        mtch1 = re.search(ptrn1,self.inp)
        mtch2 = re.search(ptrn2,self.inp)
        #The format can be 1 - with mask or 2 - with pref length
        if mtch1:
            self.addrtype = 1
            #Find the address and the mask part and turn them into tuples of integers
            str1 = mtch1.group(0)
            mtch3 = re.search("\s+",str1)
            addrl = str1[:mtch3.start(0)].split(".")
            maskl = str1[mtch3.end(0):].split(".")
            addr = tuple(int(x) for x in addrl)
            mask = tuple(int(x) for x in maskl)
            #Check that te input is correct and if yes, calculate the prefix
            #and create the tuplle to supply as input for the IPAdd object
            self.correct = self.check(self.addrtype,addr,mask)
            if self.correct:
                pref = self.calcpref(mask)
                self.ipaddr = (addr,mask,pref)                            
        elif mtch2:
            self.addrtype = 2
            #Find the address and the prefix part and turn them into integers 
            #address is still a tuple
            str1 = mtch2.group(0)
            mtch3 = re.search(r"/",str1)
            addrl = str1[:mtch3.start(0)].split(".")
            prefstr = str1[mtch3.end(0):]
            addr = tuple(int(x) for x in addrl)
            pref = int(prefstr)
            #Check that te input is correct and if yes, calculate the mask
            #and create the tuplle to supply as input for the IPAdd object            
            self.correct = self.check(self.addrtype,addr,pref)
            if self.correct:
                mask = self.calcmask(pref)
                self.ipaddr = (addr,mask,pref)
        else:
            #If the regexp soesn't find the address in either format,
            #we have an incorrect input
            self.correct = False
            self.ipaddr = (None,None,None)

    def getaddr(self):
        """Get IP address, subnet mask and prefix length as a tuple"""
        return self.ipaddr
        
    def iscorrect(self):
        if self.correct:
            return True
        else:
            return False

    @staticmethod
    def check(addrtype,addr,mask):
        """
        Check the IP address, subnet mask and prefix
        returns True if all three are correct
        returns False otherwise
        """
        correctaddr = True
        correctmask = True
        #If we have input with the mask
        if addrtype == 1:
            maskbinl = []
            #Any aprt of the IP address tuple can't be greater than 255
            for x in addr:
                if x > 255:
                    correctaddr = False
            #Any aprt of the mask tuple can't be greater than 255
            for x in mask:
                if x > 255:
                    correctmask = False
                maskbinl.append(bin(x)[2:].zfill(8))
            #Transform mask into a binary srting, the string should contain
            #strictly 1s than 0s, any other combination is not valid
            maskbinstr = "".join(maskbinl)
            mtch4 = re.match(r"1+0+1+",maskbinstr)
            if mtch4:
                correctmask = False
        #If we have input with the prefix length
        elif addrtype == 2:
            #Any aprt of the IP address tuple still can't be greater than 255
            for x in addr:
                if x > 255:
                    correctaddr = False
            #The prefix length can't be greater than 32
            if mask > 32:
                correctmask = False
        else:
            correctaddr = False
            correctmask = False
        #Only if both the address and the mask/prefix are correct,
        #we return True. Otherwise False.
        if correctaddr and correctmask:
            return True
        else:
            return False

    @staticmethod
    def calcpref(mask):
        """
        Calculate prefix length from given subnet mask
        input is a tuple containing a subnet mask (A,B,C,D)
        returns an integer from 0 to 32        
        """
        pref = 0
        #Prefix length is just a number of consecutine 1s in the mask
        #Mask is transformed onto a bit string
        binlst = [(bin(x)[2:].zfill(8)) for x in mask]
        binmask = "".join(binlst)
        #And then we count the 1s
        for x in binmask:
            if x == "1":
                pref += 1
        return pref

    @staticmethod
    def calcmask(pref):
        """
        Calculate a subnet mask from given prefix length
        input is an integer from 0 to 32
        returns a tuple containing a subnet mask (A,B,C,D)
        """
        #Prefix length is just a number of consecutine 1s in the mask
        maskbin = list()
        maskbinl = list()
        #We create the bin string for the mask, with first the number of 1s
        #equal to the prefix length, and then pad 0s untill the length of 32
        for x in range(32):
            if x < pref:
                maskbinl.append("1")
            else:
                maskbinl.append("0")
        maskbinstr = "".join(maskbinl)
        #Then we break it into the chinks of 8 bits and convert them
        #into a tuple of integers
        for x in range(4):
            maskbin.append(maskbinstr[x*8:(x+1)*8])
        mask = tuple(int(x,2) for x in maskbin)                        
        return mask
