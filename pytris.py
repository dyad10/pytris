#!/usr/bin/python
#import Tkinter
from Tkinter import *
from time import sleep
import random
import numpy

class Player:
    def __init__(self):
        self.blocks = app.get_blocks()
        self.shape = app.get_currentshape()
        print "player init'd"

    def reinit(self):
        self.blocks = app.get_blocks()
        self.shape = app.get_currentshape()
        self.canvasvals = app.canvasvals 

    def play(self):
#        self.strategy_broadestline()
        # is there a piece on the board?
        self.canvasvals = app.canvasvals 
        for j in range(len(self.canvasvals)):
            print self.canvasvals[j]
        if app.player_can_play:
            self.strategy_broadestline()
        root.after(1500, self.play)

    def drop_now(self):
        app.commit_blocks()
        self.reinit();

    def strategy_broadestline(self):
        rotationalvalues = self.get_rotationalvalues()
        self.rotate_piece(max(rotationalvalues), rotationalvalues)
        spacemap = self.map_availablespace()
        print "spacemap", spacemap
        scores = []
        for i in range(len(spacemap) - max(rotationalvalues)):
            score = 0
            for j in range(max(rotationalvalues)):
                print "score: ", score, "+=", spacemap[i+j]
                score += spacemap[i + j]
#                scores.append(spacemap[i] + spacemap[i+1] + spacemap[i+2])
            scores.append(score)

        print "scores: ", scores
        print "min score: ", min(scores)

        # get the drop position
        for i in range(len(scores)):
            if scores[i] == min(scores):
                dropposition = i
                break
        # move to the drop position
        print "moving to", dropposition
        self.move_piece(dropposition)
        self.drop_now()

    def move_piece(self, column):
        # find the leftmost block position
        miny = 10000
        i = 0
        for block in self.blocks:
            if i < 4:
                blockcoordinates = app.canvas.coords(block)
                if int(blockcoordinates[0] / app.blockwidth) < miny:
                    miny = int(blockcoordinates[0] / app.blockwidth)
                i += 1
        print miny, column
        if miny < column:
            app.move_blocks_right()
            self.move_piece(column)
        elif miny > column:
            app.move_blocks_left()
            self.move_piece(column)

    def map_availablespace(self):
        # for each column
        spacemap = []
        self.canvasvals = app.canvasvals 
        print self.canvasvals
        # from i = 0 to 20
        for i in range(len(self.canvasvals[0])) :
            # for j from 0 to 20
            for j in range(len(self.canvasvals)):
                # this goes [0][19], [0][18]
                if(self.canvasvals[j][i] == 1):
                    spacemap.append(j-1)
#spacemap.append(int(len(app.canvasvals) / app.blockheight) - (j-1))
                    break
                elif(j == len(self.canvasvals) - 1):
                    spacemap.append(0)
#                scanarray = [[self.canvasvals[i][j], self.canvasvals[i + 1][j], self.canvasvals[i + 2][j]], [self.canvasvals[i][j+1], self.canvasvals[i + 1][j+1], self.canvasvals[i + 2][j+1]]]
        print spacemap
        return spacemap

    def find_openspace(self):
        pass

    def rotate_piece(self, rotate_to, positionscores):
        for index, item in enumerate(positionscores):
            if item == rotate_to:
                i = 0
                for i in range(index):
                    app.rotate_blocks_cw()


    def get_rotationalvalues(self):
        positionscores = []
        for j in range(4):
            i = 0
            maxy = 0
            blockcount = 0
            for block in self.blocks:
                if i < 4:
                    blockcoordinates = app.canvas.coords(block)
                    if blockcoordinates[3] > maxy:
                        maxy = blockcoordinates[3]
                        blockcount = 1
                    elif blockcoordinates[3] == maxy:
                        blockcount += 1
                    i += 1
            positionscores.append(blockcount)
            app.rotate_blocks_cw()
            self.blocks = app.blocks
        
        return positionscores

class App:
    shape = "t"
    def __init__(self, master, player = None):

