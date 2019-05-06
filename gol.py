#!/usr/bin/env python

import unicornhathd
import time, colorsys
from enum import Enum
from random import randint

SHOW_STATE_CHANGE_INDICATOR = False;
SLEEP_BETWEEN_FRAMES = .05

# "none", "position", "time"
COLORS = "time"

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
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]  

#############################
class Game:
    
    # constructor
    def __init__(self):
        self.age = 0
        self.activeBoard = "a"
        self.boardSize = 16;
        self.boardA = Game._generateAnInitializedBoard(self.boardSize)
        self.boardB = Game._generateAnInitializedBoard(self.boardSize)
        
        self.prevBoardHashed = -1
        self.activeBoardHashed = -1

        self.consecutiveTimeWithoutChange = 0
        self.consecutiveTimeAlternatingBetween2States = 0

    def _getActiveBoard(self):
        if (self.activeBoard == "a"):
            return self.boardA
        else:
            return self.boardB
    
    def _getInactiveBoard(self):
        if (self.activeBoard == "a"):
            return self.boardB
        else:
            return self.boardA
    
    def _flipActiveBoard(self):
        if (self.activeBoard == "a"):
            self.activeBoard = "b"
        else:
            self.activeBoard = "a"
    
    def getNode(self,x,y):
        if(x < 0 or x >= self.boardSize):
            raise Exception("invalid x: " + x)
        if(y < 0 or y >= self.boardSize):
            raise Exception("invalid y: " + y)
        
        b = self._getActiveBoard();
        return b[x][y]
    
    def _returnNodeValOr0(self, board, x, y):
        if(x < 0 or x >= self.boardSize):
            return 0
        if(y < 0 or y >= self.boardSize):
            return 0

        return board[x][y].on
    
    def _countLiveNeighbours(self,board, x, y):
        if(x < 0 or x >= self.boardSize):
            raise Exception("invalid x: " + x)
        if(y < 0 or y >= self.boardSize):
            raise Exception("invalid y: " + y)
        
        counter = 0;

        if(self._returnNodeValOr0(board,x-1,y-1) == 1):
            counter = counter + 1
        if(self._returnNodeValOr0(board,x-0,y-1) == 1):
            counter = counter + 1
        if(self._returnNodeValOr0(board,x+1,y-1) == 1):
            counter = counter + 1
        if(self._returnNodeValOr0(board,x-1,y-0) == 1):
            counter = counter + 1
        if(self._returnNodeValOr0(board,x+1,y-0) == 1):
            counter = counter + 1
        if(self._returnNodeValOr0(board,x-1,y+1) == 1):
            counter = counter + 1
        if(self._returnNodeValOr0(board,x-0,y+1) == 1):
            counter = counter + 1
        if(self._returnNodeValOr0(board,x+1,y+1) == 1):
            counter = counter + 1
        
        return counter
    
    def advanceState(self):
        activeBoard = self._getActiveBoard();
        inactiveBoard = self._getInactiveBoard();
        
        newBoardHashed = 0
        
        # for each node in inactiveBoard
        for y in range(self.boardSize):
            for x in range(self.boardSize):
                
                # calculate new state based on activeBoard state
                currentLiveNeighbours = self._countLiveNeighbours(activeBoard,x,y)
                
                # if activeBoard cell is live
                if(activeBoard[x][y].on == 1):
                    # Any live cell with two or three live neighbours lives on to the next generation.
                    if(currentLiveNeighbours == 2 or currentLiveNeighbours == 3): 
                        inactiveBoard[x][y].on = 1
                        inactiveBoard[x][y].onAge += 1
                    # Any live cell with fewer than two live neighbours dies, as if by underpopulation.
                    # Any live cell with more than three live neighbours dies, as if by overpopulation.
                    else:
                        inactiveBoard[x][y].on = 0
                        inactiveBoard[x][y].onAge = 0
                else:
                    # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
                    if(currentLiveNeighbours == 3): 
                        inactiveBoard[x][y].on = 1
                        inactiveBoard[x][y].onAge = 1
                    else:
                        inactiveBoard[x][y].on = 0
                        inactiveBoard[x][y].onAge = 0
                
                # continue constructing hash
                newBoardHashed = newBoardHashed << 1
                if(inactiveBoard[x][y].on == 1):
                    newBoardHashed += 1

        # note we use bitwise xor to check equality of the hashes
        # because == was evaluating to false incorrectly in some cases.

        if (str(self.activeBoardHashed ^ newBoardHashed) == str(0)):
            # new board is same as current
            self.consecutiveTimeWithoutChange += 1
            self.consecutiveTimeAlternatingBetween2States = 0
        elif(str(self.prevBoardHashed ^ newBoardHashed) == str(0)):
            # new board is different from current but same as previous
            self.consecutiveTimeWithoutChange = 0
            self.consecutiveTimeAlternatingBetween2States += 1
        else:
            # new board is different from both current and previous
            self.consecutiveTimeWithoutChange = 0
            self.consecutiveTimeAlternatingBetween2States = 0

        # if board is stuck for a period of time (of random length), create new life
        stuckTimeToQualifyForNewLife = randint(20,50)
        if(self.consecutiveTimeWithoutChange >= stuckTimeToQualifyForNewLife
           or self.consecutiveTimeAlternatingBetween2States >= stuckTimeToQualifyForNewLife):
            
            #create a random number of new living nodes
            # choose a spot for first one that's not on the edge
            x, y = randint(3,12), randint(3,12) 
            for i in range(0, randint(3,8)):
                # if the note isn't alive, make it alive
                if(inactiveBoard[x][y].on == 0):
                    inactiveBoard[x][y].on = 1
                    inactiveBoard[x][y].onAge += 1
                # for the next node to make live, select randomly nearby this one
                x = max(0,min(x + randint(-1,1), 15))
                y = max(0,min(y + randint(-1,1), 15))
        
        self._flipActiveBoard()
        self.age += 1
        self.prevBoardHashed = self.activeBoardHashed
        self.activeBoardHashed = newBoardHashed
    
    @staticmethod
    def _generateAnInitializedBoard(size):
        # create board with zeros
        w, h = size, size;
        board = [[Node() for x in range(w)] for y in range(h)]
        
        # set starting values for board
        for y in range(16):
            for x in range(16):
                board[x][y].on = STARTING_VALS[x][y]
                if(board[x][y].on):
                    board[x][y].onAge = 1;
        
        return board
    

#############################
class Node:
    on = 0 # is the node alive now
    onAge = 0 # count of consecutive cycles alive
    
#############################
def setPixelForCoord(game,x, y):
    
    #color
    if(COLORS == "position"):
        h = 0.5+(x+y)*0.01
    elif(COLORS == "time"):
        h = game.age*0.01 % 1
    else: # "none"
        h = 0.4 # blue
    
    s = 0.95 # saturation

    # brightness
    if(game.getNode(x,y).on == 1):
        v = 1 - (float)(game.getNode(x,y).onAge*0.3)
        v = max(v, 0.2)
    else:
        v = 0

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

game = Game()
blinkerState = 0

try:

    while True:
        
        # update pixels with current state
        for y in range(16):
            for x in range(16):
                setPixelForCoord(game,x,y)

        if (SHOW_STATE_CHANGE_INDICATOR):
            # overwrite first pixel with blinker
            blinkerState = 1 - blinkerState
            unicornhathd.set_pixel_hsv(0,0,0.4,1,blinkerState*.1) #xyhsv

        unicornhathd.show() # show the pixels

        game.advanceState()
        time.sleep(SLEEP_BETWEEN_FRAMES)

except KeyboardInterrupt:
    unicornhathd.off()


