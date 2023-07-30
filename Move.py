class Move():

    ranksToRows = {'1': 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {value : key for key, value in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {value: key for key, value in filesToCols.items()}

    def __init__(self, startSquare, endSquare, board, isEnpassant = False, isCastle= False):
        self.startRow = startSquare[0]
        self.startCol = startSquare[1]
        self.endRow = endSquare[0]
        self.endCol = endSquare[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isCastle = isCastle
        self.isPawnPromotion = False
        if(self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7):
            self.isPawnPromotion = True
        
        self.isEnpassant = isEnpassant
        if self.isEnpassant:
            self.pieceCaptured = 'bp' if self.pieceMoved == 'wp' else 'wp'
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
