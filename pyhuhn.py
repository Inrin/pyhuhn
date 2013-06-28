#!/usr/bin/python

##############################################################################
##                               Imports                                    ##
##############################################################################

from tkinter import *

##############################################################################
##                               Definitons                                 ##
##############################################################################

def moorhenClicked(event):
    """Kill moorhen"""
    hideUnderCursor(event.widget)

def hideUnderCursor(canvas):
    """Hide item under cursor"""
    canvas.itemconfig(CURRENT, state='hidden')

def destroyAll():
    """Destroy item under cursor and free memory"""
    canvasGameWorld.destroy(ALL)

def populateMoorhens():
    """Generates random moorhens"""
    pass

def run():
    """main method for animation(Like in Greenfoot)"""
## Update screen
    root.update()
## Execute main method after 100ms
    root.after(100, run) 

##############################################################################
##                              GUI ~Creation                               ##
##############################################################################

root = Tk()
root.title('Pyhuhn')
root.geometry('1000x600')

##############################################################################
##                                Images                                    ##
##############################################################################

''' Insert your pictures here '''

##############################################################################
##                                 Canvas                                   ##
##############################################################################

canvasGameWorld = Canvas(root, bg='white', closeenough=1.0, 
        width=1000, height=600)

## Create a moorhen, for debugging only
moorhen = canvasGameWorld.create_rectangle(10, 10, 50, 50, fill='gray')

## Binding to mouse, remember: CURRENT == item under cursor
canvasGameWorld.bind('<ButtonPress-1>', moorhenClicked)

##############################################################################
##                                Layout                                    ##
##############################################################################

## Placing our Canvas  on the window
canvasGameWorld.pack()

##############################################################################
##                                Starting                                  ##
##############################################################################

run()
root.mainloop()
