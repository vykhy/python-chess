'''This is our main driver file. It will be responsible for handling user input and displaying the current game state'''

import pygame
import ChessEngine

pygame.init()
WIDTH = HEIGHT = 512
DIMENSIONS = 8
SQ_SIZE = HEIGHT // DIMENSIONS
MAX_FPS = 15
IMAGES = {}

'''
Initialize a global dictionary of images. This will be called exactly once in main
'''
def loadImages():
    pieces = ['wp', 'wR', 'wN','wB','wQ','wK','bp','bR','bN','bB','bK','bQ']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load('./images/'+piece+'.png'), (SQ_SIZE, SQ_SIZE))

'''
The main driver for our code
'''
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    gs = ChessEngine.GameState()
    loadImages()
    validMoves = gs.getValidMovesAdvanced()
    moveMade = False

    running = True
    selectedSquare = () # keep track of last click of user (row, col)
    playerClicks = [] # keep track of player clicks (two tuples: [(6, 4), (4, 4)])

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos() # location of click
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if selectedSquare == (row, col): # clicked same square, unselect
                    selectedSquare = ()
                    playerClicks = []
                else:
                    selectedSquare = (row, col)
                    playerClicks.append(selectedSquare)
               
                if len(playerClicks) == 2: # if it is second click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        selectedSquare = ()
                        playerClicks = []
                    else:
                        playerClicks = [selectedSquare]

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    gs.undoMove()
                    moveMade = True
        
        if moveMade:
            validMoves = gs.getValidMovesAdvanced()
            moveMade = False

        clock.tick(MAX_FPS)
        drawBoard(screen)
        drawPieces(screen, gs.board)
        pygame.display.flip()

'''
Responsible for all the graphics within current game state
'''
def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

'''Draw the squares on the board'''
def drawBoard(screen):
    colors = [pygame.Color('white'), pygame.Color('gray')]
    for row in range(DIMENSIONS):
        for col in range(DIMENSIONS):
            color = colors[((row + col) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''Draw the pieces on the board using the current GameState.board'''
def drawPieces(screen, board):
    for row in range(DIMENSIONS):
        for col in range(DIMENSIONS):
            piece = board[row][col]
            if piece != '--': # not an empty space
                screen.blit(IMAGES[piece], pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__=="__main__":
    main()
