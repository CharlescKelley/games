# Tetromino (a Tetris clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, time, pygame, sys, tkinter
from pygame.locals import *

FPS = 25
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOXSIZE = 20
BOARDWIDTH = 14
BOARDHEIGHT = 20
BLANK = '.'
DIFFICULTY = 0
DIFFICULTY_MAX = 99

EXTRA_CHANCE = False
REROLLS = 0

# locking rotation of pieces chance after certain difficulty is selected
STOPROTATION = 0

MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5

# Begin color definitions
# =======================
#                            R    G    B
TEXTCOLOR = WHITE       = (255, 255, 255)
TEXTSHADOWCOLOR = GRAY  = (185, 185, 185)
BGCOLOR = BLACK         = (  0,   0,   0)
RED                     = (155,   0,   0)
LIGHTRED                = (175,  20,  20)
GREEN                   = (  0, 155,   0)
LIGHTGREEN              = ( 20, 175,  20)
BORDERCOLOR = BLUE      = (  0,   0, 155)
LIGHTBLUE               = ( 20,  20, 175)
YELLOW                  = (155, 155,   0)
LIGHTYELLOW             = (175, 175,  20)
PURPLE                  = ( 128,  0, 128)
LIGHTPURPLE             = ( 255,  0, 255)
ORANGE                  = (255,  69,   0)
LIGHTORANGE             = (255, 165,   0)
BROWN                   = (139,  69,  19)
LIGHTBROWN              = (205, 133,  63)
VIOLET                  = (148,   0, 211)
LIGHTVIOLET             = (238, 130, 238)
GREY                    = (128, 128, 128)
LIGHTGREY               = (175, 175, 175)
INDIAN_RED              = (205,  92,  92)
LIGHT_INDIAN_RED        = (240, 128, 128)



COLORS      = (     BLUE,      GREEN,      RED,      YELLOW)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW)

EVIL_COLORS = (PURPLE, ORANGE, GREY)
EVIL_LIGHT_COLORS = (LIGHTPURPLE, LIGHTORANGE, LIGHTGREY)

NICE_COLORS = (BROWN, VIOLET, INDIAN_RED)
NICE_LIGHT_COLORS = (LIGHTBROWN, LIGHTVIOLET, LIGHT_INDIAN_RED)


assert len(COLORS) == len(LIGHTCOLORS) # each color must have light color
# =====================
# End color definitions

# Begin shape definitions
# =======================
TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

PIECES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}

SINGLE_TEMPLATE     = [['.....',
                        '.....',
                        '..O..',
                        '.....',
                        '.....']]

V_TEMPLATE =          [['.....',
                        '.0.0.',
                        '..O..',
                        '.....',
                        '.....'],
                       ['.....',
                        '...0.',
                        '..O..',
                        '...0.',
                        '.....'],
                       ['.....',
                        '.....',
                        '..O..',
                        '.0.0.',
                        '.....'],
                       ['.....',
                        '.0...',
                        '..O..',
                        '.0...',
                        '.....']]


SEAN_TEMPLATE =       [['.....',
                        '.0.0.',
                        '..O..',
                        '.0.0.',
                        '.....']]

EXTRA_CHANCE_TEMPLATE = [['.....',
                          '.....',
                          '..OO.',
                          '.....',
                          '.....'],
                         ['.....',
                          '.....',
                          '..O..',
                          '..O..',
                          '.....'],
                         ['.....',
                          '.....',
                          '.OO..',
                          '.....',
                          '.....'],
                         ['.....',
                          '..O..',
                          '..O..',
                          '.....',
                          '.....']
                         ]

RE_ROLL_TEMPLATE =      [['.....',
                          '.....',
                          '.OOO.',
                          '.....',
                          '.....'],
                         ['.....',
                          '..O..',
                          '..O..',
                          '..O..',
                          '.....']
                         ]

EVIL_PIECES = {"HM": SINGLE_TEMPLATE, "V": V_TEMPLATE, "SEAN": SEAN_TEMPLATE}
EVIL_PIECE_COLOR_NUMBER = {"HM": 0, "V": 1, "SEAN": 2}

NICE_PIECES = {"EC":EXTRA_CHANCE_TEMPLATE, "RR":RE_ROLL_TEMPLATE, "ONE": SINGLE_TEMPLATE}
NICE_PIECE_COLOR_NUMBER = {"EC": 0, "RR": 1, "ONE":2}
# =====================
# End shape definitions

difficulty = tkinter.Tk()
difficulty.geometry("400x150")

frame = tkinter.Frame(difficulty)
frame.pack()

message = tkinter.Label(frame, text="Enter your difficulty below (an integer between 0 and 100\n")
message.pack()

dif = tkinter.Entry(frame)
dif.pack()