#        self.shape = self.pickshape()
        self.canvaswidth = 200
        self.canvasheight = 200
        self.blockwidth = 10
        self.blockheight = 10
        self.canvasvals = []
        for i in range(self.canvasheight / self.blockheight):
            inner = []
            for j in range(self.canvaswidth / self.blockwidth):
                inner.append(0)
            self.canvasvals.append(inner)

        self.canvas = Canvas(master, width=self.canvaswidth, height=self.canvasheight)
        self.frame = Frame(master)
        self.frame.pack()
        self.canvas.pack()

        self.button = Button(self.frame, text="QUIT", fg="red", command=self.frame.quit)
        self.button.pack(side=LEFT)

        self.hi_there = Button(self.frame, text="Help", command=self.say_hi)
        self.hi_there.pack(side=LEFT)

        self.blocks = blocks = self.build_shape(self.shape, 100, 50)

        root.bind('<Right>', self.move_blocks_right)
        root.bind('<Left>', self.move_blocks_left)

        root.bind('<Down>', self.rotate_blocks_cw)
        root.bind('<Up>', self.rotate_blocks_ccw)
        root.bind('<space>', self.commit_blocks)

        
#        if player:
#            root.after(1001, player.play)
#        self.animate_shape(self.blocks)

        self.player_can_play = True

    def get_currentshape(self):
        return self.shape
    def get_blocks(self):
        return self.blocks

    def pickshape(self):
        shapes = ["line", "l", "j", "t"]
        self.shape = random.choice(shapes)
        return self.shape

    def reinit(self):
        self.shape = self.pickshape()
        self.blocks = blocks = self.build_shape(self.shape, 100, 50)

    def move_blocks_right(self, event = None):
        if self.check_space_availability([1, 0]):
            i = 0
            for blocks in self.blocks:
                if i < 4:
                    self.canvas.move(blocks, 10, 0)
                    i = i + 1
        else:
            print "illegal move"

    def move_blocks_left(self, event = None):
        if self.check_space_availability([-1, 0]):
            i = 0
            for blocks in self.blocks:
                if i < 4:
                    self.canvas.move(blocks, -10, 0)
                    i = i + 1
        else:
            print "illegal move"

        blocks = app.get_next_position([0, 1])

    def rotate_blocks_cw(self, blocks = None):
        shape = self.blocks[4]
        if shape is "t":
            print "rotating a t"
            if self.blocks[5] == 0:
                if self.check_space_availability([[1, -1], [0, 0], [1, 1], [-1, 1]]):
                    self.canvas.move(self.blocks[0], 10, -10)
                    self.canvas.move(self.blocks[2], 10, 10)
                    self.canvas.move(self.blocks[3], -10, 10)
                    self.blocks[5] = 1
                else:
                    print "illegal rotate move"

            elif self.blocks[5] == 1:
                if self.check_space_availability([[1, 0], [0, -1], [-1, 0], [-1, -2]]):
                    self.canvas.move(self.blocks[0], 10, 0)
                    self.canvas.move(self.blocks[1], 0, -10)
                    self.canvas.move(self.blocks[2], -10, 0)
                    self.canvas.move(self.blocks[3], -10, -20)
                    self.blocks[5] = 2

            elif self.blocks[5] == 2:
                if self.check_space_availability([[-1, 2], [0, 1], [-1, 0], [1, 0]]):
                    self.canvas.move(self.blocks[0], -10, 20)
                    self.canvas.move(self.blocks[1], 0, 10)
                    self.canvas.move(self.blocks[2], -10, 0)
                    self.canvas.move(self.blocks[3], 10, 0)
                    self.blocks[5] = 3

            elif self.blocks[5] == 3:
                if self.check_space_availability([[-1, -1], [0, 0], [1, -1], [1, 1]]):
                    self.canvas.move(self.blocks[0], -10, -10)
                    self.canvas.move(self.blocks[2], 10, -10)
                    self.canvas.move(self.blocks[3], 10, 10)
                    self.blocks[5] = 0

        elif shape is "line":
            print "rotating a line clockwise"
            if(self.canvas.coords(self.blocks[0])[1] == self.canvas.coords(self.blocks[1])[1]):
                if self.check_space_availability([[2, -2], [1, -1], [0, 0], [-1, 1]]):
                    print "the line is currently horizontal"
                    self.canvas.move(self.blocks[0], 20, -20)
                    self.canvas.move(self.blocks[1], 10, -10)
                    self.canvas.move(self.blocks[2], 0, 0)
                    self.canvas.move(self.blocks[3], -10, 10)
            else:
                if self.check_space_availability([[-2, 2], [-1, 1], [0, 0], [1, -1]]):
                    print "the line is currently vertical"
                    self.canvas.move(self.blocks[0], -20, 20)
                    self.canvas.move(self.blocks[1], -10, 10)
                    self.canvas.move(self.blocks[2], 0, 0)
                    self.canvas.move(self.blocks[3], 10, -10)
                    
        elif shape is "j":
            if(self.blocks[5] == 0):
                if self.check_space_availability([[1, 1], [0, 0], [-1, -1], [0, -2]]):
                    self.canvas.move(self.blocks[0], 10, 10)
                    self.canvas.move(self.blocks[2], -10, -10)
                    self.canvas.move(self.blocks[3], 0, -20)
                    self.blocks[5] = 1

            elif(self.blocks[5] == 1):
                if self.check_space_availability([[-2, 1], [-1, 0], [0, -1], [1, 0]]):
                    self.canvas.move(self.blocks[0], -20, 10)
                    self.canvas.move(self.blocks[1], -10, 0)
                    self.canvas.move(self.blocks[2], 0, -10)
                    self.canvas.move(self.blocks[3], 10, 0)
                    self.blocks[5] = 2

            elif(self.blocks[5] == 2):
                if self.check_space_availability([[-1, -1], [0, 0], [1, 1], [0, 2]]):
                    self.canvas.move(self.blocks[0], -10, -10)
                    self.canvas.move(self.blocks[2], 10, 10)
                    self.canvas.move(self.blocks[3], 0, 20)
                    self.blocks[5] = 3

            elif(self.blocks[5] == 3):
                if self.check_space_availability([[2, -1], [1, 0], [0, 1], [-1, 0]]):
                    self.canvas.move(self.blocks[0], 20, -10)
                    self.canvas.move(self.blocks[1], 10, 0)
                    self.canvas.move(self.blocks[2], 0, 10)
                    self.canvas.move(self.blocks[3], -10, 0)
                    self.blocks[5] = 0

        elif shape is "l":
            if(self.blocks[5] == 0):
                if self.check_space_availability([[2, 1], [1, 0], [0, -1], [-1, 0]]):
                    self.canvas.move(self.blocks[0], 20, 10)
                    self.canvas.move(self.blocks[1], 10, 0)
                    self.canvas.move(self.blocks[2], 0, -10)
                    self.canvas.move(self.blocks[3], -10, 0)
                    self.blocks[5] = 1
            elif(self.blocks[5] == 1):
                if self.check_space_availability([[0, 1], [1, 0], [2, -1], [1, -2]]):
                    self.canvas.move(self.blocks[0], 0, 10)
                    self.canvas.move(self.blocks[1], 10, 0)
                    self.canvas.move(self.blocks[2], 20, -10)
                    self.canvas.move(self.blocks[3], 10, -20)
                    self.blocks[5] = 2

            elif(self.blocks[5] == 2):
                if self.check_space_availability([[-2, -1], [-1, 0], [0, 1], [1, 0]]):
                    self.canvas.move(self.blocks[0], -20, -10)
                    self.canvas.move(self.blocks[1], -10, 0)
                    self.canvas.move(self.blocks[2], 0, 10)
                    self.canvas.move(self.blocks[3], 10, 0)
                    self.blocks[5] = 3

            elif(self.blocks[5] == 3):
                if self.check_space_availability([[0, -1], [-1, 0], [-2, 1], [-1, 2]]):
                    self.canvas.move(self.blocks[0], 0, -10)
                    self.canvas.move(self.blocks[1], -10, 0)
                    self.canvas.move(self.blocks[2], -20, 10)
                    self.canvas.move(self.blocks[3], -10, 20)
                    self.blocks[5] = 0

    def rotate_blocks_ccw(self, blocks= None):
        shape = self.blocks[4]
        if shape is "t":
            print "rotating a t"
            if self.blocks[5] == 0:
                if self.check_space_availability([[1, 1], [0, 0], [-1, 1], [-1, -1]]):
                    self.canvas.move(self.blocks[0], 10, 10)
                    self.canvas.move(self.blocks[2], -10, 10)
                    self.canvas.move(self.blocks[3], -10, -10)
                    self.blocks[5] = 3

            elif self.blocks[5] == 1:
                if self.check_space_availability([[-1, 1], [0, 0], [-1, -1], [1, -1]]):
                    self.canvas.move(self.blocks[0], -10, 10)
                    self.canvas.move(self.blocks[2], -10, -10)
                    self.canvas.move(self.blocks[3], 10, -10)
                    self.blocks[5] = 0

            elif self.blocks[5] == 2:
                if self.check_space_availability([[-1, 0], [0, 1], [1, 0], [1, 2]]):
                    self.canvas.move(self.blocks[0], -10, 0)
                    self.canvas.move(self.blocks[1], 0, 10)
                    self.canvas.move(self.blocks[2], 10, 0)
                    self.canvas.move(self.blocks[3], 10, 20)
                    self.blocks[5] = 1

            elif self.blocks[5] == 3:
                if self.check_space_availability([[1, -2], [0, -1], [1, 0], [-1, 0]]):
                    self.canvas.move(self.blocks[0], 10, -20)
                    self.canvas.move(self.blocks[1], 0, -10)
                    self.canvas.move(self.blocks[2], 10, 0)
                    self.canvas.move(self.blocks[3], -10, 0)
                    self.blocks[5] = 2

        elif shape is "line":
            print "rotating a line clockwise"
            if(self.canvas.coords(self.blocks[0])[1] == self.canvas.coords(self.blocks[1])[1]):
                if self.check_space_availability([[2, -2], [1, -1], [0, 0], [-1, 1]]):
                    print "the line is currently horizontal"
                    self.canvas.move(self.blocks[0], 20, -20)
                    self.canvas.move(self.blocks[1], 10, -10)
                    self.canvas.move(self.blocks[3], -10, 10)
            else:
                if self.check_space_availability([[-2, 2], [-1, 1], [0, 0], [1, -1]]):
                    print "the line is currently vertical"
                    self.canvas.move(self.blocks[0], -20, 20)
                    self.canvas.move(self.blocks[1], -10, 10)
                    self.canvas.move(self.blocks[3], 10, -10)
        elif shape is "j":
            if(self.blocks[5] == 0):
                if self.check_space_availability([[-2, 1], [-1, 0], [0, -1], [1, 0]]):
                    self.canvas.move(self.blocks[0], -20, 10)
                    self.canvas.move(self.blocks[1], -10, 0)
                    self.canvas.move(self.blocks[2], 0, -10)
                    self.canvas.move(self.blocks[3], 10, 0)
                    self.blocks[5] = 3

            elif(self.blocks[5] == 1):
                if self.check_space_availability([[-1, -1], [0, 0], [1, 1], [0, 2]]):
                    self.canvas.move(self.blocks[0], -10, -10)
                    self.canvas.move(self.blocks[2], 10, 10)
                    self.canvas.move(self.blocks[3], 0, 20)
                    self.blocks[5] = 0

            elif(self.blocks[5] == 2):
                if self.check_space_availability([[2, -1], [1, 0], [0, 1], [-1, 0]]):
                    self.canvas.move(self.blocks[0], 20, -10)
                    self.canvas.move(self.blocks[1], 10, 0)
                    self.canvas.move(self.blocks[2], 0, 10)
                    self.canvas.move(self.blocks[3], -10, 0)
                    self.blocks[5] = 1

            elif(self.blocks[5] == 3):
                if self.check_space_availability([[1, 1], [0, 0], [-1, -1], [0, -2]]):
                    self.canvas.move(self.blocks[0], 10, 10)
                    self.canvas.move(self.blocks[2], -10, -10)
                    self.canvas.move(self.blocks[3], 0, -20)
                    self.blocks[5] = 2

        elif shape is "l":
            if(self.blocks[5] == 0):
                if self.check_space_availability([[0, 1], [1, 0], [2, -1], [1, -2]]):
                    self.canvas.move(self.blocks[0], 0, 10)
                    self.canvas.move(self.blocks[1], 10, 0)
                    self.canvas.move(self.blocks[2], 20, -10)
                    self.canvas.move(self.blocks[3], 10, -20)
                    self.blocks[5] = 3

            elif(self.blocks[5] == 1):
                if self.check_space_availability([[-2, -1], [-1, 0], [0, 1], [1, 0]]):
                    self.canvas.move(self.blocks[0], -20, -10)
                    self.canvas.move(self.blocks[1], -10, 0)
                    self.canvas.move(self.blocks[2], 0, 10)
                    self.canvas.move(self.blocks[3], 10, 0)
                    self.blocks[5] = 0

            elif(self.blocks[5] == 2):
                if self.check_space_availability([[0, -1], [-1, 0], [-2, 1], [-1, 2]]):
                    self.canvas.move(self.blocks[0], 0, -10)
                    self.canvas.move(self.blocks[1], -10, 0)
                    self.canvas.move(self.blocks[2], -20, 10)
                    self.canvas.move(self.blocks[3], -10, 20)
                    self.blocks[5] = 1

            elif(self.blocks[5] == 3):
                if self.check_space_availability([[2, 1], [1, 0], [0, -1], [-1, 0]]):
                    self.canvas.move(self.blocks[0], 20, 10)
                    self.canvas.move(self.blocks[1], 10, 0)
                    self.canvas.move(self.blocks[2], 0, -10)
                    self.canvas.move(self.blocks[3], -10, 0)
                    self.blocks[5] = 2

    # takes requested_positioins
    def check_space_availability(self, deltas):
        requested_positions = self.get_next_position(deltas)
        is_available = True
        for pos in requested_positions:
            # we're in canvas boundaries
            if(int(pos[1]) < len(self.canvasvals[1]) and pos[1] >= 0 and int(pos[0]) < len(self.canvasvals[0]) and pos[0] >= 0):
                # the space is available
                try:
                    if self.canvasvals[int(pos[1])][int(pos[0])] == 1:
                        return False
                except:
                    print pos
                    print pos[1], pos[0]
                    print int(pos[1]), int(pos[0])
                    print len(self.canvasvals[1])
                    exit()
            else:
                # we went out of bounds
                return False
        return is_available

    def check_entry(self, requested_space): 
        for pos in requested_space:
            if self.canvasvals[int(pos[1])][int(pos[0])] == 1:
                return False
        return True

    def build_shape(self, shape, x0, y0):
        x1 = x0 + self.blockwidth # 10
        y1 = y0 + self.blockheight # 10
        x = x0 / self.blockwidth
        y = y0 / self.blockwidth
        if shape is "t":
            if self.check_entry([[x, y], [x+1, y], [x+1, y-1], [x+2, y]]):
                block1 = self.canvas.create_rectangle(x0,y0,x1,y1,fill="red")
                block2 = self.canvas.create_rectangle(x0+10,y0,x1+10,y1,fill="orange")
                block3 = self.canvas.create_rectangle(x0+10,y0-10,x1+10,y1-10,fill="yellow")
                block4 = self.canvas.create_rectangle(x0+20,y0,x1+20,y1,fill="green")
            else:
                print "game over!"
        elif shape is "line":
            if self.check_entry([[x, y], [x+1, y], [x+2, y], [x+3, y]]):
                block1 = self.canvas.create_rectangle(x0,y0,x1,y1,fill="red")
                block2 = self.canvas.create_rectangle(x0+10,y0,x1+10,y1,fill="red")
                block3 = self.canvas.create_rectangle(x0+20,y0,x1+20,y1,fill="red")
                block4 = self.canvas.create_rectangle(x0+30,y0,x1+30,y1,fill="red")
            else:
                print "game over!"
        elif shape is "square":
            if self.check_entry([[x, y], [x+1, y], [x, y+1], [x+1, y+1]]):
                block1 = self.canvas.create_rectangle(x0,y0,x1,y1,fill="red")
                block2 = self.canvas.create_rectangle(x0+10,y0,x1+10,y1,fill="red")
                block3 = self.canvas.create_rectangle(x0,y0+10,x1,y1+10,fill="red")
                block4 = self.canvas.create_rectangle(x0+10,y0+10,x1+10,y1+10,fill="red")
            else:
                print "game over!"
        elif shape is "j":
            if self.check_entry([[x, y], [x, y+1], [x, y+2], [x-1, y+2]]):
                block1 = self.canvas.create_rectangle(x0,y0,x1,y1,fill="red")
                block2 = self.canvas.create_rectangle(x0,y0+10,x1,y1+10,fill="orange")
                block3 = self.canvas.create_rectangle(x0,y0+20,x1,y1+20,fill="yellow")
                block4 = self.canvas.create_rectangle(x0-10,y0+20,x1-10,y1+20,fill="green")
            else:
                print "game over!"
        elif shape is "l":
            if self.check_entry([[x, y], [x, y+1], [x, y+2], [x+1, y+2]]):
                block1 = self.canvas.create_rectangle(x0,y0,x1,y1,fill="red")
                block2 = self.canvas.create_rectangle(x0,y0+10,x1,y1+10,fill="orange")
                block3 = self.canvas.create_rectangle(x0,y0+20,x1,y1+20,fill="yellow")
                block4 = self.canvas.create_rectangle(x0+10,y0+20,x1+10,y1+20,fill="green")
            else:
                print "game over!"
        elif shape is "z":
            if self.check_entry([[x-1, y], [x, y], [x, y+1], [x+1, y+1]]):
                block1 = self.canvas.create_rectangle(x0-10,y0,x1-10,y1,fill="red")
                block2 = self.canvas.create_rectangle(x0,y0,x1,y1,fill="orange")
                block3 = self.canvas.create_rectangle(x0,y0+10,x1,y1+10,fill="yellow")
                block4 = self.canvas.create_rectangle(x0+10,y0+10,x1+10,y1+10,fill="green")
            else:
                print "game over!"
        elif shape is "s":
            if self.check_entry([[x, y], [x+1, y], [x, y+1], [x-1, y+1]]):
                block1 = self.canvas.create_rectangle(x0,y0,x1,y1,fill="red")
                block2 = self.canvas.create_rectangle(x0+10,y0,x1+10,y1,fill="red")
                block3 = self.canvas.create_rectangle(x0,y0+10,x1,y1+10,fill="red")
                block4 = self.canvas.create_rectangle(x0-10,y0+10,x1-10,y1+10,fill="red")
            else:
                print "game over!"
        position = 0
        blocks = [block1, block2, block3, block4, shape, position]
        return blocks

    def check_move_legality(self, newblocks_range):
        is_legal = True
        # check to see if all blocks are in bounds
        if(newblocks_range[0] < 0):
            return False
        if(newblocks_range[2] > self.canvaswidth):
            return False
        i = 0
        for blocks in self.blocks:
            if i < 4:
              x = app.canvas.coords(app.blocks[i])[0] / self.blockwidth
              y = app.canvas.coords(app.blocks[i])[1] / self.blockheight
        return is_legal

    def get_next_position(self, deltas):
        # deltas[0] is change in x
        # deltas[1] is change in y
        newpositions = []

        # this is not ideal ... looking to see if array passed is not the expected length of 4
        if len(deltas) == 2:
            deltas_t = []
            deltas_t.append(deltas)
            deltas_t.append(deltas)
            deltas_t.append(deltas)
            deltas_t.append(deltas)
            deltas = deltas_t

        ii = 0
        for blocks in self.blocks:
            if ii < 4:
                xnum = app.canvas.coords(blocks)[0]
                ynum = app.canvas.coords(blocks)[1]
                deltax = deltas[ii][0]
                deltay = deltas[ii][1]
                x = app.canvas.coords(self.blocks[ii])[0] / self.blockwidth + deltas[ii][0]
                y = app.canvas.coords(self.blocks[ii])[1] / self.blockheight + deltas[ii][1]
                newpositions.append([x, y])

                ii += 1
        return newpositions

    def lock_blocks(self):
        i = 0
        for block in self.blocks:
            if i < 4:
                pos = app.canvas.coords(block)
                self.canvasvals[int(pos[1] / self.blockheight)][int(pos[0] / self.blockwidth)] = 1
            i += 1
        lines_to_remove = self.find_completed_lines()
