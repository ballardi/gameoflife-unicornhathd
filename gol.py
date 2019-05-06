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
        self.boardSize = 16;
        self.boardA = Board._generateAnInitializedBoard(self.boardSize)
        self.boardB = Board._generateAnInitializedBoard(self.boardSize)

    def _getCurrentBoard(self):
        if (self.state == BoardState.A):
            return self.boardA
        else:
            return self.boardB
    
    def getNode(self,x,y):
        if(x < 0 | x >= self.boardSize):
            raise Exception("invalid x: " + x)
        if(y < 0 | y >= self.boardSize):
            raise Exception("invalid y: " + y)
        
        b = self._getCurrentBoard();
        return b[x][y]
    
    def _countLiveNeighbours(board, x, y):
        if(x < 0 | x >= self.boardSize):
            raise Exception("invalid x: " + x)
        if(y < 0 | y >= self.boardSize):
            raise Exception("invalid y: " + y)

    
    def advanceState(self):
        # TODO update state of off board
        # Any live cell with fewer than two live neighbours dies, as if by underpopulation.
        # Any live cell with two or three live neighbours lives on to the next generation.
        # Any live cell with more than three live neighbours dies, as if by overpopulation.
        # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

        
        # flip state flag
        if (self.state == BoardState.A):
            self.state = BoardState.B
        else:
            self.state = BoardState.A
    
    @staticmethod
    def _generateAnInitializedBoard(size):
        # create board with zeros
        w, h = size, size;
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
def setPixelForCoord(board,x, y):
    h = 0.4 # blue
    s = 1.0 # saturation
    v = board.getNode(x,y).on*.1 # brightness
    
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
blinkerState = 0

try:

    while True:
        print(board.state)

        # update pixels with current state
        for y in range(16):
            for x in range(16):
                setPixelForCoord(board,x,y)
        
        # overwrite first pixel with blinker
        blinkerState = 1 - blinkerState
        unicornhathd.set_pixel_hsv(0,0,0.4,1,blinkerState*.1) #xyhsv
        
        unicornhathd.show() # show the pixels
        
        board.advanceState()
        time.sleep(SLEEP_BETWEEN_FRAMES) # waiting time between heartbeats

except KeyboardInterrupt:
    unicornhathd.off()

