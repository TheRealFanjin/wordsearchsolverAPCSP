import PySimpleGUI as Sg


def search_word(grid, word):
    # iterate over all possible starting positions in the grid
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            # check if the current position is the starting letter of the word
            if grid[row][col] == word[0]:
                # check all eight directions for the remaining letters of the word
                for row_vector, col_vector in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                    # calculate the next position in the current direction
                    cur_row, cur_col = row + row_vector, col + col_vector
                    # check if the remaining letters of the word match the grid starting from the current position in the current direction
                    found = True
                    for i in range(1, len(word)):
                        if cur_row < 0 or cur_row >= len(grid) or cur_col < 0 or cur_col >= len(grid[cur_row]) or grid[cur_row][cur_col] != word[i]:
                            found = False
                            break
                        cur_row, cur_col = cur_row + row_vector, cur_col + col_vector
                    if found:
                        # return the coordinates of the first letter and the direction code if the word is found
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
    # return not found if the word was not found in the grid
    return 'Word not found'


# set layout and window for the word search input screen
word_search_input_layout = [[Sg.Text('Enter the word search by pressing enter after each row:')],
                            [Sg.Multiline(size=(50, 20), enable_events=True, font='Courier', no_scrollbar=True, key='-IN-')],
                            [Sg.Submit(disabled=True, bind_return_key=False)]]
word_search_input_window = Sg.Window('Word Search Solver', word_search_input_layout, resizable=True)


# if the user exits during the word search input window, it will not proceed to the second window
stopped = False

# main loop for word search input window
board = []
while True:
    event, values = word_search_input_window.read()

    # if close button is pressed
    if event == Sg.WIN_CLOSED:
        stopped = True
        break

    # if there is change detected in the input box
    if event == '-IN-':
        if not values['-IN-'].replace(' ', '') == '':
            word_search_input_window['Submit'].update(disabled=False)
        else:
            word_search_input_window['Submit'].update(disabled=True)
    if event == 'Submit':

        # add each row to board separately
        board = [row for row in values['-IN-'].lower().replace(' ', '').split('\n')]
        issue = False
        issue_reason = ''

        # check if there's something wrong with the input board
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

            # show popup about what's wrong
            while True:
                formatPopupLayout = [[Sg.Text(issue_reason)],
                                     [Sg.Button('OK')]]
                formatPopup = Sg.Window('Word Search Solver', formatPopupLayout, modal=True)
                fPEvent, fpValues = formatPopup.read()
                if fPEvent == Sg.WIN_CLOSED or fPEvent == 'OK':
                    formatPopup.close()
                    break

            # go to beginning of search input window loop
            continue

        # if there's no issue, move on to word input window
        word_search_input_window.close()
        break


# set up word input window
word_input_window_layout = [[Sg.Text('Enter the word to find:')],
                            [Sg.InputText(enable_events=True, font='Courier', key='-IN-')],
                            [Sg.Submit(disabled=True)]]
word_input_window = Sg.Window('Word Search Solver', word_input_window_layout)


# loop for word input window
while True:

    # if user closed last window, do not show this window and stop program
    if stopped:
        break

    event1, values1 = word_input_window.read()

    if event1 == Sg.WIN_CLOSED:
        word_input_window.close()
        break

    if event1 == '-IN-':
        if not values1['-IN-'].replace(' ', '') == '':
            word_input_window['Submit'].update(disabled=False)
        else:
            word_input_window['Submit'].update(disabled=True)

    if event1 == 'Submit':
        while True:

            # see if the function search_word() returns 3 values
            try:
                # assigns what the function returns as 3 variables
                rowNum, colNum, direction = search_word(board, values1['-IN-'].lower().replace(' ', ''))

                # sets the coordinate of the first digit and direction text depending on what direction code the function returned
                if direction == 0:
                    result_popup_layout = [[Sg.Text(f'({rowNum}, {colNum}) going horizontally left to right')],
                                           [Sg.Button('OK')]]
                elif direction == 1:
                    result_popup_layout = [[Sg.Text(f'({rowNum}, {colNum}) going horizontally right to left')],
                                           [Sg.Button('OK')]]
                elif direction == 2:
                    result_popup_layout = [[Sg.Text(f'({rowNum}, {colNum}) going vertically top to bottom')],
                                           [Sg.Button('OK')]]
                elif direction == 3:
                    result_popup_layout = [[Sg.Text(f'({rowNum}, {colNum}) going vertically bottom to top')],
                                           [Sg.Button('OK')]]
                elif direction == 4:
                    result_popup_layout = [[Sg.Text(f'({rowNum}, {colNum}) going diagonally southeast')],
                                           [Sg.Button('OK')]]
                elif direction == 5:
                    result_popup_layout = [[Sg.Text(f'({rowNum}, {colNum}) going diagonally northwest')],
                                           [Sg.Button('OK')]]
                elif direction == 6:
                    result_popup_layout = [[Sg.Text(f'({rowNum}, {colNum}) going diagonally southwest')],
                                           [Sg.Button('OK')]]
                else:
                    result_popup_layout = [[Sg.Text(f'({rowNum}, {colNum}) going northeast')],
                                           [Sg.Button('OK')]]
            # if it didn't return 3 values, that means the word is not found and sets result_popup_layout as word not found
            except ValueError:
                result_popup_layout = [[Sg.Text('Word not found')],
                                       [Sg.Button('OK')]]

            result_popup = Sg.Window('Word Search Solver', result_popup_layout, modal=True)
            event2, values2 = result_popup.read()

            # close popup if "OK" or the close button is clicked
            if event2 == Sg.WIN_CLOSED or event2 == 'OK':
                result_popup.close()
                break
    word_search_input_window.close()
