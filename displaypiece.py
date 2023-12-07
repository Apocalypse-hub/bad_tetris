import pygame
import static

GAP = 25
BASE_PIECE_OFFSETS =   {
            'O' : {
                0 : (0,0),
                1 : (GAP,0),
                2 : (GAP,-GAP),
                3 : (0,-GAP)
            },
            'I' : {
                0 : (0,0),
                1 : (0,-GAP),
                2 : (0,GAP),
                3 : (0,GAP*2)
            },
            'S' : {
                0 : (0,0),
                1 : (-GAP,0),
                2 : (0,GAP),
                3 : (-GAP,-GAP)
            },
            'Z' : {
                0 : (0,0),
                1 : (GAP,0),
                2 : (0,GAP),
                3 : (GAP,-GAP)
            },
            'L' : {
                0 : (0,0),
                1 : (0,-GAP),
                2 : (0,GAP),
                3 : (GAP,GAP)
            },
            'J' : {
                0 : (0,0),
                1 : (0,-GAP),
                2 : (0,GAP),
                3 : (-GAP,GAP)
            },
            'T' : {
                0 : (0,0),
                1 : (0,GAP),
                2 : (-GAP,0),
                3 : (GAP,0)
            }
        }
PIECE_COLORS = {
            'O' : (255,255,0),
            'I' : (0,255,255),
            'S' : (0,255,0),
            'Z' : (255,0,0),
            'L' : (255,165,0),
            'J' : (0,0,255),
            'T' : (255,0,255)
        }

class DisplayPiece:
    def __init__(self, type):
        self.squares = []
        self.pieceType = type
        self.color = PIECE_COLORS[type]
        self.squareOffsets = BASE_PIECE_OFFSETS[type]

    def generateSquares(self, coord):
        self.squares.clear()
        for i in range(4):
            x,y = coord
            square = pygame.rect.Rect(x+self.squareOffsets[i][0],y+self.squareOffsets[i][1],GAP,GAP)
            self.squares.append(square)

    def draw(self, surface, coord):
        self.generateSquares(coord)
        for square in self.squares:
            pygame.draw.rect(surface,self.color,square)