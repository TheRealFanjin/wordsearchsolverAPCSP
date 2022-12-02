import PySimpleGUI as sg


def solve():
    # init variables
    vertical_length = len(board)
    horizontal_length = len(board[0])

    # initialize vertical board
    verticalBoard = []
    for i in range(0, horizontal_length):
        verticalBoard.append('')
    for row in board:
        row_count = 0
        for columnNum in range(0, horizontal_length):
            verticalBoard[row_count] += row[columnNum]
            row_count += 1

    # init down and left
    downLeftDiagonalBoard = []
    for index in range(horizontal_length + vertical_length - 1):
        downLeftDiagonalBoard.append('')
    for i in range(horizontal_length):
        x = 0
        y = i
        while True:
            try:
                downLeftDiagonalBoard[i] += board[x][::-1][y]
                x += 1
                y += 1
            except IndexError:
                while len(downLeftDiagonalBoard[i]) != vertical_length:
                    downLeftDiagonalBoard[i] += '0'
                break
    for i in range(1, len(verticalBoard[0])):
        x = 0
        y = i
        while True:
            try:
                downLeftDiagonalBoard[i + horizontal_length - 1] += verticalBoard[::-1][x][y]
                x += 1
                y += 1
            except IndexError:
                break
    # init down and right
    downRightDiagonalBoard = []
    for index in range(horizontal_length + vertical_length - 1):
        downRightDiagonalBoard.append('')
    for i in range(horizontal_length):
        x = 0
        y = i
        while True:
            try:
                downRightDiagonalBoard[i] += board[x][y]
                x += 1
                y += 1
            except IndexError:
                while len(downRightDiagonalBoard[i]) != vertical_length:
                    downRightDiagonalBoard[i] += '0'
                break
    for i in range(1, len(verticalBoard[0])):
        x = 0
        y = i
        while True:
            try:
                downRightDiagonalBoard[i + horizontal_length - 1] += verticalBoard[x][y]
                x += 1
                y += 1
            except IndexError:
                while len(downRightDiagonalBoard[i + horizontal_length - 1]) != vertical_length:
                    downRightDiagonalBoard[i + horizontal_length - 1] += '0'
                break

    # horizontal, left to right
    row_count = 1
    for row in board:
        if word in row:
            return f'({row_count}, {row.index(word) + 1})'
        row_count += 1

    # horizontal, right to left
    row_count = 1
    for row in board:
        if word in row[::-1]:
            return f'({row_count}, {len(row)-(row[::-1].index(word))})'
        row_count += 1

    # vertical, top to down
    row_count = 1
    for row in verticalBoard:
        if word in row:
            return f'({row.index(word) + 1}, {row_count})'
        row_count += 1

    # vertical, bottom to top
    row_count = 1
    for row in verticalBoard:
        if word in row[::-1]:
            return f'({len(row)-(row[::-1].index(word))}, {row_count})'
        row_count += 1

    # down right diagonal, left to right
    row_count = 1
    for row in downRightDiagonalBoard:
        if word in row:
            if row_count > horizontal_length:
                return f'({row.index(word) + 1}, {row_count - horizontal_length + (row.index(word))})'
            else:
                return f'({row.index(word) + 1}, {row_count + (row.index(word))})'
        row_count += 1
    # down right diagonal, right to left
    row_count = 1
    for row in downRightDiagonalBoard:
        if word in row[::-1]:
            if row_count > horizontal_length:
                return f'({vertical_length - row[::-1].index(word)}, {(row_count - horizontal_length) + (vertical_length - row[::-1].index(word))})'

            else:
                return f'({vertical_length - row[::-1].index(word)}, {(row_count - 1) + len(word)})'
        row_count += 1

    # down left diagonal, right to left
    row_count = 1
    for row in downLeftDiagonalBoard:
        if word in row:
            if row_count > horizontal_length:
                return f'({row_count - horizontal_length + 1}, {horizontal_length - (row.index(word))})'
            else:
                return f'({row.index(word) + 1}, {(horizontal_length - row_count + 1) + (row.index(word))})'
        row_count += 1

    # down left diagonal, left to right
    row_count = 1
    for row in downLeftDiagonalBoard:
        if word in row[::-1]:
            if row_count > horizontal_length:
                return f'({vertical_length - row[::-1].index(word)}, {(horizontal_length - (row_count - horizontal_length) + 1) - (len(word) - 1)})'
            else:
                return f'({vertical_length - row[::-1].index(word)}, {(horizontal_length - row_count + 1) - (len(word) - 1)})'
        row_count += 1


while True:
    inputLayout = [[sg.Text('Enter the word search:')],
                   [sg.InputText()],
                   [sg.Submit()]]
    window = sg.Window('Word Search Solver', inputLayout)
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'Submit':
        board = values[0].split(' ')
        window.close()
        break

while True:
    inputLayout1 = [[sg.Text('Enter the word to find:')],
                    [sg.InputText()],
                    [sg.Button('Search')]]
    window1 = sg.Window('Word Search Solver', inputLayout1)
    event1, values1 = window1.read()
    if event1 == sg.WIN_CLOSED:
        window1.close()
        break
    if event1 == 'Search':
        word = values1[0]
        while True:
            inputLayout2 = [[sg.Text(solve())],
                            [sg.Button('OK')]]
            window2 = sg.Window('Word Search Solver', inputLayout2, modal=True)
            event2, values2 = window2.read()
            if event2 == sg.WIN_CLOSED or event2 == 'OK':
                window2.close()
                break
    window.close()
