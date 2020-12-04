class GameState():
    def __init__(self, ticks_Left):
        '''
        Draws chess pieces and displays over board. Pieces have 2 letters to signifying them.
        First letter is the color, second letter is piece type.
        b = black
        w = white
        K = King
        Q = Queen
        R = Rook
        B = Bishop
        N = Knight
        P = Pawn
        '''

        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['..', '..', '..', '..', '..', '..', '..', '..'],
            ['..', '..', '..', '..', '..', '..', '..', '..'],
            ['..', '..', '..', '..', '..', '..', '..', '..'],
            ['..', '..', '..', '..', '..', '..', '..', '..'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]


        self.white_Move = True
        self.move_Log = []
        self.white_King = (7,4) #initalize king location to determine check/checkmate
        self.black_King = (0,4) #initalize king location to determine check/checkmate
        self.checkmate = False
        self.stalemate = False
        self.timeout = False

        self.white_ticks_Left = ticks_Left
        self.black_ticks_Left = ticks_Left

        self.black_captured = []
        self.white_captured = []
    

    ### Makes move ###
    def make_Move(self, move):
        self.board[move.start_Row][move.start_Col] = '..'
        self.board[move.end_Row][move.end_Col] = move.piece_Moved
        self.move_Log.append(move)

        if move.piece_Captured != '..':
            if self.white_Move:
                self.white_captured.append(move.piece_Captured)
            else:
                self.black_captured.append(move.piece_Captured)

        self.white_Move = not self.white_Move
        if move.piece_Moved == 'wK':
            self.white_King = (move.end_Row, move.end_Col)
        elif move.piece_Moved == 'bK':
            self.black_King = (move.end_Row, move.end_Col)
        
        #Pawn Promotion
        if move.pawn_Promotion:
            self.board[move.end_Row][move.end_Col] = move.piece_Moved[0] + 'Q'
        

    ### Undo last move ###
    def undo_Move(self):
        if len(self.move_Log) != 0:
            move = self.move_Log.pop()
            self.board[move.start_Row][move.start_Col] = move.piece_Moved
            self.board[move.end_Row][move.end_Col] = move.piece_Captured

            self.white_Move = not self.white_Move
            if move.piece_Moved == 'wK':
                self.white_King = (move.start_Row, move.start_Col)
            elif move.piece_Moved == 'bK':
                self.black_King = (move.start_Row, move.start_Col)

            if move.piece_Captured != '..':
                if self.white_Move:
                    if move.piece_Captured in self.white_captured:
                        self.white_captured.remove(move.piece_Captured)
                else:
                    if move.piece_Captured in self.black_captured:
                        self.black_captured.remove(move.piece_Captured)


    # Possible moves when player is checked
    def check_Moves(self):
        moves = self.possible_Moves()
        for i in range(len(moves)-1,-1,-1):
            self.make_Move(moves[i])
            self.white_Move = not self.white_Move #Switches to other player to check if king can move
            if self.in_Check(): #If the move makes the king vulnerable to check...
                moves.remove(moves[i]) # ... the move is removed from the possible_moves.
            self.white_Move = not self.white_Move
            self.undo_Move()
        if len(moves) == 0: #If there are no possible moves for a player...
            if self.in_Check():
                self.checkmate = True # ... if they are in check it's a checkmate.
            else:
                self.stalemate = True # ... if they are not in check it's a stalemate.
        else:
            self.checkmate = False
            self.stalemate = False
        return moves


    # Determines if player is in check.
    def in_Check(self):
        if self.white_Move:
            return self.under_Attack(self.white_King[0], self.white_King[1])
        else:
            return self.under_Attack(self.black_King[0], self.black_King[1])


    # Determines if player is attacking given row and col. This will help with recognizing check/checkmate.
    def under_Attack(self, row, col):
        self.white_Move = not self.white_Move
        opponent_Moves = self.possible_Moves()
        self.white_Move = not self.white_Move
        for move in opponent_Moves:
            if move.end_Row == row and move.end_Col == col:
                return True
        return False


    ### Determines possible move for every piece on board ###
    def possible_Moves(self):
        possible_moves = [] #Total set of all potential moves
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                color = self.board[row][col][0]
                if (self.white_Move and color == 'w') or (not self.white_Move and color == 'b'):
                    piece = self.board[row][col][1] # Gets 2nd letter from self.board to determine piece type. i.e.: 'bQ' = 'Q' = Queen
                    if piece == 'K':
                        self.king_Moves(row, col, possible_moves)
                    elif piece == 'Q':
                        self.queen_Moves(row, col, possible_moves)
                    elif piece == 'R':
                        self.rook_Moves(row, col, possible_moves)
                    elif piece == 'B':
                        self.bishop_Moves(row, col, possible_moves)
                    elif piece == 'N':
                        self.knight_Moves(row, col, possible_moves)
                    elif piece == 'P':
                        self.pawn_Moves(row, col, possible_moves)
        return possible_moves


    '''
    Piece Movement
    Cite: Use of directions (i.e.: ((1,1), (-1,1), (-1,-1), (1,-1)) ) taken from YT video.
    '''
    def king_Moves(self, row, col, possible_moves):
        directions = (1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,1), (-1,-1), (0,-1)
        if self.white_Move:
            color = 'w'
        else:
            color = 'b'

        for i in range(8):
                endRow = row + directions[i][0]
                endCol = col + directions[i][1]
                if endRow >= 0 and endRow < 8 and endCol >= 0 and endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if color != endPiece[0]:
                        possible_moves.append(Move((row, col), (endRow, endCol), self.board))


    def queen_Moves(self, row, col, possible_moves):
        #Queen is a rook + bishop
        self.rook_Moves(row, col, possible_moves)
        self.bishop_Moves(row, col, possible_moves)


    def rook_Moves(self, row, col, possible_moves):
        directions = ((1,0), (-1,0), (0,1), (0,-1))
        if self.white_Move:
            enemy_color = 'b'
        else:
            enemy_color = 'w'
        
        for direction in directions:
            for count in range(1, 8):
                endRow = row + direction[0] * count
                endCol = col + direction[1] * count
                if endRow >= 0 and endRow < 8 and endCol >= 0 and endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '..':
                        possible_moves.append(Move((row, col), (endRow, endCol), self.board))
                    elif endPiece[0] == enemy_color:
                        possible_moves.append(Move((row, col), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break


    def bishop_Moves(self, row, col, possible_moves):
        directions = ((1,1), (-1,1), (-1,-1), (1,-1))
        if self.white_Move:
            enemy_color = 'b'
        else:
            enemy_color = 'w'
        
        for direction in directions:
            for count in range(1,8):
                endRow = row + direction[0] * count
                endCol = col + direction[1] * count
                if endRow >= 0 and endRow < 8 and endCol >= 0 and endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '..': #Checks if squares are empty
                        possible_moves.append(Move((row, col), (endRow, endCol), self.board))
                    elif endPiece[0] == enemy_color: #Checks if last possible capture is a enemy piece
                        possible_moves.append(Move((row, col), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break


    def knight_Moves(self, row, col, possible_moves):
        L_movements = ((2,1), (2,-1), (1,2), (1,-2), (-2,1), (-2,-1), (-1,2), (-1,-2))
        if self.white_Move:
            color = 'w'
        else:
            color = 'b'
        for L in L_movements:
                endRow = row + L[0]
                endCol = col + L[1]
                if endRow >= 0 and endRow < 8 and endCol >= 0 and endCol < 8:
                    endPiece = self.board[endRow][endCol] #Knights can jump over pieces. Do not need to check for '..'
                    if color != endPiece[0]:
                        possible_moves.append(Move((row, col), (endRow, endCol), self.board))


    def pawn_Moves(self, row, col, possible_moves):
        if self.white_Move:
            if self.board[row - 1][col] == '..': #Checks to see if 1 square forward is empty.
                possible_moves.append(Move((row, col), (row - 1, col), self.board))
                if row == 6 and self.board[row - 2][col] == '..': #Checks to see if 1 more square forward is empty if pawn is still in 6th row.
                    possible_moves.append(Move((row, col), (row - 2, col), self.board))
            if col - 1 >= 0: #Pawn left diagonal capture
                if self.board[row - 1][col - 1][0] == 'b':
                    possible_moves.append(Move((row, col), (row - 1, col - 1), self.board))
            if col + 1 <= 7: #Pawn right diagonal capture
                if self.board[row - 1][col + 1][0] == 'b':
                    possible_moves.append(Move((row, col), (row - 1, col + 1), self.board))

        else:
            if self.board[row + 1][col] == '..': #Checks to see if 1 square forward is empty.
                possible_moves.append(Move((row, col), (row + 1, col), self.board))
                if row == 1 and self.board[row + 2][col] == '..': #Checks to see if 1 more square forward is empty if pawn is still in 6th row.
                    possible_moves.append(Move((row, col), (row + 2, col), self.board))
            if col + 1 <= 7: #Pawn left diagonal capture
                if self.board[row + 1][col + 1][0] == 'w':
                    possible_moves.append(Move((row, col), (row + 1, col + 1), self.board))
            if col - 1 >= 0:
                if self.board[row + 1][col - 1][0] == 'w':
                    possible_moves.append(Move((row, col), (row + 1, col - 1), self.board))


class Move():
    '''
    Got ranks_to_rows / files_to_cols from YT video
    '''
    ranks_to_rows = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
    rows_to_ranks = {7: '1', 6: '2', 5: '3', 4: '4', 3: '5', 2: '6', 1: '7', 0: '8'}
    files_to_cols = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    cols_to_files = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

    def __init__(self, start, end, board):
        self.start_Row = start[0]
        self.end_Row = end[0]
        self.start_Col = start[1]
        self.end_Col = end[1]
        self.piece_Moved = board[self.start_Row][self.start_Col]
        self.piece_Captured = board[self.end_Row][self.end_Col]
        self.pawn_Promotion = False
        if (self.piece_Moved == 'wP' and self.end_Row == 0) or (self.piece_Moved == 'bP' and self.end_Row == 7):
            self.pawn_Promotion = True

        #Creates ID that shows piece starting col, starting row, end row and end col in one 4-digit number:
        # i.e.: 2356: Piece moving from COL 2, ROW 3 ---> COL 5, ROW 6
        self.move_ID = self.start_Row * 1000 + self.start_Col * 100 + self.end_Row * 10 + self.end_Col * 1


    '''
    Got def __eq__ idea from YT video
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_ID == other.move_ID
        return False


    def chess_Notation(self):
        return self.rank_File(self.start_Row, self.start_Col) + ' ' + self.rank_File(self.end_Row, self.end_Col)

    def rank_File(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]
