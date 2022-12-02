import PySimpleGUI as Sg


def solve():
    # init variables
    vertical_length = len(board)
    horizontal_length = len(board[0])

    # initialize vertical board
    vertical_board = []
    for i in range(0, horizontal_length):
        vertical_board.append('')
    for row in board:
        row_count = 0
        for columnNum in range(0, horizontal_length):
            vertical_board[row_count] += row[columnNum]
            row_count += 1

    # init down and left
    south_east_diagonal = []
    for index in range(horizontal_length + vertical_length - 1):
        south_east_diagonal.append('')
    for i in range(horizontal_length):
        x = 0
        y = i
        while True:
            try:
                south_east_diagonal[i] += board[x][::-1][y]
                x += 1
                y += 1
            except IndexError:
                while len(south_east_diagonal[i]) != vertical_length:
                    south_east_diagonal[i] += '0'
                break
    for i in range(1, len(vertical_board[0])):
        x = 0
        y = i
        while True:
            try:
                south_east_diagonal[i + horizontal_length - 1] += vertical_board[::-1][x][y]
                x += 1
                y += 1
            except IndexError:
                break
    # init down and right
    south_west_diagonal = []
    for index in range(horizontal_length + vertical_length - 1):
        south_west_diagonal.append('')
    for i in range(horizontal_length):
        x = 0
        y = i
        while True:
            try:
                south_west_diagonal[i] += board[x][y]
                x += 1
                y += 1
            except IndexError:
                while len(south_west_diagonal[i]) != vertical_length:
                    south_west_diagonal[i] += '0'
                break
    for i in range(1, len(vertical_board[0])):
        x = 0
        y = i
        while True:
            try:
                south_west_diagonal[i + horizontal_length - 1] += vertical_board[x][y]
                x += 1
                y += 1
            except IndexError:
                while len(south_west_diagonal[i + horizontal_length - 1]) != vertical_length:
                    south_west_diagonal[i + horizontal_length - 1] += '0'
                break

    # horizontal, left to right
    row_count = 1
    for row in board:
        if word in row:
            return row_count, row.inputLine(word) + 1, 0
        row_count += 1

    # horizontal, right to left
    row_count = 1
    for row in board:
        if word in row[::-1]:
            return row_count, len(row) - (row[::-1].inputLine(word)), 1
        row_count += 1

    # vertical, top to down
    row_count = 1
    for row in vertical_board:
        if word in row:
            return row.index(word) + 1, row_count, 2
        row_count += 1

    # vertical, bottom to top
    row_count = 1
    for row in vertical_board:
        if word in row[::-1]:
            return len(row)-(row[::-1].index(word)), row_count, 3
        row_count += 1

    # down right diagonal, left to right
    row_count = 1
    for row in south_west_diagonal:
        if word in row:
            if row_count > horizontal_length:
                return row.index(word) + 1, row_count - horizontal_length + row.index(word), 4
            else:
                return row.index(word) + 1, row_count + (row.index(word)), 4
        row_count += 1
    # down right diagonal, right to left
    row_count = 1
    for row in south_west_diagonal:
        if word in row[::-1]:
            if row_count > horizontal_length:
                return vertical_length - row[::-1].index(word), \
                       (row_count - horizontal_length) + (vertical_length - row[::-1].index(word)), \
                       5

            else:
                return vertical_length - row[::-1].index(word), (row_count - 1) + len(word), 5
        row_count += 1

    # down left diagonal, right to left
    row_count = 1
    for row in south_east_diagonal:
        if word in row:
            if row_count > horizontal_length:
                return row_count - horizontal_length + 1, horizontal_length - (row.index(word)), 6
            else:
                return row.index(word) + 1, (horizontal_length - row_count + 1) + (row.index(word)), 6
        row_count += 1

    # down left diagonal, left to right
    row_count = 1
    for row in south_east_diagonal:
        if word in row[::-1]:
            if row_count > horizontal_length:
                return vertical_length - row[::-1].index(word), \
                       (horizontal_length - (row_count - horizontal_length) + 1) - (len(word) - 1), \
                       7
            else:
                return vertical_length - row[::-1].index(word), (horizontal_length - row_count + 1) - (len(word) - 1), 7
        row_count += 1
    return 'Word not found'


stopped = False
while True:
    inputLayout = [[Sg.Text('Enter the word search:')],
                   [Sg.InputText()],
                   [Sg.Submit()]]
    window = Sg.Window('Word Search Solver', inputLayout)
    event, values = window.read()
    if event == Sg.WIN_CLOSED:
        stopped = True
        break
    if event == 'Submit':
        board = values[0].split(' ')
        issue = False
        issue_reason = ''
        for inputLine in range(0, len(board)):
            if not board[inputLine].isalpha():
                issue = True
                issue_reason = 'The word search must only contain alphabetic characters!'
            if inputLine == len(board) - 1:
                break
            if len(board[inputLine]) != len(board[inputLine + 1]):
                issue = True
                issue_reason = 'Lines must be the same length!'
        if issue:
            while True:
                formatPopupLayout = [[Sg.Text(issue_reason)],
                                     [Sg.Button('OK')]]
                formatPopup = Sg.Window('Word Search Solver', formatPopupLayout, modal=True)
                fPEvent, fpValues = formatPopup.read()
                if fPEvent == Sg.WIN_CLOSED or fPEvent == 'OK':
                    formatPopup.close()
                    break
            window.close()
            continue
        window.close()
        break


while True:
    if stopped:
        break
    inputLayout1 = [[Sg.Text('Enter the word to find:')],
                    [Sg.InputText()],
                    [Sg.Submit()]]
    window1 = Sg.Window('Word Search Solver', inputLayout1)
    event1, values1 = window1.read()
    if event1 == Sg.WIN_CLOSED:
        window1.close()
        break
    if event1 == 'Submit':
        word = values1[0]
        while True:
            try:
                rowNum, col, direction = solve()
                if direction == 0:
                    inputLayout2 = [[Sg.Text(f'({rowNum}, {col}) going horizontally left to right')],
                                    [Sg.Button('OK')]]
                elif direction == 1:
                    inputLayout2 = [[Sg.Text(f'({rowNum}, {col}) going horizontally right to left')],
                                    [Sg.Button('OK')]]
                elif direction == 2:
                    inputLayout2 = [[Sg.Text(f'({rowNum}, {col}) going vertically top to bottom')],
                                    [Sg.Button('OK')]]
                elif direction == 3:
                    inputLayout2 = [[Sg.Text(f'({rowNum}, {col}) going vertically bottom to top')],
                                    [Sg.Button('OK')]]
                elif direction == 4:
                    inputLayout2 = [[Sg.Text(f'({rowNum}, {col}) going diagonally southeast')],
                                    [Sg.Button('OK')]]
                elif direction == 5:
                    inputLayout2 = [[Sg.Text(f'({rowNum}, {col}) going diagonally northwest')],
                                    [Sg.Button('OK')]]
                elif direction == 6:
                    inputLayout2 = [[Sg.Text(f'({rowNum}, {col}) going diagonally southwest')],
                                    [Sg.Button('OK')]]
                else:
                    inputLayout2 = [[Sg.Text(f'({rowNum}, {col}) going northeast')],
                                    [Sg.Button('OK')]]
            except ValueError:
                inputLayout2 = [[Sg.Text('Word not found')],
                                [Sg.Button('OK')]]
            window2 = Sg.Window('Word Search Solver', inputLayout2, modal=True)
            event2, values2 = window2.read()
            if event2 == Sg.WIN_CLOSED or event2 == 'OK':
                window2.close()
                window1.close()
                break
    window.close()
