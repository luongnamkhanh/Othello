import random
import copy
import time
import pygame
import sys

pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Othello Board")

WHITE_BOARD = (255, 255, 255)
BLACK_BOARD = (0, 0, 0)
GREEN_BOARD = (0, 188, 140)

FPS = 60


def recursive_draw(x, y, width, height):
    pygame.draw.rect(WIN, BLACK, [x, y, width, height], 1)
    if y >= 800:  # Screen bottom reached.
        return
    # Is the rectangle wide enough to draw again?
    elif x < 800 - width:  # Right screen edge not reached.
        x += width
        # Recursively draw again.
        recursive_draw(x, y, width, height)
    else:
        # Increment y and reset x to 0 and start drawing the next row.
        x = 0
        y += height
        recursive_draw(x, y, width, height)


def black_circle(x, y):
    pygame.draw.circle(WIN, BLACK_BOARD, (x, y), 45)


def white_circle(x, y):
    pygame.draw.circle(WIN, WHITE_BOARD, (x, y), 45)


def flipable_circle(x, y):
    pygame.draw.circle(WIN, BLACK_BOARD, (x, y), 45, 1)


white_circle_list = []
black_circle_list = []
flipable_circle_list = []


def draw_window():
    WIN.fill(GREEN_BOARD)
    recursive_draw(0, 0, 100, 100)
    for value in black_circle_list:
        black_circle(value[0], value[1])
    for value in white_circle_list:
        white_circle(value[0], value[1])
    for value in flipable_circle_list:
        flipable_circle(value[0], value[1])
    pygame.display.update()


def draw_board():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # run = False
                pygame.quit()
                run = False
                sys.exit()
        draw_window()

###################################################################################################
###################################################################################################
###################################################################################################
###################################################################################################

BOARD = [[0] * 8 for _ in range(8)]
SCORE = [0, 0]  # first for black, second for white
EMPTY = 0
BLACK = 1
WHITE = 2
DEPTH = 5
PLAYERS = {BLACK: "Black", WHITE: "White"}
SURROUND_POSITION = [[-1, -1], [-1, 0], [-1, 1],
                     [0, -1], [0, 1],
                     [1, -1], [1, 0], [1, 1]]
POV = {0: "Human", 1: "Computer"}


# 2 players. Player 1 serves as black, player 2 serves as white.
# Black goes first

def initBoard():
    BOARD[3][3] = BOARD[4][4] = WHITE
    BOARD[3][4] = BOARD[4][3] = BLACK


def printFinalBoard(cur_state):
    print("   ", end=" ")
    for _ in range(8):
        print(_, end=" ")
    print("\n")
    for row in range(8):
        print(row, end="   ")
        for col in range(8):
            if (cur_state[row][col] == BLACK):
                print("B", end=" ")
                black_circle_list.append([col * 100 + 50, row * 100 + 50])
            elif (cur_state[row][col] == WHITE):
                print("W", end=" ")
                white_circle_list.append([col * 100 + 50, row * 100 + 50])
            else:
                print(" ", end=" ")
        print()


def printBoard(cur_state, possibleMoves):
    global black_circle_list
    black_circle_list = []
    global white_circle_list
    white_circle_list = []
    global flipable_circle_list
    flipable_circle_list = []
    print("   ", end=" ")
    for _ in range(8):
        print(_, end=" ")
    print("\n")
    for row in range(8):
        print(row, end="   ")
        for col in range(8):
            if (cur_state[row][col] == EMPTY):
                if ([row, col] in possibleMoves):
                    print("*", end=" ")
                    flipable_circle_list.append([col * 100 + 50, row * 100 + 50])
                else:
                    print(" ", end=" ")
            elif (cur_state[row][col] == BLACK):
                print("B", end=" ")
                black_circle_list.append([col * 100 + 50, row * 100 + 50])
            else:
                print("W", end=" ")
                white_circle_list.append([col * 100 + 50, row * 100 + 50])
        print()
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                sys.exit()
        draw_window()
        run = False


