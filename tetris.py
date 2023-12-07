import pygame
import piece
import random
import copy
import displaypiece

class Tetris:
    
    def __init__(self, width, height):
        self.fallSeconds = .7
        self.alreadyHeld = False
        self.squares = []
        self.ticker = 0
        self.width = width
        self.height = height
        self.gap = 25
        self.leftBound = self.gap*5
        self.rightBound = self.width-125
        self.piece = "placeholder"
        self.held = ""
        self.bag = []
        self.addBag()
        self.newPiece()

    def addBag(self):
        pieces = ['O','T','I','L','J','S','Z']
        random.shuffle(pieces)
        self.bag += pieces

    def hold(self):
        if not(self.alreadyHeld):
            self.alreadyHeld = not(self.alreadyHeld)
            if self.held:
                currentptype = self.piece.pieceType
                self.piece = piece.Piece(self.gap, self.leftBound, self.rightBound, self.height, self.held)
                self.held = currentptype
            else:
                self.held = self.piece.pieceType
                ptype = self.bag[0]
                self.bag.remove(ptype)
                if len(self.bag) == 4:
                    self.addBag()
                self.nextFourPieces = self.bag[0:4]
                self.piece = piece.Piece(self.gap, self.leftBound, self.rightBound, self.height, ptype)

    
    def newPiece(self):
        if self.piece != "placeholder":
            self.alreadyHeld = False
            pieceCopy = copy.deepcopy(self.piece)
            self.squares += pieceCopy.squares
            self.piece.addStatic(pieceCopy)
        ptype = self.bag[0]
        self.bag.remove(ptype)
        if len(self.bag) == 4:
            self.addBag()
        self.nextFourPieces = self.bag[0:4]
        self.piece = piece.Piece(self.gap, self.leftBound, self.rightBound, self.height, ptype)
        self.clearLines()

    def clearLines(self):
        for i in range(0,476,25):
            squaresInLine = [static for static in self.piece.statics if static.y == i]
            if len(squaresInLine) == 10:
                for square in squaresInLine:
                    self.piece.statics.remove(square)
                for j in range(len(self.piece.statics)):
                    if self.piece.statics[j].y < i:
                        self.piece.statics[j].y += self.gap

    def checkForLoss(self):
        staticCoords = [(static.x,static.y) for static in self.piece.statics]
        for square in self.piece.squares:
            if (square.left,square.top) in staticCoords:
                self.__init__(self.width,self.height)
                self.piece.statics.clear()
                return

    def moveDown(self, forced):
        if self.piece.moveDown(forced):
            self.ticker = 0

    def hardDrop(self):
        while not(self.piece.moveDown(True)):
            pass
        self.newPiece()
        self.checkForLoss()

    def evolve(self, dt):
        self.ticker += dt
        if self.ticker >= self.fallSeconds:
            push = self.piece.moveDown(True)
            self.ticker -= self.fallSeconds
            if push:
                self.newPiece()
                self.checkForLoss()
        self.piece.makeGhost()

    def drawUpcoming(self, surface):
        for index,y in enumerate(range(self.gap,20*self.gap,5*self.gap)):
            displaypiece.DisplayPiece(self.nextFourPieces[index]).draw(surface, (self.rightBound + 2*self.gap, y))

    def draw(self, surface):
        pygame.draw.rect(surface, (0,0,0), (0, 0, self.width, self.height))
        for i in range(0,self.height,self.gap):
            pygame.draw.line(surface, (255,255,255),(self.leftBound,i),(self.rightBound,i))
        for i in range(self.leftBound-25,self.rightBound+self.gap+1,self.gap):
            pygame.draw.line(surface, (255,255,255),(i,0),(i,self.height))
        
        for square in self.piece.statics:
            pygame.draw.rect(surface,square.color,pygame.rect.Rect(square.x,square.y,self.gap,self.gap))
        
        self.drawUpcoming(surface)

        if self.held:
            displaypiece.DisplayPiece(self.held).draw(surface, (self.gap,2*self.gap))

        self.piece.draw(surface)