def setDifficulty():
    global DIFFICULTY
    temp = dif.get()
    try:
        DIFFICULTY = int(temp)
    except ValueError:
        message.config(text ="Not an integer. Enter an integer between 0 and 100.")
        return -1
    if(DIFFICULTY < 0 or DIFFICULTY > 100):
        DIFFICULTY = 0
        message.config(text ="Number must be an integer between 0 and 100")
        return -1
    difficulty.withdraw()
    difficulty.quit()

choose_dif = tkinter.Button(frame, text = "Confirm Difficulty", command = setDifficulty)
choose_dif.pack()


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
    difficulty.mainloop()
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
    pygame.display.set_caption('Tetromino')

    showTextScreen('Tetromino')
    while True:  # game loop
        pygame.mixer.music.load(random.choice(('tetrisb.mid', 'tetrisc.mid')))
        pygame.mixer.music.play(-1, 0.0)
        runGame()
        pygame.mixer.music.stop()
        showTextScreen('Game Over')


def runGame():
    # setup variables for the start of the game
    global EXTRA_CHANCE
    global REROLLS
    board = getBlankBoard()
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()
    movingDown = False  # note: there is no movingUp variable
    movingLeft = False
    movingRight = False
    score = 0
    level, fallFreq = calculateLevelAndFallFreq(score)

    fallingPiece = getNewPiece()
    nextPiece = getNewPiece()

    while True: # game loop
        if fallingPiece == None:
            # No falling piece in play, so start a new piece at the top
            fallingPiece = nextPiece
            nextPiece = getNewPiece()
            lastFallTime = time.time() # reset lastFallTime

            if not isValidPosition(board, fallingPiece):
                if EXTRA_CHANCE:
                    board = getBlankBoard()
                    EXTRA_CHANCE = False
                else:
                    return  # can't fit a new piece on the board, so game over

        checkForQuit()
        for event in pygame.event.get():  # event handling loop
            if event.type == KEYUP:
                if (event.key == K_p):
                    # Pausing the game
                    DISPLAYSURF.fill(BGCOLOR)
                    pygame.mixer.music.stop()
                    showTextScreen('Paused')  # pause until a key press
                    pygame.mixer.music.play(-1, 0.0)
                    lastFallTime = time.time()
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()
                elif (event.key == K_LEFT or event.key == K_a):
                    movingLeft = False
                elif (event.key == K_RIGHT or event.key == K_d):
                    movingRight = False
                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = False
                elif(event.key == K_r and REROLLS > 0):
                    fallingPiece = getNewPiece()
                    REROLLS -= 1

            elif event.type == KEYDOWN:
                # moving the piece sideways
                movingLeft, movingRight, lastMoveSidewaysTime = moveSideways(event, board, fallingPiece, movingLeft, movingRight, lastMoveSidewaysTime)

                rotatePiece(event, fallingPiece, board)

                # making the piece fall faster with the down key
                if (event.key == K_DOWN or event.key == K_s):
                    movingDown = True
                    if isValidPosition(board, fallingPiece, adjY=1):
                        fallingPiece['y'] += 1
                    lastMoveDownTime = time.time()

                # move the current piece all the way down
                elif event.key == K_SPACE:
                    movingDown = False
                    movingLeft = False
                    movingRight = False
                    for i in range(1, BOARDHEIGHT):
                        if not isValidPosition(board, fallingPiece, adjY=i):
                            break
                    fallingPiece['y'] += i - 1

        # handle moving the piece because of user input
        if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
            if movingLeft and isValidPosition(board, fallingPiece, adjX=-1):
                fallingPiece['x'] -= 1
            elif movingRight and isValidPosition(board, fallingPiece, adjX=1):
                fallingPiece['x'] += 1
            lastMoveSidewaysTime = time.time()

        if movingDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ and isValidPosition(board, fallingPiece, adjY=1):
            fallingPiece['y'] += 1
            lastMoveDownTime = time.time()

        # let the piece fall if it is time to fall
        if time.time() - lastFallTime > fallFreq:
            # see if the piece has landed
            if not isValidPosition(board, fallingPiece, adjY=1):
                # falling piece has landed, set it on the board
                addToBoard(board, fallingPiece)
                score += removeCompleteLines(board)
                level, fallFreq = calculateLevelAndFallFreq(score)
                if(fallingPiece["shape"] == "HM"):
                    holeMaker(fallingPiece, board)
                fallingPiece = None
            else:
                # piece did not land, just move the piece down
                fallingPiece['y'] += 1
                lastFallTime = time.time()

        # drawing everything on the screen
        drawAll(BGCOLOR, board, score, level, nextPiece)
        if fallingPiece != None:
            drawPiece(fallingPiece)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def terminate():
    pygame.quit()
    sys.exit()


