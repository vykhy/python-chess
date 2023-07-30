from Move import Move
from CastleRights import CastleRights 

'''This class is responsible or storing all the information about the current state of a chess game. 
It is also responsible for determining the valid moves at the current state, and will maintain a move log'''

class GameState():
    def __init__(self):
        # board is an 8x8 2d list. 
        # First char represents color, and second char represents type
        # '--' represents an empty space with no piece
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]
        self.moveFunctions = {
            "p": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves, "B": self.getBishopMoves,
            "Q": self.getQueenMoves, "K": self.getKingMoves
        }
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.enpassantPossible = () # coordinates of square where possible. only 1 square on each move
        self.currentCastleRights = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastleRights.wks, self.currentCastleRights.wqs,
                                self.currentCastleRights.bks, self.currentCastleRights.wqs)]    
    '''
    returns checks, pins and whether currently in check
    '''
    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            enemyColor = 'b'
            allyColor = 'w'
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = 'w'
            allyColor = 'b'
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        directions = ((-1, 0), (0,-1), (1,0), (0,1), (-1, -1), (-1, 1),(1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol <8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, d[0], d[1])
                        #second allied piece, so no pin or check possible in this direction
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        # 5 possiblities here to check for
                        # 1. orthogonally away from king and piece is a rook
                        # 2. diagonally away form king and piece is a bishop
                        # 3. 1 square diagonally away from king and piece is a pawn
                        # 4. any direction and piece is a queen
                        # 5. any direction 1 square away and piece is a king
                        if (0 <= j <= 3 and type == 'R') or \
                            (4 <= j <= 7 and type == 'B') or \
                                (i == 1 and type == 'p' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor =='b' and 4 <= j <= 5))) or \
                                    (type == 'Q') or (i == 1 and type == 'K'):
                            if possiblePin == ():
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else:
                                pins.append(possiblePin)
                                break
                        else:
                            # piece not applying check
                            break
                else: 
                    break # off board
        
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow + m [0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks

    '''
    Takes a move and executes it. Will not work for castling, pawn promotion and en-passant
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        if move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)
        
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + "Q"
        

        # set enPassant square
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.startRow + move.endRow) // 2, move.endCol)
        else:
            self.enpassantPossible = ()
        if move.isEnpassant:
            # capturing the pawn beside it, and after move behind it
            self.board[move.startRow][move.endCol] = '--' 

        # castle move
        if move.isCastle:
            if move.endCol - move.startCol == 2: # kingside castle
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol + 1] ="--" # erase old rook
            else: # queenside castle
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol-2]
                self.board[move.endRow][move.endCol - 2] ="--" # erase old rook
                

        # update castle rights
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastleRights.wks, self.currentCastleRights.wqs,
                                    self.currentCastleRights.bks, self.currentCastleRights.bqs))
    '''
    Undo the last move
    '''
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.startRow, move.startCol)
        if move.pieceMoved == 'bK':
            self.blackKingLocation = (move.startRow, move.startCol)
        
        if move.isEnpassant:
            self.board[move.endRow][move.endCol] = '--'
            self.board[move.startRow][move.endCol] = move.pieceCaptured
            self.enpassantPossible = (move.endRow, move.endCol)
        
        # case 2 square pawn move
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ()
        
        # undo castle rights log
        self.castleRightsLog.pop()
        self.currentCastleRights = self.castleRightsLog[-1]

        # undo castle move
        if move.isCastle:
            if move.endCol - move.startCol == 2: # kingside
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                self.board[move.endRow][move.endCol - 1] = "--"
            else:
                self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                self.board[move.endRow][move.endCol + 1] = "--" 

    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastleRights.wks = False
            self.currentCastleRights.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastleRights.bks = False
            self.currentCastleRights.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastleRights.wqs = False
                elif move.startCol == 7:
                    self.currentCastleRights.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastleRights.bqs = False
                elif move.startCol == 7:
                    self.currentCastleRights.bks = False

    '''
    All moves considering checks (naive brute force method)
    '''
    def getValidMoves(self):
        # 1. Generate all possible moves
        moves = self.getAllPossibleMoves()
        # 2. For each move, make move
        for i in range(len(moves) - 1, -1, -1):
            self.makeMove(moves[i])
            # 3. Generate all opponent's moves
            # 4. For each opponent's moves, see if they attack your king
            self.whiteToMove = not self.whiteToMove
            # 5. If king is attacked, not a valid move
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        
        # if no valid moves, it is either a checkmate or a stalemate
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        return moves
    
    '''
    All moves considering checks (Advanced efficient method)
    '''
    def getValidMovesAdvanced(self):
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:
            if(len(self.checks)) == 1: # only 1 check, block or move king
                moves = self.getAllPossibleMoves()
                # move a piece between enemy piece and king
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = [] #squares that pieces can move to 
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i) # check 2 and 3 are the directions
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                # remove moves that dont move king or block checks
                for i in range(len(moves) -1, -1, -1):
                    if moves[i].pieceMoved[1] != 'K':
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else: # double check, so king has to move
                self.getKingMoves(kingRow, kingCol, moves)
        else: # not in check, so all moves fine
            moves = self.getAllPossibleMoves()
        
        self.getCastleMoves(kingRow, kingCol, moves)
        if len(moves) == 0:
            if self.inCheck:
                self.checkMate = True
            else:
                self.staleMate = True
        
        return moves

    '''
    Return whether king is in check
    '''
    def inCheck_(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    '''
    Determine if the enemy can attack the square at row, col
    '''
    def squareUnderAttack(self, row, col):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == row and move.endCol == col:
                return True
        return False

    '''
    All moves without checks
    '''
    def getAllPossibleMoves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[row][col][1]
                    self.moveFunctions[piece](row, col, moves)
        return moves
                    
    '''
    Get all possible pawn moves for pawn at row, col and add to moves
    '''
    def getPawnMoves(self, row, col, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        if self.whiteToMove:
            if self.board[row-1][col] == '--':
                if not piecePinned or pinDirection == (-1, 0):
                    moves.append(Move((row, col), (row-1, col), self.board))
                    if row == 6 and self.board[row-2][col] == '--':
                        moves.append(Move((row, col), (row-2, col), self.board))
            #captures
            if col - 1 >= 0: # capture to left
                if self.board[row-1][col-1][0] == 'b':
                    if not piecePinned or pinDirection == (-1, -1):
                        moves.append(Move((row, col), (row-1, col-1), self.board))
                if (row-1, col-1) == self.enpassantPossible:
                    if not piecePinned or pinDirection == (-1, -1):
                        moves.append(Move((row, col), (row-1, col-1), self.board, isEnpassant=True))
            if col + 1 <= 7: # capture to right
                if self.board[row-1][col+1][0] == 'b':
                    if not piecePinned or pinDirection == (-1, 1):
                        moves.append(Move((row, col), (row-1, col+1), self.board))
                if (row-1, col+1) == self.enpassantPossible:
                    if not piecePinned or pinDirection == (-1, 1):
                        moves.append(Move((row, col), (row-1, col+1), self.board, isEnpassant=True))
        # black pawn moves
        else:
            if self.board[row+1][col] == '--':
                if not piecePinned or pinDirection == (1, 0):
                    moves.append(Move((row, col), (row+1, col), self.board))
                    if row == 1 and self.board[row+2][col] == '--':
                        moves.append(Move((row, col), (row+2, col), self.board))
            if col -1 >= 0:
                if self.board[row+1][col-1][0] == 'w':
                    if not piecePinned or pinDirection == (1, -1):
                        moves.append(Move((row, col), (row+1, col-1), self.board))
                if (row+1, col-1) == self.enpassantPossible:
                    if not piecePinned or pinDirection == (1, -1):
                        moves.append(Move((row, col), (row+1, col-1), self.board, isEnpassant=True))
            if col + 1 <= 7:
                if self.board[row+1][col+1][0] == 'w':
                    if not piecePinned or pinDirection == (1, 1):
                        moves.append(Move((row, col), (row+1, col+1), self.board))
                if (row + 1, col + 1) == self.enpassantPossible:
                    if not piecePinned or pinDirection == (1, 1):
                        moves.append(Move((row, col), (row+1, col+1), self.board, isEnpassant=True))

    '''
    Get all possible rook moves for rook at row, col and add to moves
    '''
    def getRookMoves(self, row, col, moves):
        piecePinned = False
        pinDirection = ()

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[row][col][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for dir in directions:
            for i in range (1, 8):
                endRow = row + dir[0] * i
                endCol = col + dir[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == dir or pinDirection == (-dir[0], -dir[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == '--': 
                            moves.append(Move((row, col), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((row, col), (endRow, endCol), self.board))
                            break
                        else:
                            break
                else:
                    break


    '''
    Get all possible knight moves for knight at row, col and add to moves
    '''
    def getKnightMoves(self, row, col, moves):
        piecePinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if(self.pins[i][0] == row and self.pins[i][1] == col):
                piecePinned = True
                self.pins.remove(self.pins[i])
                break
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for move in knightMoves:
            endRow = row + move[0]
            endCol = col + move[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:
                        moves.append(Move((row, col), (endRow, endCol), self.board))

    '''
    Get all possible bishop moves for bishop at row, col and add to moves
    '''
    def getBishopMoves(self, row, col, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) -1, -1, -1):
            if(self.pins[i][0] == row and self.pins[i][1] == col):
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        directions = ((-1, -1), (1, -1), (1, 1), (-1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for dir in directions:
            for i in range (1, 8):
                endRow = row + dir[0] * i
                endCol = col + dir[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == dir or pinDirection == (-dir[0], -dir[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == '--':
                            moves.append(Move((row, col), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((row, col), (endRow, endCol), self.board))
                            break
                        else:
                            break
                else:
                    break

    '''
    Get all possible queen moves for queen at row, col and add to moves
    '''
    def getQueenMoves(self, row, col, moves):
        self.getBishopMoves(row, col, moves)
        self.getRookMoves(row, col, moves)

    '''
    Get all possible king moves for king at row, col and add to moves
    '''
    def getKingMoves(self, row, col, moves):
        allyColor = 'w' if self.whiteToMove else 'b'
        direcions = ((-1, -1), (1, -1), (1, 1), (-1, 1), (-1, 0), (0, -1), (1, 0), (0, 1))
        for i in range(8):
            endRow = row + direcions[i][0]
            endCol = col + direcions[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8 :
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    if allyColor == 'w':
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    if allyColor == 'w':
                        self.whiteKingLocation = (row, col)
                    else:
                        self.blackKingLocation = (row, col)
    
    def getCastleMoves(self, row, col, moves, ):
        if self.inCheck: 
            return
        if (self.whiteToMove and self.currentCastleRights.wks) or (not self.whiteToMove and self.currentCastleRights.bks):
            self.getKingSideCastleMoves(row, col, moves)
        if (self.whiteToMove and self.currentCastleRights.wqs)  or (not self.whiteToMove and self.currentCastleRights.bqs):
            self.getQueenSideCastleMoves(row, col, moves )
    
    def getKingSideCastleMoves(self, row, col, moves):
        if self.board[row][col+1] == "--" and self.board[row][col+2] == "--":
            if not self.squareUnderAttack(row, col + 1) and not self.squareUnderAttack(row, col + 2):
                moves.append(Move((row, col), (row, col+2), self.board, isCastle=True))
    
    def getQueenSideCastleMoves(self, row, col, moves):
        if self.board[row][col-1] == "--" and \
            self.board[row][col-2] == "--" and \
            self.board[row][col-3] == "--":
            if not self.squareUnderAttack(row, col - 1) and not self.squareUnderAttack(row, col - 2):
                moves.append(Move((row, col), (row, col-2), self.board, isCastle=True))

