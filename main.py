import PySimpleGUI as Sg

#test
def search_word(grid, word):
    # Iterate over all possible starting positions in the grid
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            # Check if the current position is the starting letter of the word
            if grid[row][col] == word[0]:
                # Check all eight directions for the remaining letters of the word
                for row_vector, col_vector in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                    # Calculate the next position in the current direction
                    cur_row, cur_col = row + row_vector, col + col_vector
                    # Check if the remaining letters of the word match the grid
                    # starting from the current position in the current direction
                    found = True
                    for i in range(1, len(word)):
                        if cur_row < 0 or cur_row >= len(grid) or cur_col < 0 or cur_col >= len(grid[cur_row]) or grid[cur_row][cur_col] != word[i]:
                            found = False
                            break
                        cur_row, cur_col = cur_row + row_vector, cur_col + col_vector
                    if found:
                        # Return the coordinates of the first letter and the direction
                        # if the word was found in the grid
                        if (row_vector, col_vector) == (0, 1):
                            return row + 1, col + 1, 0
                        elif (row_vector, col_vector) == (0, -1):
                            return row + 1, col + 1, 1
                        elif (row_vector, col_vector) == (1, 0):
                            return row + 1, col + 1, 2
                        elif (row_vector, col_vector) == (-1, 0):
                            return row + 1, col + 1, 3
                        elif (row_vector, col_vector) == (1, 1):
                            return row + 1, col + 1, 4
                        elif (row_vector, col_vector) == (-1, -1):
                            return row + 1, col + 1, 5
                        elif (row_vector, col_vector) == (1, -1):
                            return row + 1, col + 1, 6
                        elif (row_vector, col_vector) == (-1, 1):
                            return row + 1, col + 1, 7
    # Return None if the word was not found in the grid
    return 'Word not found'


word_search_input_layout = [[Sg.Text('Enter the word search by pressing enter after each row:')],
                            [Sg.Multiline(size=(50, 20), enable_events=True, font='Courier', no_scrollbar=True, key='-IN-')],
                            [Sg.Submit(disabled=True, bind_return_key=False)]]
word_search_input_window = Sg.Window('Word Search Solver', word_search_input_layout, resizable=True)


stopped = False
board = []
while True:
    event, values = word_search_input_window.read()
    if event == Sg.WIN_CLOSED:
        stopped = True
        break
    if event == '-IN-':
        if not values['-IN-'].replace(' ', '') == '':
            word_search_input_window['Submit'].update(disabled=False)
        else:
            word_search_input_window['Submit'].update(disabled=True)
    if event == 'Submit':
        board = [row.lower().replace(' ', '') for row in values['-IN-'].strip().split('\n')]
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
            continue
        word_search_input_window.close()
        break


inputLayout1 = [[Sg.Text('Enter the word to find:')],
                [Sg.InputText(enable_events=True, font='Courier', key='-WI-')],
                [Sg.Submit(disabled=True)]]
window1 = Sg.Window('Word Search Solver', inputLayout1)


while True:
    if stopped:
        break
    event1, values1 = window1.read()
    if event1 == Sg.WIN_CLOSED:
        window1.close()
        break
    if event1 == '-WI-':
        if not values1['-WI-'].replace(' ', '') == '':
            window1['Submit'].update(disabled=False)
        else:
            window1['Submit'].update(disabled=True)
    if event1 == 'Submit':
        while True:
            try:
                rowNum, colNum, direction = search_word(board, values1['-WI-'].lower().replace(' ', ''))
                if direction == 0:
                    inputLayout2 = [[Sg.Text(f'({rowNum}, {colNum}) going horizontally left to right')],
                                    [Sg.Button('OK')]]
                elif direction == 1:
                    inputLayout2 = [[Sg.Text(f'({rowNum}, {colNum}) going horizontally right to left')],
                                    [Sg.Button('OK')]]
                elif direction == 2:
                    inputLayout2 = [[Sg.Text(f'({rowNum}, {colNum}) going vertically top to bottom')],
                                    [Sg.Button('OK')]]
                elif direction == 3:
                    inputLayout2 = [[Sg.Text(f'({rowNum}, {colNum}) going vertically bottom to top')],
                                    [Sg.Button('OK')]]
                elif direction == 4:
                    inputLayout2 = [[Sg.Text(f'({rowNum}, {colNum}) going diagonally southeast')],
                                    [Sg.Button('OK')]]
                elif direction == 5:
                    inputLayout2 = [[Sg.Text(f'({rowNum}, {colNum}) going diagonally northwest')],
                                    [Sg.Button('OK')]]
                elif direction == 6:
                    inputLayout2 = [[Sg.Text(f'({rowNum}, {colNum}) going diagonally southwest')],
                                    [Sg.Button('OK')]]
                else:
                    inputLayout2 = [[Sg.Text(f'({rowNum}, {colNum}) going northeast')],
                                    [Sg.Button('OK')]]
            except ValueError:
                inputLayout2 = [[Sg.Text('Word not found')],
                                [Sg.Button('OK')]]
            window2 = Sg.Window('Word Search Solver', inputLayout2, modal=True)
            event2, values2 = window2.read()
            if event2 == Sg.WIN_CLOSED or event2 == 'OK':
                window2.close()
                break
    word_search_input_window.close()
