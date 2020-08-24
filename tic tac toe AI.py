import pygame
from collections import defaultdict, Counter
import math
import tkinter
from tkinter import simpledialog

pygame.init()
root = tkinter.Tk()
root.withdraw()

WIDTH = 501
HEIGHT = 501
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('tic-tac-toe')

positions = []
for i in range(2, -1, -1):
    for j in range(2, -1, -1):
        positions.append(((WIDTH - i * 167 - 167, HEIGHT - j * 167 - 167, WIDTH - i * 167, HEIGHT - j * 167)))
positions_copy = positions.copy()


class Board:
    def __init__(self):
        self.numOfLines = 2
    
    def draw(self, win):
        for i in range(self.numOfLines, 0, -1):
            pygame.draw.line(win, (255, 255, 255), (WIDTH - i * 167, 0), (WIDTH - i * 167, HEIGHT))
            pygame.draw.line(win, (255, 255, 255), (0, HEIGHT - i * 167), (WIDTH, HEIGHT - i * 167))

           

            
class Player:
    def __init__(self, pos, letter, color):
        self.x, self.y = pos
        self.letter = letter
        self.color = color
    
    def draw(self, win):
        font = pygame.font.SysFont('comicsans', 200)
        w, h = font.size(self.letter)
        text = font.render(self.letter, True, self.color)
        win.blit(text, (self.x, self.y))



def redraw_window(win):
    win.fill((0, 0, 0), (0, 0, WIDTH, HEIGHT))
    grid.draw(win)
    for obj in player_objects:
        obj.draw(win)
    pygame.display.update()


def check_winner_minimax(board):
    x_positionsX = []
    y_positionsX = []
    x_positionsO = []
    y_positionsO = []
    lstX = []
    lstO = []

    condition1X = False
    condition1O = False

    counter1X = 0
    counter2X = 0
    counter3X = 0
    counter4X = 0
    counter1O = 0
    counter2O = 0
    counter3O = 0
    counter4O = 0

    diagonals1 = [(0, 0), (167, 167), (334, 334)]
    diagonals2 = [(334, 0), (167, 167), (0, 334)]


    for k, v in board.items():
        if v == 'x':
            x_positionsX.append(k[0])
            y_positionsX.append(k[1])
            lstX.append((k[0], k[1]))
        elif v == 'o':
            x_positionsO.append(k[0])
            y_positionsO.append(k[1])
            lstO.append((k[0], k[1]))

    x_counterX = Counter(x_positionsX)
    y_counterX = Counter(y_positionsX)
    x_counterO = Counter(x_positionsO)
    y_counterO = Counter(y_positionsO)

    for v1 in x_counterX.values():
            if v1 >= 3:
                condition1X = True
    for v1 in x_counterO.values():
            if v1 >= 3:
                condition1O = True

    for v1 in y_counterX.values():
            if v1 >= 3:
                condition1X = True
    for v1 in y_counterO.values():
            if v1 >= 3:
                condition1O = True

    for p in diagonals1:
            if p in lstX:
                counter3X += 1
    for p in diagonals1:
            if p in lstO:
                counter3O += 1

    for p in diagonals2:
            if p in lstX:
                counter4X += 1
    for p in diagonals2:
            if p in lstO:
                counter4O += 1

    if condition1X or counter2X >= 3 or counter3X >= 3 or counter4X >= 3:
        return 'x'
    if condition1O or counter2O >= 3 or counter3O >= 3 or counter4O >= 3:
        return 'o'
    if not positions_copy:
        return 'tie'


def best_move(board):
    bestScore = -math.inf
    for k, v in board.items():
        if v is None:
            board[k] = 'x'
            score = minimax(board, 0, False) 
            board[k] = None
            if score > bestScore:
                bestScore = score
                return k



def minimax(board, depth, maximizingplayer):

    winner = check_winner_minimax(board)
    if winner is not None:
        return scores[winner]

    if maximizingplayer:
        bestScore = -math.inf
        for k, v in board.items():
            if v is None:
                board[k] = 'x'
                score = minimax(board, depth + 1, False) 
                board[k] = None
                bestScore = max(score, bestScore)
        return bestScore

    else:
        bestScore = math.inf
        for k, v in board.items():
            if v is None:
                board[k] = 'o'
                score = minimax(board, depth + 1, True) 
                board[k] = None
                bestScore = min(score, bestScore)
        return bestScore


grid = Board()
running = True
turn = 'x'
player_objects = []
player_movements = defaultdict(list)
scores = {'x': 1, 'o': -1, 'tie': 0}
player_movements_copy = player_movements.copy()

board = {}
for pos in positions:
    board.setdefault(pos)


while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if turn == 'x':
            p = best_move(board)
            print(p)
            pos = (p[0] + 47, p[1] +14 )
            player_objects.append(Player(pos, 'x', (255, 10, 10)))
            player_movements['x'].append(p)
            positions_copy.pop(positions_copy.index(p))
            board[p] = 'x'
            turn = 'o'

        if event.type == pygame.MOUSEBUTTONDOWN and turn == 'o':
            x, y = pygame.mouse.get_pos()
            for p in positions_copy:
                if p[2] > x > p[0] and p[3] > y > p[1]:
                    pos = (p[0] + 47, p[1] +14 )
                    player_objects.append(Player(pos, 'o', (10, 10, 255)))
                    player_movements['o'].append(p)
                    positions_copy.pop(positions_copy.index(p))
                    board[p] = 'o'
                    turn = 'x'
                    break

    winner = check_winner_minimax(board)
    if winner is not None:
        if winner == 'tie':
            redraw_window(win)
            simpledialog.messagebox.showinfo('No winner', 'No winner its a draw')
            running = False

        else:
            redraw_window(win)
            simpledialog.messagebox.showinfo('WINNER', f'The winner in player {winner}')
            running = False
   
    redraw_window(win)

pygame.quit()
