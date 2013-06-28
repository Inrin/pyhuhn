#!/usr/bin/python

##############################################################################
##                               Imports                                    ##
##############################################################################

from tkinter import *
from random import randint

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

def populateMoorhens(howmany):
    """Generates random moorhens"""
    moorhens = []
    for i in range(howmany):
        rands = randint(0, 1)
        randy = randint(0, 600)
        if rands == 0:
            moorhens.append( 
                                                #x0, y0,  x1,   y2
                    canvasGameWorld.create_rectangle(0, randy, 50, randy + 50, 
                        fill='gray', tags='left')
                )
        elif rands == 1:
            moorhens.append( 
                        canvasGameWorld.create_rectangle(1000, randy, 950, randy + 50, 
                            fill='gray', tags='right')
                )
    return moorhens

def run():
    """main method for animation(Like in Greenfoot)"""
## Update screen
    root.update_idletasks()
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
moorhen = canvasGameWorld.create_rectangle(0, 50, 50, 100, fill='gray')

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
