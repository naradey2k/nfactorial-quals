import random
import copy

def printBoard(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")
        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")


def findEmpty(board):
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == 0:
                return y, x

    return None


def validCheck(board, number, coordinates):
    for x in range(len(board[0])):
        if number == board[coordinates[0]][x] and coordinates[1] != x:
            return False

    for y in range(len(board)):
        if number == board[y][coordinates[1]] and coordinates[0] != y:
            return False

    box_x = coordinates[1] // 3
    box_y = coordinates[0] // 3

    for y in range(box_y * 3, box_y * 3 + 3):
        for x in range(box_x * 3, box_x * 3 + 3):
            if number == board[y][x] and (y, x) != coordinates:
                return False

    return True


def generateRandomBoard(board):
    find = findEmpty(board)
    if find is None:
        return True
    else:
        row, col = find

    for number in range(1, 10):
        randomNumber = random.randint(1, 9)

        if validCheck(board, randomNumber, (row, col)):
            board[row][col] = randomNumber
            if generateRandomBoard(board):
                return True

            board[row][col] = 0
    return False


def deleteCells(firstBoard,number):
    while number:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if firstBoard[row][col] != 0:
            firstBoard[row][col] = 0
            number = number - 1


def sudokuGenerate(firstBoard, level):
    generateRandomBoard(firstBoard)

    if level == 1:
        deleteCells(firstBoard, 30)
    if level == 2:
        deleteCells(firstBoard, 40)
    if level == 3:
        deleteCells(firstBoard, 50)
