#!/usr/bin/env python

import unicornhathd
import time, colorsys
from enum import Enum

STARTING_VALS = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
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

SLEEP_BETWEEN_FRAMES = 0.5

#############################
class BoardState(Enum):
     A = 0
     B = 1

#############################
class Board:
    
    # constructor
    def __init__(self):
        self.state = BoardState.A
        self.boardA = generateInitialBoard()
        self.boardB = generateInitialBoard()

    def getCurrentBoard():
        if (state == BoardState.A):
            return boardA
        else:
            return boardB
    
    def getNode(x,y):
        b = getCurrentBoard();
        return b[x][y]
    
    def advanceState():
        # TODO update state of off board
        
        # flip state flag
        if (state == BoardState.A):
            state = BoardState.B
        else:
            state = BoardState.A
        
    def generateInitialBoard():
        # create board with zeros
        w, h = 16, 16;
        board = [[Node() for x in range(w)] for y in range(h)]
        
        # set starting values for board
        for y in range(16):
            for x in range(16):
                board[x][y].on = STARTING_VALS[x][y]
        
        return board
    

#############################
class Node:
    on = 0
    

#############################
def toggleFirstPixel(board):
        if board[0][0].on == 0:
            board[0][0].on = 1
        else:
            board[0][0].on = 0

#############################
def setPixelForCoord(x, y):
    h = 0.4 # blue
    s = 1.0 # saturation
    v = board[x][y].on*.1 # brightness
    
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

board = Board()

try:

    while True:

        for y in range(16):
            for x in range(16):
                setPixelForCoord(x,y)
               
        unicornhathd.show() # show the pixels
        
        board.advanceState()
        time.sleep(SLEEP_BETWEEN_FRAMES) # waiting time between heartbeats

except KeyboardInterrupt:
    unicornhathd.off()