def updateScore(cur_state, cur_score):
    cur_score[0] = cur_score[1] = 0
    for row in range(8):
        for col in range(8):
            if cur_state[row][col] == BLACK:
                cur_score[0] += 1
            elif cur_state[row][col] == WHITE:
                cur_score[1] += 1


def printScore(cur_score):
    print("SCORE")
    print("Player 1 - BLACK: " + str(cur_score[0]))
    print("Player 2 - WHITE: " + str(cur_score[1]))
    print("==============================")


# check valid position to play
def isFlippable(cur_state, row, col, player):
    opponent = BLACK if player == WHITE else WHITE
    for pos in SURROUND_POSITION:
        currentRow = row + pos[0]
        currentCol = col + pos[1]
        if currentRow > 7 or currentRow < 0 or currentCol > 7 or currentCol < 0:
            continue
        else:
            currentPiece = cur_state[currentRow][currentCol]
            if (currentPiece == opponent):
                while (currentPiece == opponent):
                    currentRow += pos[0]
                    currentCol += pos[1]
                    if (currentRow > 7 or currentRow < 0 or currentCol > 7 or currentCol < 0):
                        break
                    else:
                        currentPiece = cur_state[currentRow][currentCol]
                if (currentPiece == player):
                    return True
    return False


def flip(cur_state, row, col, player):
    positionToFlip = []
    opponent = BLACK if player == WHITE else WHITE
    for pos in SURROUND_POSITION:
        currentRow = row + pos[0]
        currentCol = col + pos[1]
        if (currentRow > 7 or currentRow < 0 or currentCol > 7 or currentCol < 0):
            continue
        else:
            currentPiece = cur_state[currentRow][currentCol]
            flipThisDirection = False
            if (currentPiece == opponent):
                while (currentPiece == opponent):
                    currentRow += pos[0]
                    currentCol += pos[1]
                    if (currentRow > 7 or currentRow < 0 or currentCol > 7 or currentCol < 0):
                        break
                    else:
                        currentPiece = cur_state[currentRow][currentCol]
                if (currentPiece == player):
                    flipThisDirection = True
                if (flipThisDirection):
                    currentRow = row + pos[0]
                    currentCol = col + pos[1]
                    currentPiece = cur_state[currentRow][currentCol]
                    while (currentPiece == opponent):
                        positionToFlip.append([currentRow, currentCol])
                        currentRow += pos[0]
                        currentCol += pos[1]
                        currentPiece = cur_state[currentRow][currentCol]
    for pos in positionToFlip:
        cur_state[pos[0]][pos[1]] = player


def calculateLegalMoves(cur_state, cur_player):
    legalMoves = []
    for i in range(8):
        for j in range(8):
            if (cur_state[i][j] == EMPTY and isFlippable(cur_state, i, j, cur_player)):
                legalMoves.append([i, j])
                # flipable_circle_list.append([i * 100 + 50, j * 100 + 50])
    return legalMoves


def getBlackMoves(cur_state):
    return calculateLegalMoves(cur_state=cur_state, cur_player=BLACK)


def getWhiteMoves(cur_state):
    return calculateLegalMoves(cur_state=cur_state, cur_player=WHITE)


def showLegalMoves(possibleMoves):
    for move in possibleMoves:
        print(move, end=" ")
    print()


def processMove(cur_state, row, col, player):
    cur_state[row][col] = player
    flip(cur_state, row, col, player)


# check valid input
def isValidMove(cur_state, possibleMoves, row, col, player):
    if (row > 7 or row < 0 or col > 7 or col < 0):
        return False
    proposedMove = [row, col]
    if (cur_state[row][col] != EMPTY):
        return False
    if (proposedMove in possibleMoves):
        return True
    return False


def isGameOver(cur_state):
    return not getBlackMoves(cur_state) and not getWhiteMoves(cur_state)


