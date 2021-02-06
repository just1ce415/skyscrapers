"""
Main module
GitHub: https://github.com/just1ce415/skyscrapers
"""

def read_input(path: str):
    """
    Read game board file from path.
    Return list of str.

    >>> read_input("tests/check.txt")
    ['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***']
    """
    board_lst = []
    with open(path, 'r', encoding='utf-8') as f_board:
        for line in f_board:
            if line.find('\n') != -1:
                board_lst.append(line[:-1])
            else:
                board_lst.append(line)
    return board_lst


def left_to_right_check(input_line: str, pivot: int):
    """
    Check row-wise visibility from left to right.
    Return True if number of building from the left-most hint is visible looking to the right,
    False otherwise.

    input_line - representing board row.
    pivot - number on the left-most hint of the input_line.

    >>> left_to_right_check("412453*", 4)
    True
    >>> left_to_right_check("452453*", 5)
    False
    """
    highest = 0
    visible_builds = 0
    for i in range(1, len(input_line) - 1):
        current_height = int(input_line[i])
        if current_height > highest:
            highest = current_height
            visible_builds += 1
    if visible_builds == pivot:
        return True
    return False


def check_not_finished_board(board: list):
    """
    Check if skyscraper board is not finished, i.e., '?' present on the game board.

    Return True if finished, False otherwise.

    >>> check_not_finished_board(['***21**', '4?????*', '4?????*', '*?????5', '*?????*', '*?????*', '*2*1***'])
    False
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*5?3215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    for line in board:
        if line.find('?') != -1:
            return False
    return True


def check_uniqueness_in_rows(board: list):
    """
    Check buildings of unique height in each row.

    Return True if buildings in a row have unique height, False otherwise.

    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_uniqueness_in_rows(['***21**', '452453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*553215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    height_range = len(board[0]) - 2
    for line in board:
        # THROW OUT FIRST AND LAST LINE
        if line in (board[0], board[-1]):
            continue
        # CHECKING UNIQUENESS VIA SET
        non_stars = line.replace('*', '')
        unique_set = set(non_stars)
        if len(unique_set) != len(non_stars):
            return False
    return True


def check_horizontal_visibility(board: list):
    """
    Check row-wise visibility (left-right and vice versa)

    Return True if all horizontal hints are satisfiable,
    i.e., for line 412453* , hint is 4, and 1245 are the four buildings
    that could be observed from the hint looking to the right.

    >>> check_horizontal_visibility(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_horizontal_visibility(['***21**', '452453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_horizontal_visibility(['***21**', '452413*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    for line in board:
        # THROW OUT UNNECESSARY CASE
        if line[0] == '*' and line[-1] == '*':
            continue
        # REVERSING LINE
        reversed_line = ''
        for i in range(len(line) - 1, -1, -1):
            reversed_line += line[i]
        # CHECK
        if line[0] == '*':
            if not left_to_right_check(reversed_line, int(reversed_line[0])):
                return False
        elif line[-1] == '*':
            if not left_to_right_check(line, int(line[0])):
                return False
        else:
            if (not left_to_right_check(reversed_line, int(reversed_line[0])) and
                not left_to_right_check(line, int(line[0]))):
                return False
    return True


def check_columns(board: list):
    """
    Check column-wise compliance of the board for uniqueness (buildings of unique height) and visibility (top-bottom and vice versa).

    Same as for horizontal cases, but aggregated in one function for vertical case, i.e. columns.

    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41232*', '*2*1***'])
    False
    >>> check_columns(['***21**', '412553*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    # CREATING REVERSED BOARD
    reversed_board = []
    for i in range(len(board)):
        lined_colomn = []
        for j in range(len(board[0])):
            lined_colomn.append(board[j][i])
        reversed_board.append(''.join(lined_colomn))
    # CHECKING FOR DOUBLES
    if not check_uniqueness_in_rows(reversed_board):
        return False
    # CHECKING FOR LINES
    if not check_horizontal_visibility(reversed_board):
        return False
    return True


def check_skyscrapers(input_path: str):
    """
    Main function to check the status of skyscraper game board.
    Return True if the board status is compliant with the rules,
    False otherwise.

    >>> check_skyscrapers("tests/check.txt")
    True
    """
    board = read_input(input_path)
    if (check_not_finished_board(board) and check_uniqueness_in_rows(board)
        and check_horizontal_visibility(board) and check_columns(board)):
        return True
    return False


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
    #print(check_skyscrapers("tests/check.txt"))