#        for j in range(len(self.canvasvals)):
#            print self.canvasvals[j]
        return lines_to_remove

    def remove_lines(self, lines_to_remove):
        if(len(lines_to_remove) > 0):
            for line in lines_to_remove:
#                i = int ((self.canvasheight - 1) / self.canvasheight)
                for i in range(int (self.canvaswidth / self.blockwidth)):
                    rmbox = app.canvas.find_closest((i+0.5) * self.blockwidth, (line + 0.5) * self.blockheight)
                    result = self.canvas.delete(rmbox)
                    i += 1
            self.canvas.update()

            # move all other blocks in the row above down one
            allblocks = self.canvas.find_all()
            lines_to_remove.sort()
            lines_to_remove.reverse()
            # starting from the bottom removed line, move blocks down
            for line in lines_to_remove:
                # line = 19
                for b in allblocks:
                    b_coords = self.canvas.coords(b)
                    if b_coords[1] <= line * self.blockheight:
                        self.canvas.move(b, 0, self.blockheight)
                self.canvas.update()
                k = 0
                for l in lines_to_remove:
                    lines_to_remove[k] += 1
                    k += 1
                    # handle case with more lines matched
#                    j = 0
#                    for a in lines_to_remove:
#                        lines_to_remove[j] += 1
#                        j += 1

    def find_completed_lines(self):
        # check for complete lines
        i = 0
        linescompleted = []
        for line in self.canvasvals:
            if sum(line) == self.canvaswidth / self.blockwidth:
                #line is completed
                linescompleted.append(i)
                self.canvasvals.pop(i)
                self.canvasvals.insert(0, [0] * self.canvaswidth)
            i += 1
        print "lines completed: ", linescompleted
        return linescompleted
                
    def rm_shape(self, blocks):
        print "shape being removed"
        self.canvas.delete(self.blocks[0])
        self.canvas.delete(self.blocks[1])
        self.canvas.delete(self.blocks[2])
        self.canvas.delete(self.blocks[3])

    def say_hi(self):
        root.after(0, player.play)

    def commit_blocks(self, event=None):
        print "Committnig blocks"
        self.player_can_play = False
        block0 = app.canvas.coords(self.blocks[0])
        block1 = app.canvas.coords(self.blocks[1])
        block2 = app.canvas.coords(self.blocks[2])
        block3 = app.canvas.coords(self.blocks[3])

        blocks = [[block0[0] / 10, block0[1] / 10 + 1], 
                  [block1[0] / 10, block1[1] / 10 + 1], 
                  [block2[0] / 10, block2[1] / 10 + 1], 
                  [block3[0] / 10, block3[1] / 10 + 1]] 

        if app.check_space_availability([0, 1]):
            app.canvas.move(app.blocks[0], 0, 10)
            app.canvas.move(app.blocks[1], 0, 10)
            app.canvas.move(app.blocks[2], 0, 10)
            app.canvas.move(app.blocks[3], 0, 10)

            app.canvas.update()
            # Recursive call, not calling the mainloop currently 
            # because that causes a race condition with drop_blocks()
            self.commit_blocks()

        else: 
            #Lock the piece
            lines_to_remove = app.lock_blocks()
            if len(lines_to_remove) > 0:
                app.remove_lines(lines_to_remove)
            app.reinit()

        self.player_can_play = True

root = Tk()
root.title("Tetris")

print "Calling App"
app = App(root)
player = Player()

def drop_blocks():

    if app.check_space_availability([0, 1]):
        app.canvas.move(app.blocks[0], 0, 10)
        app.canvas.move(app.blocks[1], 0, 10)
        app.canvas.move(app.blocks[2], 0, 10)
        app.canvas.move(app.blocks[3], 0, 10)

        app.canvas.update()
        root.after(1000, drop_blocks)

    else: 
        print 'locked!'
        #Lock the piece
        lines_to_remove = app.lock_blocks()
        print len(lines_to_remove), "lines need to be removed"
        if len(lines_to_remove) > 0:
            app.remove_lines(lines_to_remove)

        app.reinit()
        root.after(1000, drop_blocks)

root.after(0, drop_blocks)
#root.after(0, player.play)

print "Calling mainroot"
root.mainloop()