def main():
    global BOARD
    initBoard()
    turn = 0
    print("WELCOME TO OTHELLO!")
    print("Please select role for each side.")
    print("Select 0 for human, 1 for computer")
    while True:
        black_player = int(input("Black: "))
        if black_player == 0 or black_player == 1:
            break
        else:
            print("Invalid choice")
    while True:
        white_player = int(input("White: "))
        if white_player == 0 or white_player == 1:
            break
        else:
            print("Invalid choice")
    # black_player = white_player = 1
    if (black_player == 1 or white_player == 1):
        print(f"Black will be played by {POV[black_player]}, White will be played by {POV[white_player]}")
        print("Select algorithms for AI to play")
        print("1. Random")
        print("2. Greedy - Maximum strategy")
        print("3. Minimax")
        print("4. Alpha - Beta pruning")
        print("5. Negamax")
        print("6. Negamax with Alpha - Beta pruning")
        if (black_player == 1):
            while True:
                black_ai = int(input("Black: "))
                if 1 <= black_ai <= 6:
                    break
                else:
                    print("Invalid choice")
        if (white_player == 1):
            while True:
                white_ai = int(input("White: "))
                if 1 <= white_ai <= 6:
                    break
                else:
                    print("Invalid choice")
    while (not isGameOver(BOARD)):
        updateScore(BOARD, SCORE)
        printScore(SCORE)
        player = turn % 2 + 1
        possibleMoves = calculateLegalMoves(BOARD, player)
        printBoard(BOARD, possibleMoves)
        print(f"Turn: {turn + 1}, player {player} - {PLAYERS[player]}")
        print(f"{PLAYERS[player]}'s possible move:")
        showLegalMoves(possibleMoves)
        turn += 1
        if (player == BLACK):
            if (not possibleMoves):
                print("NO POSSIBLE MOVES FOR BLACK. SWITCH TURN!\n\n\n")
                continue
            elif (POV[black_player] == "Human"):
                while True:
                    print("Position (row and column separate by space): ", end=" ")
                    row, col = map(int, input().split())
                    if (not isValidMove(BOARD, possibleMoves, row, col, player)):
                        print("Invalid move entered, try again.")
                        continue
                    else:
                        print(f"Player {player} - {PLAYERS[player]} choose: {row}, {col} \n\n")
                        processMove(BOARD, row, col, player)
                        break
            elif (POV[black_player] == "Computer"):
                if black_ai == 1:
                    computerMove = randomMove(possibleMoves)
                elif black_ai == 2:
                    computerMove = greedy(BOARD, player, SCORE, possibleMoves)
                elif black_ai == 3:
                    computerMove = minimax(BOARD, player, DEPTH, True)[2]
                elif black_ai == 4:
                    computerMove = alphaBeta(BOARD, player, DEPTH, float("-inf"), float("inf"), True)[2]
                elif black_ai == 5:
                    computerMove = negamax(BOARD, player, DEPTH)[2]
                elif black_ai == 6:
                    computerMove = negamaxWithAB(BOARD, player, DEPTH, float("-inf"), float("inf"))[2]
                print(f"Player {player} - {PLAYERS[player]} choose: {computerMove[0]}, {computerMove[1]} \n\n")
                processMove(BOARD, computerMove[0], computerMove[1], player)
        elif (player == WHITE):
            if (not possibleMoves):
                print("NO POSSIBLE MOVES FOR WHITE. SWITCH TURN!\n\n\n")
                continue
            elif (POV[white_player] == "Human"):
                while True:
                    print("Position (row and column separate by space): ", end=" ")
                    row, col = map(int, input().split())
                    if (not isValidMove(BOARD, possibleMoves, row, col, player)):
                        print("Invalid move entered, try again.")
                        continue
                    else:
                        print(f"Player {player} - {PLAYERS[player]} choose: {row}, {col} \n\n")
                        processMove(BOARD, row, col, player)
                        break
            elif (POV[white_player] == "Computer"):
                if white_ai == 1:
                    computerMove = randomMove(possibleMoves)
                elif white_ai == 2:
                    computerMove = greedy(BOARD, player, SCORE, possibleMoves)
                elif white_ai == 3:
                    computerMove = minimax(BOARD, player, DEPTH, True)[2]
                elif white_ai == 4:
                    computerMove = alphaBeta(BOARD, player, DEPTH, float("-inf"), float("inf"), True)[2]
                elif white_ai == 5:
                    computerMove = negamax(BOARD, player, DEPTH)[2]
                elif white_ai == 6:
                    computerMove = negamaxWithAB(BOARD, player, DEPTH, float("-inf"), float("inf"))[2]
                print(f"Player {player} - {PLAYERS[player]} choose: {computerMove[0]}, {computerMove[1]} \n\n")
                processMove(BOARD, computerMove[0], computerMove[1], player)
    updateScore(BOARD, SCORE)
    printScore(SCORE)
    printFinalBoard(BOARD)
    if (SCORE[0] > SCORE[1]):
        print(f"{PLAYERS[1]} wins")
    elif (SCORE[0] < SCORE[1]):
        print(f"{PLAYERS[2]} wins")
    else:
        print("The game is draw.")
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # run = False
                pygame.quit()
                run = False
                sys.exit()
        draw_window()


