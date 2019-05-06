#!/usr/bin/env python

import unicornhathd
import time, colorsys
import numpy


#############################
def generateInitialBoard():
    board = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]  

    board = numpy.array(board)
    return board
    
#############################
def toggleFirstPixel(board):
        if board[0,0] == 0:
            board[0,0] = 1
        else:
            board[0,0] = 0

#############################
def updateGameWorld(board):
    toggleFirstPixel(board)
    
    
#############################
def setPixelForCoord(x, y):
    h = 0.4 # blue
    s = 1.0 # saturation
    v = board[x,y]*0.1 # brightness
    
    # convert the hsv back to RGB
    rgb = colorsys.hsv_to_rgb(h, s, v) 
    
    # makes a 0-1 range into a 0-255 range
    # and rounds it to a whole number
    r = int(rgb[0]*255.0) 
    g = int(rgb[1]*255.0)
    b = int(rgb[2]*255.0)
    
    # sets the pixels on the unicorn hat
    unicornhathd.set_pixel(x, y, r, g, b) 


#############################
# init
unicornhathd.brightness(1)
#need to rotate the image to have the heart the right way up
unicornhathd.rotation(90)

board = generateInitialBoard()

try:

    while True:
            
        updateGameWorld(board)
        
        for y in range(16):
            for x in range(16):
                setPixelForCoord(x,y)
                
        unicornhathd.show() # show the pixels
        
        time.sleep(1) # waiting time between heartbeats

except KeyboardInterrupt:
    unicornhathd.off()
