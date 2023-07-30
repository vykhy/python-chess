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
    animate = True

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
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            animate = True
                            gs.makeMove(validMoves[i])
                            moveMade = True
                            selectedSquare = ()
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [selectedSquare]

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    animate = False
                    gs.undoMove()
                    moveMade = True
                if event.key == pygame.K_r: # reset the board
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMovesAdvanced()
                    selectedSquare = ()
                    playerClicks = []
                    moveMade = False
                    animate = False

        
        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMovesAdvanced()
            moveMade = False
            animate = False

        clock.tick(MAX_FPS)
        drawGameState(screen, gs, validMoves, selectedSquare)
        pygame.display.flip()

'''
Highlight possible mnove squared
'''
def highlightSquares(screen, gameState, validMoves, sqSelected):
    if sqSelected == ():
        return
    row, col = sqSelected
    # check if selected square belongs to the correct color's turn
    if gameState.board[row][col][0] == ('w' if gameState.whiteToMove else 'b'):
        # highlight selected square
        s = pygame.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100)
        s.fill(pygame.Color('blue'))
        screen.blit(s, (col * SQ_SIZE, row * SQ_SIZE))

        # highlight moves
        s.fill(pygame.Color('yellow'))
        for move in validMoves:
            if move.startRow == row and move.startCol == col:
                screen.blit(s, (SQ_SIZE * move.endCol, SQ_SIZE * move.endRow))

'''
Responsible for all the graphics within current game state
'''
def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)

'''Draw the squares on the board'''
def drawBoard(screen):
    global colors
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

'''
Animate piece movement
'''
def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    fps = min(18 // (abs(dR) + abs(dC)), 5)    # frames per square
    frameCount = (abs(dR) + abs(dC)) * fps
    for frame in range(frameCount + 1):
        row, col = (move.startRow + dR*frame/frameCount, move.startCol + dC * frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase end piece
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = pygame.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        pygame.draw.rect(screen, color, endSquare)

        # draw captured piece
        if move.pieceCaptured != "--":
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        
        # draw moving piece
        screen.blit(IMAGES[move.pieceMoved], pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        pygame.display.flip()
        clock.tick(60)

if __name__=="__main__":
    main()
