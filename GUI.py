
from tkinter import *
from tkinter import messagebox
import random
from PIL import Image, ImageTk
import tkinter.font as font
import tkinter as tk
import time
import math
import neat,os

class square:

    def onClick(self):
        self.clicked = TRUE
        if self.flagged:
          return
        self.button.config(relief=SUNKEN)
        self.button.config(bg="green")
        
        if not self.containsbomb:
            if self.minenum==0 and not self.updated:
                self.grid.propagate(self.coordinate)
            if self.minenum!=0:
                self.button.config(text= "%d" %(self.minenum)) #display minenum when clicked
        elif self.containsbomb:
            self.button.config(bg="red")
            image = Image.open("rsz_12mine.png")
            photo = ImageTk.PhotoImage(image)
            self.button.config(image=photo,height=35,width=32)  #numbers for height and width in pixels
            self.button.image=photo
            if not self.updated:
                messagebox.showinfo("Death","Game Over")
                self.grid.update()

            
       
    def flag(self,event):
        if self.flagged:  # remove flag if square is already flagged
            self.flagged=FALSE
            self.button.config(image='',height=2,width=4)
            self.grid.addflag()
            if self.containsbomb:  #add 1 to total bomb count if unflagged a correct flag
               self.grid.addbomb()
            return
        elif self.clicked or self.grid.getflagnum()==0:
            return
        image = Image.open("rsz2flag.png")
        photo = ImageTk.PhotoImage(image)
        img = photo
        self.button.config(image=img,height=35,width=32)
        self.button.image = img
        self.flagged = TRUE
        self.grid.minusflag()
        if self.containsbomb:  # if flag is correct remove 1 from total bomb count
            self.grid.removebomb()
    def __init__(self,x,y,root,containsbomb,G,minenum):
        self.updated = FALSE # if the square is already updated to avoid infinite loop
        self.flagged = FALSE # check if the square is flagged
        self.clicked = FALSE # if the square is clicked it cannot be flagged
        self.grid=G   #all square refer to the same grid
        self.containsbomb= containsbomb
        self.coordinate=(x,y)
        self.root=root
        self.minenum = minenum
        self.button = Button(root,height=2,width=4,bd=4,fg="black",command=self.onClick)
        self.button.bind("<Button-3>", self.flag)
        self.button.grid(row=self.coordinate[0]+1,column=self.coordinate[1])
    def update(self):  #update the button
        self.updated = TRUE
        self.button.invoke()

    #some getters
    def getcontainsbomb(self):
        return self.containsbomb
    def getflagged(self):
        return self.flagged
    #some setters
    def setfalse(self):  # put red cross on flag 
        image = Image.open("redcrossflag.png")
        photo = ImageTk.PhotoImage(image)
        self.button.config(image=photo,height=35,width=32)
        self.button.image = photo

    #recursion method works together with propogate
    def unravel(self):
        if self.minenum != 0  or self.updated:
            self.button.invoke()
            return
        else:
            self.updated = TRUE
            self.button.invoke()
            self.grid.propagate(self.coordinate)


class grid:
   
    def __init__(self,bombcoordlist,bombnum):
        self.buttons = list()
        self.bombcoordlist= bombcoordlist
        self.totalbomb = bombnum
        self.flagnum = self.totalbomb
        for i in range(0,10):
            for j in range(0,10):
                arr = self.determinefg(i,j) #number of mines in surrounding 8 squares
                if (i,j) in self.bombcoordlist:
                    s = square(i,j,root,TRUE,self,arr)
                    
                else:
                    s = square(i,j,root,FALSE,self,arr)
                self.buttons.append(s)

    def determinefg(self,row,col):  #determine what number needs to be displayed based on bombs in vicinity
        
        check1 = (row+1,col+1)
        check2 = (row,col+1)
        check3 = (row-1,col+1)
        check4 = (row+1,col)
        check5 = (row+1,col-1)
        check6 = (row-1,col-1)
        check7 = (row,col-1)
        check8 = (row-1,col)
        count = 0
        checklist = [check1,check2,check3,check4,check5,check6,check7,check8]
        for check in checklist:
            if check[0]>9 or check[1]>9 or check[0]<0 or check[1]<0:  #prevent checking squares in the next row
                continue
            for bombpos in self.bombcoordlist:
                if check==bombpos:
                    count=count+1
 
        return count
        
    def update(self):
        for button in self.buttons:
            button.update()
            if button.getflagged() and not button.getcontainsbomb():  #if a flagged square doesn't contain bomb then put red cross on it
                button.setfalse()

    def addbomb(self):
        self.totalbomb+=1
    def removebomb(self):
        self.totalbomb-=1
        if self.totalbomb==0:  # check for win condition 
            messagebox.showinfo("Congrats","You Win!!")
            self.update()
    def getflagnum(self):
        return self.flagnum
    def minusflag(self):
        self.flagnum-=1
    def addflag(self):
        self.flagnum+=1
    def propagate(self,coord):
        coord1 = (coord[0]+1,coord[1])
        coord2 = (coord[0]-1,coord[1])
        coord3 = (coord[0],coord[1]+1)
        coord4 = (coord[0],coord[1]-1) 
        coord5 = (coord[0]+1,coord[1]+1)
        coord6 = (coord[0]+1,coord[1]-1)
        coord7 = (coord[0]-1,coord[1]-1)
        coord8 = (coord[0]-1,coord[1]+1)
         #propagate through all 8 squares surrounding the target square
        coords = [coord1,coord2,coord3,coord4,coord5,coord6,coord7,coord8]
          
        for coordinate in coords:
            if coordinate[0] < 0 or coordinate[0] > 9 or coordinate[1] < 0 or coordinate[1] > 9:
                continue
            self.buttons[coordinate[0]*10+coordinate[1]].unravel()
class minesweep:    
    def __init__(self):
        global root
        root = Tk()
        self.startime = time.time()   # used for timer
        self.w = tk.Label(root, bg="red", fg="white",height=10)
        self.w.grid(row=0,columnspan=10)
        self.update_clock()
        bombcoordlist = list()
        bombnum = 10
        while len(bombcoordlist)<bombnum:
            xcoord=random.randint(0,9)
            ycoord=random.randint(0,9)
            bombpos = (xcoord,ycoord)
            if bombpos not in bombcoordlist:  # append bomb position to the list if it doesn't already exist in the list
                bombcoordlist.append(bombpos)  
        global starttime
        starttime = time.time()
        grid(bombcoordlist,bombnum)
        root.mainloop()
    def update_clock(self):
            now = time.time()
            seconds = now-self.startime
            minutes = str(math.floor(seconds/60)).zfill(2)
            seconds = str(round(seconds%60)).zfill(2)
            self.w.configure(text="%s:%s"%(minutes,seconds))   #display the time
            root.after(1000, self.update_clock)  # every one second updates the clock

minesweep()