def randomMove(possibleMoves):
    random.shuffle(possibleMoves)
    return random.choice(possibleMoves)


# maximum strategy
def greedy(cur_state, player, cur_score, possibleMoves):
    maximumScore = float('-inf')
    maximumMoves = []
    for pos in possibleMoves:
        scoreDiff = maximumStrategy(copy.deepcopy(cur_state), pos, cur_score, player)
        if (scoreDiff > maximumScore):
            maximumScore = scoreDiff
            maximumMoves.clear()
        elif (scoreDiff < maximumScore):
            continue
        maximumMoves.append(pos)
    return randomMove(maximumMoves)


def maximumStrategy(cur_state, move, cur_score, player):
    possible_score = [0, 0]
    processMove(cur_state, move[0], move[1], player)
    updateScore(cur_state, possible_score)
    return possible_score[player - 1] - cur_score[player - 1]


def pieceDifference(possibleState, maximizePlayer):
    opponent = BLACK if maximizePlayer == WHITE else WHITE
    maxPlayerScore = 0
    opponentScore = 0
    for row in range(8):
        for col in range(8):
            if possibleState[row][col] == maxPlayerScore:
                maxPlayerScore += 1
            elif possibleState[row][col] == opponent:
                opponentScore += 1
    if (maxPlayerScore > opponentScore):
        return (maxPlayerScore / (maxPlayerScore + opponentScore)) * 100
    elif (maxPlayerScore < opponentScore):
        return - (opponentScore / (maxPlayerScore + opponentScore)) * 100
    else:
        return 0


def cornerCaptions(possibleState, maximizePlayer):
    opponent = BLACK if maximizePlayer == WHITE else WHITE
    maxPlayerScore = 0
    opponentScore = 0
    if (possibleState[0][0] == maximizePlayer):
        maxPlayerScore += 1
    elif (possibleState[0][0] == opponent):
        opponentScore += 1
    if (possibleState[0][7] == maximizePlayer):
        maxPlayerScore += 1
    elif (possibleState[0][7] == opponent):
        opponentScore += 1
    if (possibleState[7][0] == maximizePlayer):
        maxPlayerScore += 1
    elif (possibleState[7][0] == opponent):
        opponentScore += 1
    if (possibleState[7][7] == maximizePlayer):
        maxPlayerScore += 1
    elif (possibleState[7][7] == opponent):
        opponentScore += 1
    return (maxPlayerScore - opponentScore) * 25


