#!/usr/bin/python

##############################################################################
##                               Imports                                    ##
##############################################################################

from tkinter import *
from random import randint

###############################################################################
##                                Definitons                                 ##
###############################################################################

def moorhenClicked(event):
    """Kill moorhen"""
    hideUnderCursor(event.widget)

def hideUnderCursor(canvas):
    """Hide item under cursor"""
## Hide our victim
    canvas.itemconfig(CURRENT, state='hidden')
## Remove the `left' or `right' fying tag to stop it
    canvas.dtag(CURRENT, 'left')
    canvas.dtag(CURRENT, 'right')

def destroyAll():
    """Destroy item under cursor and free memory"""
    canvasGameWorld.destroy(ALL)

def populateMoorhens(howmany):
    """Generates random moorhens for game init only reuse existing later"""
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

def moveMoorhens():
    """Move Moorhens in a straight line"""
    for i in range(len(moorhens)):
## Move them from left -> right
        if moorhens[i] in canvasGameWorld.find_withtag('left'):
            canvasGameWorld.move(moorhens[i], 5, 0)
## Move them from right -> left 
        elif moorhens[i] in canvasGameWorld.find_withtag('right'):
            canvasGameWorld.move(moorhens[i], -5, 0)

def run():
    """main method for animation(Like in Greenfoot)"""
## Let's move it
    moveMoorhens()
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

## Generate 3 Moorhens, first only for debugging
moorhens = populateMoorhens(3)
run()
root.mainloop()
