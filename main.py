from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Word Search Solver")


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


app = QApplication([])
window = MainWindow()
window.show()
app.exec()