def cornerCloseness(possibleState, maximizePlayer):
    opponent = BLACK if maximizePlayer == WHITE else WHITE
    maxPlayerScore = 0
    opponentScore = 0
    closeCorner = [[0, 1], [1, 0], [1, 1], [0, 6], [1, 7], [1, 6], [6, 0], [7, 1], [6, 1], [6, 7], [7, 6], [6, 6]]
    corners = [[0, 0], [0, 7], [7, 0], [7, 7]]
    for i in range(4):
        if possibleState[corners[i][0]][corners[i][1]] == EMPTY:
            if possibleState[closeCorner[3 * i][0]][closeCorner[3 * i][1]] == maximizePlayer:
                maxPlayerScore += 1
            elif possibleState[closeCorner[3 * i][0]][closeCorner[3 * i][1]] == opponent:
                opponentScore += 1
            if possibleState[closeCorner[3 * i + 1][0]][closeCorner[3 * i + 1][1]] == maximizePlayer:
                maxPlayerScore += 1
            elif possibleState[closeCorner[3 * i + 1][0]][closeCorner[3 * i + 1][1]] == opponent:
                opponentScore += 1
            if possibleState[closeCorner[3 * i + 2][0]][closeCorner[3 * i + 2][1]] == maximizePlayer:
                maxPlayerScore += 1
            elif possibleState[closeCorner[3 * i + 2][0]][closeCorner[3 * i + 2][1]] == opponent:
                opponentScore += 1
    return (opponentScore - maxPlayerScore) * 12.5


def mobility(possibleState, maximizePlayer):
    opponent = BLACK if maximizePlayer == WHITE else WHITE
    maxPlayerScore = len(calculateLegalMoves(possibleState, maximizePlayer))
    opponentScore = len(calculateLegalMoves(possibleState, opponent))
    if (maxPlayerScore > opponentScore):
        return (maxPlayerScore / (maxPlayerScore + opponentScore)) * 100
    elif (maxPlayerScore < opponentScore):
        return - (opponentScore / (maxPlayerScore + opponentScore)) * 100
    else:
        return 0


def frontierPiece(possibleState, maximizePlayer):
    opponent = BLACK if maximizePlayer == WHITE else WHITE
    maxPlayerScore = 0
    opponentScore = 0
    for row in range(8):
        for col in range(8):
            if (possibleState[row][col] == maximizePlayer):
                for pos in SURROUND_POSITION:
                    if (0 <= row + pos[0] <= 7) and (0 <= col + pos[1] <= 7) and (
                            possibleState[row + pos[0]][col + pos[1]] == EMPTY):
                        maxPlayerScore += 1
                        break
            elif (possibleState[row][col] == opponent):
                for pos in SURROUND_POSITION:
                    if (0 <= row + pos[0] <= 7) and (0 <= col + pos[1] <= 7) and (
                            possibleState[row + pos[0]][col + pos[1]] == EMPTY):
                        opponentScore += 1
                        break
            else:
                continue
    if (maxPlayerScore > opponentScore):
        return - (maxPlayerScore / (maxPlayerScore + opponentScore)) * 100
    elif (maxPlayerScore < opponentScore):
        return (opponentScore / (maxPlayerScore + opponentScore)) * 100
    else:
        return 0


def staticWeight(possibleState, maximizePlayer):
    weight = [[20, -3, 11, 8, 8, 11, -3, 20],
              [-3, -7, -4, 1, 1, -4, -7, -3],
              [11, -4, 2, 2, 2, 2, -4, 11],
              [8, 1, 2, -3, -3, 2, 1, 8],
              [8, 1, 2, -3, -3, 2, 1, 8],
              [11, -4, 2, 2, 2, 2, -4, 11],
              [-3, -7, -4, 1, 1, -4, -7, -3],
              [20, -3, 11, 8, 8, 11, -3, 20]]
    opponent = BLACK if maximizePlayer == WHITE else WHITE
    score = 0
    for row in range(8):
        for col in range(8):
            if (possibleState[row][col] == maximizePlayer):
                score += weight[row][col]
            elif (possibleState[row][col] == opponent):
                score -= weight[row][col]
    return score


def heuristic(possibleState, maximizePlayer):
    return pieceDifference(possibleState, maximizePlayer) * 400 \
           + cornerCaptions(possibleState, maximizePlayer) * 850 \
           + cornerCloseness(possibleState, maximizePlayer) * 600 \
           + mobility(possibleState, maximizePlayer) * 500 \
           + frontierPiece(possibleState, maximizePlayer) * 200 \
           + staticWeight(possibleState, maximizePlayer) * 50