def checkForKeyPress():
    # Go through event queue looking for a KEYUP event.
    # Grab KEYDOWN events to remove them from the event queue.
    checkForQuit()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None


def showTextScreen(text):
    # This function displays large text in the
    # center of the screen until a key is pressed.
    # Draw the text drop shadow
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the text
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the additional "Press a key to play." text.
    pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()


def checkForQuit():
    for event in pygame.event.get(QUIT):  # get all the QUIT events
        terminate()  # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP):  # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate()  # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event)  # put the other KEYUP event objects back


def calculateLevelAndFallFreq(score):
    # Based on the score, return the level the player is on and
    # how many seconds pass until a falling piece falls one space.
    level = int(score / 10) + 1
    fallFreq = 0.27 - (level * 0.02)
    return level, fallFreq

def getNewPiece():
    # return a random new piece in a random rotation and color
    piece_type = random.randint(0, 3)
    global STOP_ROTATION
    STOP_ROTATION = random.randint(0, 3)
    if(piece_type == 3):
        good_or_bad = random.randint(0,DIFFICULTY_MAX)
        if(good_or_bad < DIFFICULTY):
            shape = random.choice(list(EVIL_PIECES.keys()))
            newPiece = {'shape': shape,
             'rotation': random.randint(0, len(SINGLE_TEMPLATE) - 1),
             'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
             'y': -2,  # start it above the board (i.e. less than 0)
             'color': EVIL_PIECE_COLOR_NUMBER[shape],
             'alignment': "evil"}
        else:
            shape = random.choice(list(NICE_PIECES.keys()))
            newPiece = {'shape': shape,
                        'rotation': random.randint(0, len(SINGLE_TEMPLATE) - 1),
                        'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                        'y': -2,  # start it above the board (i.e. less than 0)
                        'color': NICE_PIECE_COLOR_NUMBER[shape],
                        'alignment': "nice"}
    else:
        shape = random.choice(list(PIECES.keys()))
        newPiece = {'shape': shape,
                    'rotation': random.randint(0, len(PIECES[shape]) - 1),
                    'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                    'y': -2, # start it above the board (i.e. less than 0)
                    'color': random.randint(0, len(COLORS)-1),
                    'alignment': "neutral"}
    return newPiece


def addToBoard(board, piece):
    # fill in the board based on piece's location, shape, and rotation
    alignment = piece['alignment']
    if alignment == "neutral":
        pieces = PIECES
    elif alignment == "evil":
        pieces = EVIL_PIECES
    elif alignment == "nice":
        pieces = NICE_PIECES

    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if pieces[piece['shape']][piece['rotation']][y][x] != BLANK:
                board[x + piece['x']][y + piece['y']] = [piece['color'], piece['alignment'], piece['shape']]


def getBlankBoard():
    # create and return a new blank board data structure
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT)
    return board


def isOnBoard(x, y):
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT


def isValidPosition(board, piece, adjX=0, adjY=0):
    # Return True if the piece is within the board and not colliding
    alignment = piece['alignment']
    if alignment == "neutral":
        pieces = PIECES
    elif alignment == "evil":
        pieces = EVIL_PIECES
    elif alignment == "nice":
        pieces = NICE_PIECES

    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            isAboveBoard = y + piece['y'] + adjY < 0
            if isAboveBoard or pieces[piece['shape']][piece['rotation']][y][x] == BLANK:
                continue
            if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                return False
    return True


def isCompleteLine(board, y):
    # Return True if the line filled with boxes with no gaps.
    for x in range(BOARDWIDTH):
        if board[x][y] == BLANK:
            return False
    giveSpecialBonuses(board, y)
    return True


def giveSpecialBonuses(board, y):
    # Check if there is an extra chance block in a completed row
    global EXTRA_CHANCE
    global REROLLS
    for x in range(BOARDWIDTH):
        if (board[x][y])[2] == "EC":
            EXTRA_CHANCE = True
        if (board[x][y])[2] == "RR":
            REROLLS += 1


def removeCompleteLines(board):
    # Remove any completed lines on the board, move everything above them down, and return the number of complete lines.
    numLinesRemoved = 0
    y = BOARDHEIGHT - 1  # start y at the bottom of the board
    while y >= 0:
        if isCompleteLine(board, y):
            # Remove the line and pull boxes down by one line.
            for pullDownY in range(y, 0, -1):
                for x in range(BOARDWIDTH):
                    board[x][pullDownY] = board[x][pullDownY-1]
            # Set very top line to blank.
            for x in range(BOARDWIDTH):
                board[x][0] = BLANK
            numLinesRemoved += 1
            # Note on the next iteration of the loop, y is the same.
            # This is so that if the line that was pulled down is also
            # complete, it will be removed.
        else:
            y -= 1  # move on to check next row up
    return numLinesRemoved


