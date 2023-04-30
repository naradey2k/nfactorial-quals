import pygame
import time

from solver import *
from level import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
L_GREEN = (150, 255, 150)
RED = (255, 0, 0)
L_RED = (255, 204, 203)
GRAY = (60, 60, 60)
L_GRAY = (220, 220, 220)
YELLOW = (255, 255, 0)

WIDTH = HEIGHT = 50

MARGIN = 5
numbers_1to9 = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8,
                pygame.K_9]

size = (500, 500)

pygame.init()
font = pygame.font.Font('freesansbold.ttf', 32)

done = False

def cheatingAllTheWay():
    for row in range(len(Board)):
        for column in range(len(Board[row])):
            Board[row][column] = solvedBoard[row][column]
            addNumToBoard(Board[row][column], row, column, L_GREEN)
            time.sleep(0.05)
            pygame.display.flip()

    finish()


def addNumToBoard(number, row, column, color):
    addNewRect(row, column, WHITE, 5)
    addNewRect(row, column, color, None)

    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(str(number), True, BLACK, )
    textRect = text.get_rect()
    textRect.center = ((MARGIN + WIDTH) * column + MARGIN + WIDTH / 2, (MARGIN + HEIGHT) * row + MARGIN + WIDTH / 2)
    screen.blit(text, textRect)

    drawTheBorder()


def finish():
    if solvedBoard == Board:
        print("1")
    else:
        print("0")


def addNewRect(row, col, color, width):
    rectSize = pygame.Rect((MARGIN + WIDTH) * col + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH,
                           HEIGHT)
    if width is not None:
        pygame.draw.rect(screen, color, rectSize, width)
    else:
        pygame.draw.rect(screen, color, rectSize)


def flickering(timeFlickering, color):
    addNewRect(row, column, color, 5)
    pygame.display.flip()
    time.sleep(timeFlickering)
    addNewRect(row, column, WHITE, 5)
    pygame.display.flip()
    time.sleep(timeFlickering)
    addNewRect(row, column, color, 5)
    pygame.display.flip()
    time.sleep(timeFlickering)
    addNewRect(row, column, WHITE, 5)
    pygame.display.flip()


def drawTheBorder():
    dif = 500 // 9
    for i in range(10):
        thick = 5
        pygame.draw.line(screen, GRAY, (0, i * dif + 2), (500, i * dif + 2), thick)
        pygame.draw.line(screen, GRAY, (i * dif + 2, 0), (i * dif + 2, 500), thick)

    for i in range(10):
        if i % 3 == 0:
            thick = 8
            pygame.draw.line(screen, BLACK, (0, i * dif), (500, i * dif), thick)
            pygame.draw.line(screen, BLACK, (i * dif, 0), (i * dif, 500), thick)


def drawInitBoard():
    for row in range(len(Board)):
        for column in range(len(Board[row])):
            color = L_GRAY
            if Board[row][column] == 0:
                color = WHITE

            pygame.draw.rect(screen, color,
                             [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])

            font = pygame.font.Font('freesansbold.ttf', 32)
            if Board[row][column] == 0:
                text = font.render(" ", True, BLACK, )
            else:
                text = font.render(str(Board[row][column]), True, BLACK, )

            textRect = text.get_rect()
            textRect.center = (
                (MARGIN + WIDTH) * column + MARGIN + WIDTH / 2, (MARGIN + HEIGHT) * row + MARGIN + WIDTH / 2)

            screen.blit(text, textRect)
            drawTheBorder()


if __name__ == "__main__":
    flag1 = True

    while flag1:
        level = chooseLevel()
        if level == 1 or level == 2 or level == 3:
            print(level)
            flag1 = False

    pygame.display.set_caption("Судоку")
    screen = pygame.display.set_mode(size)

    sol = mainSolver(level)

    print("решение")
    printBoard(sol)

    pygame.init()
    screen.fill(BLACK)
    drawInitBoard()
    readyForInput = False
    key = None

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key in numbers_1to9:
                    key = chr(event.key)
                if event.key == pygame.K_RETURN:
                    finish()
                if event.key == pygame.K_c:
                    cheatingAllTheWay()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if readyForInput is True:
                    addNewRect(row, column, WHITE, None)
                    drawTheBorder()
                    readyForInput = False

                pos = pygame.mouse.get_pos()
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (WIDTH + MARGIN)

                if Board[row][column] == 0:
                    addNewRect(row, column, YELLOW, 5)
                    readyForInput = True

        if readyForInput and key is not None:
            if int(key) == sol[row][column]:
                Board[row][column] = key
                flickering(0.1, GREEN)
                addNumToBoard(key, row, column, L_GREEN)
            else:
                flickering(0.1, RED)
                addNumToBoard(key, row, column, L_RED)

            drawTheBorder()
            readyForInput = False

        key = None
        pygame.display.flip()
        pygame.display.update()

pygame.quit()