def minimax(cur_state, player, depth, maximizing):
    choices = calculateLegalMoves(BOARD, player)
    if depth == 0 or len(choices) == 0:
        return [heuristic(cur_state, player), cur_state]
    boards = []
    for choice in choices:
        test = copy.deepcopy(BOARD)
        processMove(test, choice[0], choice[1], player)
        boards.append(test)
    if maximizing:
        bestValue = float("-inf")
        bestBoard = []
        bestChoice = []
        for board in boards:
            val = minimax(board, 3 - player, depth - 1, False)[0]
            if val > bestValue:
                bestValue = val
                bestBoard = board
                bestChoice = choices[boards.index(board)]
        return [bestValue, bestBoard, bestChoice]
    else:
        bestValue = float("inf")
        bestBoard = []
        bestChoice = []
        for board in boards:
            val = minimax(board, 3 - player, depth - 1, True)[0]
            if (val < bestValue):
                bestValue = val
                bestBoard = board
                bestChoice = choices[boards.index(board)]
        return [bestValue, bestBoard, bestChoice]


def alphaBeta(cur_state, player, depth, alpha, beta, maximizing):
    choices = calculateLegalMoves(BOARD, player)
    if depth == 0 or len(choices) == 0:
        return [heuristic(cur_state, player), cur_state]
    boards = []
    for choice in choices:
        test = copy.deepcopy(BOARD)
        processMove(test, choice[0], choice[1], player)
        boards.append(test)
    if maximizing:
        v = float("-inf")
        bestBoard = []
        bestChoice = []
        for board in boards:
            boardValue = alphaBeta(board, 3 - player, depth - 1, alpha, beta, False)[0]
            if boardValue > v:
                v = boardValue
                bestBoard = board
                bestChoice = choices[boards.index(board)]
            alpha = max(alpha, v)
            if (beta <= alpha):
                break
        return [v, bestBoard, bestChoice]
    else:
        v = float("inf")
        bestBoard = []
        bestChoice = []
        for board in boards:
            boardValue = alphaBeta(board, 3 - player, depth - 1, alpha, beta, True)[0]
            if (boardValue < v):
                v = boardValue
                bestBoard = board
                bestChoice = choices[boards.index(board)]
            beta = min(beta, v)
            if (beta <= alpha):
                break
        return [v, bestBoard, bestChoice]


def negamax(cur_state, player, depth):
    choices = calculateLegalMoves(BOARD, player)
    if depth == 0 or len(choices) == 0:
        return [heuristic(cur_state, player), cur_state]
    boards = []
    for choice in choices:
        test = copy.deepcopy(BOARD)
        processMove(test, choice[0], choice[1], player)
        boards.append(test)
    val = float("-inf")
    for board in boards:
        boardVal = -negamax(board, 3 - player, depth - 1)[0]
        if (boardVal > val):
            val = boardVal
            bestBoard = board
            bestChoice = choices[boards.index(board)]
    return [val, bestBoard, bestChoice]


def negamaxWithAB(cur_state, player, depth, alpha, beta):
    choices = calculateLegalMoves(BOARD, player)
    if depth == 0 or len(choices) == 0:
        return [heuristic(cur_state, player), cur_state]
    boards = []
    for choice in choices:
        test = copy.deepcopy(BOARD)
        processMove(test, choice[0], choice[1], player)
        boards.append(test)
    val = float("-inf")
    for board in boards:
        boardVal = -negamaxWithAB(board, 3 - player, depth - 1, - beta, - alpha)[0]
        if boardVal > val:
            val = boardVal
            bestBoard = board
            bestChoice = choices[boards.index(board)]
        alpha = max(alpha, val)
        if (alpha >= beta):
            break
    return [val, bestBoard, bestChoice]


if __name__ == '__main__':
    main()
