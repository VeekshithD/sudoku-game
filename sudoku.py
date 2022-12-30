from tkinter import *


def find_empty(sudoku):
    for i in range(len(sudoku)):
        for j in range(len(sudoku[0])):
            if sudoku[i][j] == 0:
                return i, j

    return None


def valid(sudoku, num, pos):
    for i in range(9):
        if sudoku[pos[0]][i] == num and pos[1] != i:
            return False

    for i in range(9):
        if sudoku[i][pos[1]] == num and pos[0] != i:
            return False

    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if sudoku[i][j] == num and (i, j) != pos:
                return False

    return True


def solve(sudoku):
    find = find_empty(sudoku)
    if not find:
        return True
    else:
        row, column = find

    for i in range(1, 10):
        if valid(sudoku, i, (row, column)):
            sudoku[row][column] = i

            if solve(sudoku):
                return True

            sudoku[row][column] = 0

    return False


def validate_number(P):
    out = (P.isdigit() or P == "") and len(P) < 2
    return out


def draw3x3grid(row, column, bgcolor):
    for i in range(3):
        for j in range(3):
            e = Entry(main_window, width=5, bg=bgcolor, justify="center", validate="key", validatecommand=(reg, "%P"))
            e.grid(row=row+i+1, column=column+j+1, sticky="nsew", padx=1, pady=1, ipady=5)
            cells[(row+i+1, column+j+1)] = e


def draw9x9grid():
    color = "#D0ffff"
    for rowNo in range(1, 10, 3):
        for colNo in range(0, 9, 3):
            draw3x3grid(rowNo, colNo, color)
            if color == "#D0ffff":
                color = "#ffffd0"
            else:
                color = "#D0ffff"


def clear_values():
    errLabel.configure(text="")
    solvedLabel.configure(text="")
    for row in range(2, 11):
        for col in range(1, 10):
            cell = cells[(row, col)]
            cell.delete(0, "end")


def get_values():
    board = []
    errLabel.configure(text="")
    solvedLabel.configure(text="")
    for row in range(2, 11):
        rows = []
        for col in range(1, 10):
            val = cells[(row, col)].get()
            if val.strip() == "":
                rows.append(0)
            else:
                cells[(row, col)].configure(fg="red")
                rows.append(int(val))

        board.append(rows)

    global sol
    sol = solve(board)
    update_values(board)


def update_values(board):
    if sol:
        for rows in range(2, 11):
            for col in range(1, 10):
                cells[(rows, col)].delete(0, "end")
                cells[(rows, col)].insert(0, board[rows-2][col-1])

        solvedLabel.configure(text="Sudoku Successfully Solved", font=("arial", 13))
    else:
        errLabel.configure(text="No solution exists for this Sudoku", font=("arial", 13))


main_window = Tk()
main_window.title("Sudoku Solver")
main_window.geometry("324x500")
main_window.resizable(width=False, height=False)
main_window.configure(background="light blue")

label = Label(main_window, text="Fill in the numbers and click solve", background="light blue", font=("arial", 13))
label.grid(row=0, column=1, columnspan=10)

errLabel = Label(main_window, text="", fg="red", background="light blue")
errLabel.grid(row=15, column=1, columnspan=10, pady=5)

solvedLabel = Label(main_window, text="", fg="green", background="light blue")
solvedLabel.grid(row=15, column=1, columnspan=10, pady=5)

cells = {}

reg = main_window.register(validate_number)
sol = False

btn = Button(main_window, command=get_values, text="Solve", width=12, bg="black", fg="white", font=("arial", 13))
btn.grid(row=20, column=1, columnspan=5, pady=20)

btn = Button(main_window, command=clear_values, text="Clear", width=12, bg="black", fg="white", font=("arial", 13))
btn.grid(row=20, column=5, columnspan=5, pady=20)

draw9x9grid()
main_window.mainloop()