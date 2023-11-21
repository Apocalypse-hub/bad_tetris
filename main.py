import pygame
import game
import tetris

TITLE = "Tetris v0.6.4"
WINDOW_WIDTH  = 500
WINDOW_HEIGHT = 500
DESIRED_RATE  = 20
GAP = 50

class PygameApp(game.Game):

    def __init__(self, title, width, height, frame_rate):
        game.Game.__init__(self, title, width, height, frame_rate)

        # create a game instance
        self.game = tetris.Tetris(width, height)


    def game_logic(self, keys, newkeys, buttons, newbuttons, mouse_position, dt):
        # keys contains all keys currently held down
        # newkeys contains all keys pressed since the last frame
        # Use pygame.K_? as the keyboard keys.
        # Examples: pygame.K_a, pygame.K_UP, etc.
        if pygame.K_c in newkeys:
            self.game.hold()
        
        if pygame.K_DOWN in keys:
            self.game.moveDown(False)
        if pygame.K_SPACE in newkeys:
            self.game.hardDrop()
        elif pygame.K_LEFT in keys:
            self.game.piece.moveLeft()
        elif pygame.K_RIGHT in keys:
            self.game.piece.moveRight()
        
        if pygame.K_z in newkeys:
            self.game.piece.l_rotate()
        elif pygame.K_x in newkeys:
            self.game.piece.r_rotate()
        
        if pygame.K_BACKSLASH in newkeys:
            print(self.game.piece.anchor)
        #
        # buttons contains all mouse buttons currently held down
        # newbuttons contains all buttons pressed since the last frame
        # Use 1, 2, 3 as the mouse buttons
        # if 3 in buttons:
        #    The user is holding down the right mouse button
        #
        # mouse_position contains x and y location of mouse in window
        # dt contains the number of seconds since last frame

        # Update the state of the game instance

        self.game.evolve(dt)

    def paint(self, surface):
        # Draw the current state of the game instance
        self.game.draw(surface)

def main():
    pygame.font.init()
    game = PygameApp(TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, DESIRED_RATE)
    game.main_loop()

if __name__ == "__main__":
    main()
