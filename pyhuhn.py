#!/usr/bin/python

##############################################################################
##                               Imports                                    ##
##############################################################################

from tkinter import *
from random import randint
## To negate integers
from operator import neg

###############################################################################
##                                Definitons                                 ##
###############################################################################

def moorhenClicked(event):
    """Kill moorhen"""
    hideUnderCursor(event.widget)

def hideUnderCursor(canvas):
    """Hide item UNDer cursor"""
## Hide our victim
    canvas.itemconfig(CURRENT, state='hidden')
## Remove the `left' or `right' fying tag to stop it
    canvas.dtag(CURRENT, 'left')
    canvas.dtag(CURRENT, 'right')
## Add `hidden' tag to specify that it is hidden
    canvas.addtag('hidden', 'withtag', CURRENT)
## For killed got one Hit
    for i in moorhens:
        if CURRENT in canvasGameWorld.gettags(i):
            updateHits()
            break
## Executes if for doesn't breaks
    else:
        updateMisses()

def stop(who):
    """Stop who"""
    canvasGameWorld.dtag(who, 'left')
    canvasGameWorld.dtag(who, 'right')

def hideAndStopEscaped():
    """hide and stop escaped to save resources"""
## Abbreviate for better readability
    find = canvasGameWorld.find_withtag
## Save left and right flying moorhens
    movingMoorhens = find('left') + find('right')
    
## If behind world, hide and stop
    for i in movingMoorhens:
        if behindWorldEdge(i):
            hideAndStop(i)
    
def hideAndStop(who):
    """Hide item who and stop"""
## Hide our victim
    canvasGameWorld.itemconfig(who, state='hidden')
## Add `hidden' tag to specify that it is hidden
    canvasGameWorld.addtag('hidden', 'withtag', who)
    stop(who)

def unhide(who):
    """Unhide who"""
## Unhide our hen
    canvasGameWorld.itemconfig(who, state='normal')
## Remove `hidden' tag to specify that it is not hidden
    canvasGameWorld.dtag(who, 'hidden')

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
                        fill='gray', tags=('left', 'hen'))
                )
        elif rands == 1:
            moorhens.append( 
                        canvasGameWorld.create_rectangle(1000, randy, 950, randy + 50, 
                            fill='gray', tags=('right', 'hen'))
                )
    return moorhens

def reviveMoorhens():
    """Revive killed or escaped moorhens"""
## Get hidden(killed or escaped moorhens)
    hiddenMoorhens = canvasGameWorld.find_withtag('hidden')
    for i in hiddenMoorhens:
        rands = randint(0, 1)
        randy = randint(0, 600)
        if rands == 0:
## Place it on start
            canvasGameWorld.coords(i, 0, randy, 50, randy + 50)
## Make it visible
            unhide(i)
## Let it move again
            canvasGameWorld.addtag('left', 'withtag', i)
        elif rands == 1:
            canvasGameWorld.coords(i, 1000, randy, 950, randy + 50)
            unhide(i)
            canvasGameWorld.addtag('right', 'withtag', i)

def behindWorldEdge(who):
    """Checks if who is at worlds edge"""
    x0 = canvasGameWorld.coords(moorhens[0])[0]
    x1 = canvasGameWorld.coords(moorhens[0])[2]
    y0 = canvasGameWorld.coords(moorhens[0])[1]
    y1 = canvasGameWorld.coords(moorhens[0])[3]

    if x0 < 0 and x1 < 0:
        return True
    elif y0 < 0 and y1 < 0:
        return True
    elif x0 > 1000 and x1 > 1000:
        return True
    elif y0 > 1000 and y1 > 1000:
        return True
    else:
        return False

def moveMoorhens():
    """Move Moorhens in a straight line"""
    for i in range(len(moorhens)):
## Move them from left -> right
        if moorhens[i] in canvasGameWorld.find_withtag('left'):
            canvasGameWorld.move(moorhens[i], 5, 0)
## Move them from right -> left 
        elif moorhens[i] in canvasGameWorld.find_withtag('right'):
            canvasGameWorld.move(moorhens[i], -5, 0)

def updateHits():
    """Update the display of hits"""
## Get current hits, reading text
    currentHits = canvasGameWorld.itemcget('hits', 'text')
## Just get the hits suffix -> The ints
## int = string[afterSpace:toEnd]
    currentHitsAsInt = int(currentHits[currentHits.index(' ') + 1 :
        len(currentHits)]) + 1
## Convert the int back to string
    canvasGameWorld.itemconfig('hits', text='Hits: ' + str(currentHitsAsInt))

def updateMisses():
    """Exactly like updateHits, but for misses"""
    currentHits = canvasGameWorld.itemcget('misses', 'text')
    currentHitsAsInt = int(currentHits[currentHits.index(' ') + 1 :
        len(currentHits)]) + 1
    canvasGameWorld.itemconfig('misses', text='Misses: ' + str(currentHitsAsInt))

def run():
    """main method for animation(Like in Greenfoot)"""
## Hide and stop moorhens out of world edges
    hideAndStopEscaped()
## Revive dead and escaped moorhens
    reviveMoorhens()
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

## Binding to mouse, remember: CURRENT == item under cursor
canvasGameWorld.bind('<ButtonPress-1>', moorhenClicked)

## print Hits
canvasGameWorld.create_text(950, 10, tags='hits', text='Hits: 0') 
## print Misses
canvasGameWorld.create_text(850, 10, tags='misses', text='Misses: 0') 

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
