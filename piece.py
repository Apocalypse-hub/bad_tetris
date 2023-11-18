import pygame
import copy
import static

gap = 25
BASE_PIECE_OFFSETS =   {
            'O' : {
                0 : (0,0),
                1 : (gap,0),
                2 : (gap,-gap),
                3 : (0,-gap)
            },
            'I' : {
                0 : (0,0),
                1 : (0,-gap),
                2 : (0,gap),
                3 : (0,gap*2)
            },
            'S' : {
                0 : (0,0),
                1 : (-gap,0),
                2 : (0,gap),
                3 : (-gap,-gap)
            },
            'Z' : {
                0 : (0,0),
                1 : (gap,0),
                2 : (0,gap),
                3 : (gap,-gap)
            },
            'L' : {
                0 : (0,0),
                1 : (0,-gap),
                2 : (0,gap),
                3 : (gap,gap)
            },
            'J' : {
                0 : (0,0),
                1 : (0,-gap),
                2 : (0,gap),
                3 : (-gap,gap)
            },
            'T' : {
                0 : (0,0),
                1 : (0,gap),
                2 : (-gap,0),
                3 : (gap,0)
            }
        }

class Piece:
    def __init__(self, gap, lBound, rBound, bottom, type, statics=[]):
        self.statics = statics
        self.pieceType = type
        self.pieceOffsets = BASE_PIECE_OFFSETS
        self.pieceColor = {
            'O' : (255,255,0),
            'I' : (0,255,255),
            'S' : (255,0,0),
            'Z' : (0,255,0),
            'L' : (255,165,0),
            'J' : (0,0,255),
            'T' : (255,0,255)
        }
        self.color = self.pieceColor[self.pieceType]
        self.squareOffsets = self.pieceOffsets[self.pieceType]
        self.gap = gap
        self.lBound = lBound
        self.rBound = rBound
        self.bottom = bottom
        self.anchor = {'x':gap*9,'y':gap}
        self.generateSquares()

    def generateSquares(self):
        self.squares: list[pygame.rect.Rect] = []
        for i in range(4):
            square = pygame.rect.Rect(self.anchor['x']+self.squareOffsets[i][0],self.anchor['y']+self.squareOffsets[i][1],self.gap,self.gap)
            self.squares.append(square)

    def addStatic(self, piece):
        self.statics += [static.Static((square.left,square.top),self.color) for square in piece.squares]
    
    def wouldCollide(self, dir):
        if dir == 'down':
            for square in self.squares:
                if square.top+self.gap >= self.bottom:
                    return True
                for static in self.statics:
                    if (static.x,static.y) == (square.left,square.top+self.gap):
                        return True
        elif dir == 'right':
            for square in self.squares:
                if square.left+self.gap >= self.rBound:
                    return True
                for static in self.statics:
                    if (static.x,static.y) == (square.left+self.gap,square.top):
                        return True
        else:
            for square in self.squares:
                if square.left-self.gap < self.lBound:
                    return True
                for static in self.statics:
                    if (static.x,static.y) == (square.left-self.gap,square.top):
                        return True
        return False

    def moveDown(self, forced):
        onbottom = self.wouldCollide('down')
        if onbottom:
            if forced:
                return True
            else:
                return False
        self.anchor['y'] += self.gap
        self.generateSquares()
        if not(forced):
            return True

    def moveLeft(self):
        if not(self.wouldCollide('left')):
            self.anchor['x'] -= self.gap
            self.generateSquares()
                
    def moveRight(self):
        if not(self.wouldCollide('right')):
            self.anchor['x'] += self.gap
            self.generateSquares()
    
    def l_rotate(self):
        if self.pieceType == 'O':
            return
        offsetsCopy = copy.copy(self.squareOffsets)
        for i in range(len(self.squareOffsets)):
            self.squareOffsets[i] = (self.squareOffsets[i][1],-self.squareOffsets[i][0])
        self.generateSquares()
        if self.isColliding():
            self.squareOffsets = offsetsCopy

    def r_rotate(self):
        if self.pieceType == 'O':
            return
        offsetsCopy = copy.copy(self.squareOffsets)
        for i in range(len(self.squareOffsets)):
            self.squareOffsets[i] = (-self.squareOffsets[i][1],self.squareOffsets[i][0])
        self.generateSquares()
        if self.isColliding():
            self.squareOffsets = offsetsCopy

    def isColliding(self):
        for square in self.squares:
                if (square.left,square.top) in self.statics:
                    return True
                if square.top >= self.bottom or square.left < self.lBound or square.left >= self.rBound:
                    return True

    def draw(self, surface):
            for square in self.squares:
                pygame.draw.rect(surface,self.color,square)