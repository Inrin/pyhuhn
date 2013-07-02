#!/usr/bin/python

##############################################################################
##                               Imports                                    ##
##############################################################################

from tkinter import *
from random import randint
## Get OS
import os

###############################################################################
##                                Definitons                                 ##
###############################################################################

def moorhenClicked(event):
    """Kill moorhen"""
    shot()

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
    canvasGameWorld.delete(ALL)

def populateMoorhens(howmany):
    """Generates random moorhens for game init only reuse existing later"""
    moorhens = []
    for i in range(howmany):
        rands = randint(0, 1)
        randy = randint(0, 500)
        if rands == 0:
            moorhens.append( 
                    canvasGameWorld.create_image(50, randy,
                        image=imageMoorhenLeft, tags=('left', 'hen'))
                )
        elif rands == 1:
            moorhens.append( 
                        canvasGameWorld.create_image(950, randy, 
                            image=imageMoorhenRight, tags=('right', 'hen'))
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
            canvasGameWorld.coords(i, 50, randy)
## Make it visible
            unhide(i)
## Let it move again
            canvasGameWorld.addtag('left', 'withtag', i)
            canvasGameWorld.itemconfig(i, image=imageMoorhenLeft)
        elif rands == 1:
            canvasGameWorld.coords(i, 950, randy)
            unhide(i)
            canvasGameWorld.addtag('right', 'withtag', i)
            canvasGameWorld.itemconfig(i, image=imageMoorhenRight)

def behindWorldEdge(who):
    """Checks if who is at worlds edge"""
    x0 = canvasGameWorld.coords(moorhens[0])[0]
    y0 = canvasGameWorld.coords(moorhens[0])[1]

    if x0 < 0:
        return True
    elif y0 < 0:
        return True
    elif x0 > 1000 :
        return True
    elif y0 > 1000:
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

def updateTime():
    """Updating remaining time"""
    currentTime = canvasGameWorld.itemcget('time', 'text')
    currentTimeAsFloat = float(currentTime[currentTime.index(' ') + 1 :
        len(currentTime)]) - 0.1
    canvasGameWorld.itemconfig('time', text='Time: {:10.2f} '.format(currentTimeAsFloat))
    gameOver()

def gameOver():
    """Game over, eh?"""
    currentTime = canvasGameWorld.itemcget('time', 'text')
    currentTimeAsFloat = float(currentTime[currentTime.index(' ') + 1 :
        len(currentTime)])
    if currentTimeAsFloat <= 0.0:
        hits = canvasGameWorld.itemcget('hits', 'text')
        misses = canvasGameWorld.itemcget('misses', 'text')
        destroyAll()
        canvasGameWorld.create_text(500, 350, justify=CENTER, 
                text='Game Over\n' + hits + '\n' + misses)

def shot():
    """What to do, if user shots"""
    for i in canvasGameWorld.find_withtag('shell'):
        if 'empty' not in canvasGameWorld.gettags(i):
            canvasGameWorld.itemconfig(i, state='hidden')
            canvasGameWorld.addtag('empty', 'withtag', i)
            hideUnderCursor(canvasGameWorld)
            break
    else:
       print('empty. Reload!')
            

def reloadGun(event):
    """Reload your shotgun"""
    shells = canvasGameWorld.find_withtag('shell')
    if len(shells) == len(canvasGameWorld.find_withtag('empty')):
        for i in shells:
            canvasGameWorld.itemconfig(i, state='normal')
            canvasGameWorld.dtag(i, 'empty')

def run():
    """main method for animation(Like in Greenfoot)"""
## Update the time
    updateTime()
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
root.geometry('1000x700')
## Posix path `/'
if os.name == 'posix':
    PATH = 'img/'
## Windows Path `\'
elif os.name == 'nt':
    PATH = 'img\\'

##############################################################################
##                                Images                                    ##
##############################################################################

imageShell = PhotoImage(file=PATH + 'shell.gif')
imageMoorhenLeft = PhotoImage(file=PATH + 'hen_left.gif')
imageMoorhenRight = PhotoImage(file=PATH + 'hen_right.gif')

##############################################################################
##                                 Canvas                                   ##
##############################################################################

## Specify custom cursor for posix and windows
if os.name == 'posix':
    CURSOR = ('@img/cursor.xbm', 'img/cursor-mask.xbm', 'black', 'white')
elif os.name == 'nt':
    CURSOR = '@img\cursor.cur'
else:
    CURSOR = None
canvasGameWorld = Canvas(root, bg='white', closeenough=1.0, cursor=CURSOR,
        width=1000, height=700)

## Binding to mouse, remember: CURRENT == item under cursor
canvasGameWorld.bind('<ButtonPress-1>', moorhenClicked)

## Binding to right mouse button
canvasGameWorld.bind('<ButtonPress-3>', reloadGun)

## print Hits
canvasGameWorld.create_text(850, 10, tags='hits', text='Hits: 0') 
## print Misses
canvasGameWorld.create_text(750, 10, tags='misses', text='Misses: 0') 
## print Time
canvasGameWorld.create_text(950, 10, tags='time', text='Time: 120') 

## Place shells
for i in range(8):
    canvasGameWorld.create_image(720 + (i*35), 650, image=imageShell,
                    tags='shell')

##############################################################################
##                                Layout                                    ##
##############################################################################

## Placing our Canvas  on the window
canvasGameWorld.pack()

##############################################################################
##                                Starting                                  ##
##############################################################################

## Generate 3 Moorhens, first only for debugging
moorhens = populateMoorhens(5)
run()
root.mainloop()
