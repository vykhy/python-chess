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
    
    '''
    Takes a move and executes it. Will not work for castling, pawn promotion and en-passant
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
    
    '''
    Undo the last move
    '''
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
    
    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        return self.getAllPossibleMoves()

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
        if self.whiteToMove:
            if self.board[row-1][col] == '--':
                moves.append(Move((row, col), (row-1, col), self.board))
                if row == 6 and self.board[row-2][col] == '--':
                    moves.append(Move((row, col), (row-2, col), self.board))
            if col - 1 >= 0:
                if self.board[row-1][col-1][0] == 'b':
                    moves.append(Move((row, col), (row-1, col-1), self.board))
            if col + 1 <= 7:
                if self.board[row-1][col+1][0] == 'b':
                    moves.append(Move((row, col), (row-1, col+1), self.board))
        else:
            if self.board[row+1][col] == '--':
                moves.append(Move((row, col), (row+1, col), self.board))
                if row == 1 and self.board[row+2][col] == '--':
                    moves.append(Move((row, col), (row+2, col), self.board))
            if col > 1:
                if self.board[row+1][col-1][0] == 'w':
                    moves.append(Move((row, col), (row+1, col-1), self.board))
            if col < 6:
                if self.board[row+1][col+1][0] == 'w':
                    moves.append(Move((row, col), (row+1, col+1), self.board))

    '''
    Get all possible rook moves for rook at row, col and add to moves
    '''
    def getRookMoves(self, row, col, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for dir in directions:
            for i in range (1, 8):
                endRow = row + dir[0] * i
                endCol = col + dir[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
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
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for move in knightMoves:
            endRow = row + move[0]
            endCol = col + move[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor or endPiece == '--':
                    moves.append(Move((row, col), (endRow, endCol), self.board))

    '''
    Get all possible bishop moves for bishop at row, col and add to moves
    '''
    def getBishopMoves(self, row, col, moves):
        directions = ((-1, -1), (1, -1), (1, 1), (-1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for dir in directions:
            for i in range (1, 8):
                endRow = row + dir[0] * i
                endCol = col + dir[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
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
        direcions = ((-1, -1), (1, -1), (1, 1), (-1, 1), (-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for i in range(8):
            endRow = row + direcions[i][0]
            endCol = col + direcions[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8 :
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor:
                    moves.append(Move((row, col), (endRow, endCol), self.board))

class Move():

    ranksToRows = {'1': 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {value : key for key, value in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {value: key for key, value in filesToCols.items()}

    def __init__(self, startSquare, endSquare, board):
        self.startRow = startSquare[0]
        self.startCol = startSquare[1]
        self.endRow = endSquare[0]
        self.endCol = endSquare[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    '''
    Overriding equals method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    
    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]
