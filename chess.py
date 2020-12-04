path = 'c:/Users/keno.deary/Desktop/chess/'

import pygame
import time
import chess_Engine

pygame.init()

#Define Global Constants
target_fps = 240
width = 448
height = 448
window_width = 800
window_height = 600
board_dimensions = 8
boardX = 64
boardY = 64
sq_size = height // board_dimensions
game_Display = pygame.display.set_mode((window_width, window_height))
icons = {}
small_icons = {}
sounds = {}

font_type = 'cambria'
font = pygame.font.SysFont(font_type, 20)
font2 = pygame.font.SysFont(font_type, 15)
font3 = pygame.font.SysFont(font_type, 30)
white = (255,255,255)
black = (0,0,0)
grey = (105,105,105)
dark = (112,162,163)
light = (177,228,185)

col_num = ['8', '7', '6', '5', '4', '3', '2', '1']
rank_let = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']

def load_Images():
    for piece in pieces:
        icons[piece] = pygame.transform.scale(pygame.image.load(path + 'icons/' + piece + '.png'), (sq_size, sq_size))
    
    for piece in pieces:
        small_icons[piece] = pygame.transform.scale(pygame.image.load(path + 'icons/' + piece + '.png'), (sq_size // 2, sq_size // 2))

def load_Sounds():
    sounds["move_piece"] = pygame.mixer.Sound(path + 'sounds/sound.wav')
    sounds["winner!"] = pygame.mixer.Sound(path + 'sounds/winner!.wav')

def draw_Pieces(screen, board):
    for i in range(board_dimensions):
        for j in range(board_dimensions):
            piece = board[i][j]
            if piece != '..':
                game_Display.blit(icons[piece], pygame.Rect(j*sq_size + boardX, i*sq_size + boardY, sq_size, sq_size))

#Create Chess Board
def draw_Board(black_ticks_Left, white_ticks_Left):

    # Draws all Titles/Headers/Words on Screen #######################################################################
    black_title = font.render("Black", 1, dark)
    white_title = font.render("White", 1, light)
    black_timer_title = font.render("Time Left:   " + seconds_To_MMSS(black_ticks_Left / target_fps), 1, dark)
    white_timer_title = font.render("Time Left:   " + seconds_To_MMSS(white_ticks_Left / target_fps), 1, light)
    black_captures_title = font.render("Captured Pieces:", 1, dark)
    white_captures_title = font.render("Captured Pieces:", 1, light)
    game_Display.blit(black_title, ((width // 2) + boardX - 20, 10))
    game_Display.blit(white_title, ((width // 2) + boardX - 20, 550))
    game_Display.blit(black_timer_title, (550, 90))
    game_Display.blit(white_timer_title, (550, 420))
    game_Display.blit(black_captures_title, (550, 120))
    game_Display.blit(white_captures_title, (550, 450))

    count = 0
    for i in col_num:
        rank_letters = font2.render(str(i), 1, black)
        game_Display.blit(rank_letters, (boardX - 15, boardY + 15 + count))
        count = count + sq_size 
    
    count = 0
    half_sq_size = sq_size // 2 - 3
    for i in rank_let:
        rank_letters = font2.render(i, 1, black)
        game_Display.blit(rank_letters, (boardX + half_sq_size + count, boardY + height))
        count = count + sq_size

    #############################################################################################################


    colors = [light, dark]
    # Draws the Board
    for i in range(board_dimensions):
        for j in range(board_dimensions):
            color = colors[((i+j) % 2)]
            pygame.draw.rect(game_Display, color, pygame.Rect(i*sq_size + boardX, j*sq_size + boardY, sq_size, sq_size))
    pygame.draw.rect(game_Display, dark, [boardX, boardY, board_dimensions*sq_size, board_dimensions*sq_size], 3)


def move_Assist(game_Display, gs, check_Moves, square_chosen):
    if square_chosen != ():
        row = square_chosen[0]
        col = square_chosen[1]

        if gs.board[row][col][0] == ('w' if gs.white_Move else 'b'):
            highlight = pygame.Surface((sq_size, sq_size))
            highlight.set_alpha(100) #Sets opacity
            highlight.fill(pygame.Color('blue'))
            game_Display.blit(highlight, ((col * sq_size) + boardX, (row * sq_size) + boardY))
            highlight.fill(pygame.Color('yellow'))
            for move in check_Moves:
                if move.start_Row == row and move.start_Col == col:
                    game_Display.blit(highlight, ((move.end_Col * sq_size) + boardX, (move.end_Row * sq_size) + boardY))


def player_Win(game_Display, text, winning_color):
    game_Over_Text = font3.render(text, 1, winning_color)
    game_Display.blit(game_Over_Text, (100, (height//2) + 25))
    
def player_Tie(game_Display, text, winning_color):
    game_Over_Text = font3.render(text, 1, winning_color)
    game_Display.blit(game_Over_Text, (120, (height//2) + 25))

def replay_Text(game_Display, text, winning_color):
    game_Over_Text = font3.render(text, 1, winning_color)
    game_Display.blit(game_Over_Text, (160, (height//2) + 65))

def draw_GameState(game_Display, gs, check_Moves, square_chosen):
    draw_Board(gs.black_ticks_Left, gs.white_ticks_Left)
    move_Assist(game_Display, gs, check_Moves, square_chosen)
    draw_Pieces(game_Display, gs.board)


def pieces_Captured(gs, white_captured, black_captured):
    white_x = 1
    black_x = 1
    white_y = 0
    black_y = 0

    for piece in white_captured:
        if white_x > 8:
            white_x = 1
            white_y += (sq_size // 2)
        
        game_Display.blit(small_icons[piece], pygame.Rect((sq_size // 2 * white_x) + 510, 475 + white_y, sq_size // 2, sq_size // 2))
        white_x += 1

    for piece in black_captured:
        if black_x > 8:
            black_x = 1
            black_y += (sq_size // 2)

        game_Display.blit(small_icons[piece], pygame.Rect((sq_size // 2 * black_x) + 510, 145 + black_y, sq_size // 2, sq_size // 2))
        black_x += 1


def checkmate_stalemate(gs, game_Over):
    if gs.checkmate:
        game_Over = True

        sounds["winner!"].play()

        if gs.white_Move:
            player_Win(game_Display, 'Black Wins by checkmate!', black)
            replay_Text(game_Display, 'Press \'R\' to replay.', black)
        else:
            player_Win(game_Display, 'White Wins by checkmate!', white)
            replay_Text(game_Display, 'Press \'R\' to replay.', white)
    elif gs.stalemate:
        game_Over = True
        sounds["winner!"].play()
        player_Tie(game_Display, 'It\'s a draw by stalemate!', grey)
        replay_Text(game_Display, 'Press \'R\' to replay.', grey)


def player_Countdown(gs, game_Over):
    if gs.timeout:
        game_Over = True

        if gs.black_ticks_Left <= 0:
            sounds["winner!"].play()
            player_Tie(game_Display, 'White Wins by timeout!', white)
            replay_Text(game_Display, 'Press \'R\' to replay.', white)
        else:
            sounds["winner!"].play()
            player_Tie(game_Display, 'Black Wins by timeout!', black)
            replay_Text(game_Display, 'Press \'R\' to replay.', black)

    if not game_Over:
        if gs.white_Move:
            gs.white_ticks_Left -= 1
        else:
            gs.black_ticks_Left -= 1

        if gs.white_ticks_Left <= 0 or gs.black_ticks_Left <= 0:
            gs.white_ticks_Left = max(0, gs.white_ticks_Left)
            gs.black_ticks_Left = max(0, gs.black_ticks_Left)

            gs.timeout = True


def seconds_To_MMSS(seconds):
    minutes = seconds // 60
    return "%02d:%02d" % (minutes % 60, seconds % 60)


def main():
    ### Constants for main() function ###
    load_Images()
    load_Sounds()
    game_Display.fill(white)
    draw_Board(0, 0)
    square_chosen = ()
    player_Clicks = []
    move_Made = False
    game_Over = False

    user_input = int(input('How much minutes for each side? Enter an integer: '))
    timeLeft = target_fps * (user_input * 60)

    gs = chess_Engine.GameState(timeLeft)
    check_Moves = gs.check_Moves()

    prev_time = time.time()

    chessRunning = True
    while chessRunning:
        game_Display.fill(white)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                chessRunning = False

            ### Player interact with mouse ###   
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_Over == False:
                    loc = pygame.mouse.get_pos()
                    col = ((loc[0] // sq_size) - 1)
                    row = ((loc[1] // sq_size) - 1)
                    if square_chosen == (row, col):
                        square_chosen = ()
                        player_Clicks = []
                    elif col <= 7 and col >= 0 and row <= 7 and row >= 0: #If player clicks are outside of board, do nothing.
                        square_chosen = (row, col)
                        player_Clicks.append(square_chosen)
                    
                    if len(player_Clicks) == 2: #first click chooses piece, second click moves piece.
                        move = chess_Engine.Move(player_Clicks[0], player_Clicks[1], gs.board)
                        for count in range(len(check_Moves)):
                            if move == check_Moves[count]:
                                sounds["move_piece"].play()
                                gs.make_Move(check_Moves[count])
                                move_Made = True
                                square_chosen = () #re-initalize player clicks
                                player_Clicks = [] #re-initalize player clicks
                        
                        if not move_Made:
                            player_Clicks = [square_chosen]


            ### Player interact with keys ###   
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u: #if player presses 'u', undo last move
                    gs.undo_Move()
                    move_Made = True
                if event.key == pygame.K_r: #if player presses 'r', reset board
                    gs = chess_Engine.GameState(timeLeft)
                    check_Moves = gs.check_Moves()
                    square_chosen = ()
                    player_Clicks = []
                    move_Made = False
                    game_Over = False

        if move_Made:
            check_Moves = gs.check_Moves()
            # Prints square of first click and second click
            print(move.chess_Notation())

            move_Made = False

        # Limits to 60 fps  ################################################################
        curr_time = time.time() # Time after processing
        diff = curr_time - prev_time 
        delay = max(1.0 / target_fps - diff, 0)
        time.sleep(delay)
        fps = 1.0 / (delay + diff) 
        prev_time = curr_time
        ####################################################################################

        draw_GameState(game_Display, gs, check_Moves, square_chosen)
        if not game_Over:
            pieces_Captured(gs, gs.black_captured, gs.white_captured)
            checkmate_stalemate(gs, game_Over)
            player_Countdown(gs, game_Over)

        pygame.display.update()



if __name__ == '__main__':
    main()