def convertToPixelCoords(boxx, boxy):
    # Convert the given xy coordinates of the board to xy
    # coordinates of the location on the screen.
    return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))


def drawAll(BGCOLOR, board, score, level, nextPiece):
    DISPLAYSURF.fill(BGCOLOR)
    drawBoard(board)
    drawStatus(score, level)
    drawNextPiece(nextPiece)
    drawExtraChanceStatus()
    drawReRollsStatus()


def drawBox(boxx, boxy, color, alignment, pixelx=None, pixely=None):
    # draw a single box (each tetromino piece has four boxes)
    # at xy coordinates on the board. Or, if pixelx & pixely
    # are specified, draw to the pixel coordinates stored in
    # pixelx & pixely (this is used for the "Next" piece).
    if alignment == "neutral":
        colors = COLORS
        light_colors = LIGHTCOLORS
    elif alignment == "evil":
        colors = EVIL_COLORS
        light_colors = EVIL_LIGHT_COLORS
    elif alignment == "nice":
        colors = NICE_COLORS
        light_colors = NICE_LIGHT_COLORS

    if color == BLANK:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, colors[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
    pygame.draw.rect(DISPLAYSURF, light_colors[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))


def drawBoard(board):
    # draw the border around the board
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)

    # fill the background of the board
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
    # draw the individual boxes on the board
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if(board[x][y] == BLANK):
                drawBox(x, y, board[x][y], 'neutral')
            else:
                drawBox(x, y, board[x][y][0], board[x][y][1])


def drawStatus(score, level):
    # draw the score text
    scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 150, 20)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

    # draw the level text
    levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (WINDOWWIDTH - 150, 50)
    DISPLAYSURF.blit(levelSurf, levelRect)


def drawPiece(piece, pixelx=None, pixely=None):
    if(piece["alignment"] == "neutral"):
        shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    elif(piece["alignment"] == "evil"):
        shapeToDraw = EVIL_PIECES[piece['shape']][piece['rotation']]
    elif(piece["alignment"] == "nice"):
        shapeToDraw = NICE_PIECES[piece['shape']][piece['rotation']]

    if pixelx == None and pixely == None:
        # if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

    # draw each of the boxes that make up the piece
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBox(None, None, piece['color'], piece['alignment'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))


def drawNextPiece(piece):
    # draw the "next" text
    nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 120, 80)
    DISPLAYSURF.blit(nextSurf, nextRect)
    # draw the "next" piece
    drawPiece(piece, pixelx=WINDOWWIDTH-120, pixely=100)


def drawExtraChanceStatus():
    if EXTRA_CHANCE:
        ec_status = "Yes"
    else:
        ec_status = "No"
    nextSurf = BASICFONT.render('Extra Chance?  ' + ec_status, True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 170, 200)
    DISPLAYSURF.blit(nextSurf, nextRect)


def drawReRollsStatus():
    nextSurf = BASICFONT.render('Re-rolls:  ' + str(REROLLS), True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 170, 300)
    DISPLAYSURF.blit(nextSurf, nextRect)


def moveSideways(event, board, fallingPiece, movingLeft, movingRight, lastMoveSidewaysTime):
    if (event.key == K_LEFT or event.key == K_a) and isValidPosition(board, fallingPiece, adjX=-1):
        fallingPiece['x'] -= 1
        return (True, False, time.time())

    elif (event.key == K_RIGHT or event.key == K_d) and isValidPosition(board, fallingPiece, adjX=1):
        fallingPiece['x'] += 1
        return(False, True, time.time())
    return(movingLeft, movingRight, lastMoveSidewaysTime)


def rotatePiece(event, fallingPiece, board):
    alignment = fallingPiece['alignment']
    if alignment == "neutral":
        pieces = PIECES
    elif alignment == "evil":
        pieces = EVIL_PIECES
    elif alignment == "nice":
        pieces = NICE_PIECES

    # rotating the piece (if there is room to rotate)
    # no rotation of a piece
    if STOP_ROTATION == 3 and DIFFICULTY >= 75:
        pass
    # regular piece rotation
    elif STOP_ROTATION < 15:
        if event.key == K_UP or event.key == K_w:
            fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(pieces[fallingPiece['shape']])
            if not isValidPosition(board, fallingPiece):
                fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(pieces[fallingPiece['shape']])
        elif event.key == K_q:  # rotate the other direction
            fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(pieces[fallingPiece['shape']])
            if not isValidPosition(board, fallingPiece):
                fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(pieces[fallingPiece['shape']])


def holeMaker(piece, board):
    if(piece['y'] < BOARDHEIGHT - 3):
        to_delete = random.randint(piece['y'] + 3, BOARDHEIGHT - 1)
        board[piece['x'] + 2][to_delete] = BLANK

if __name__ == '__main__':
    main()