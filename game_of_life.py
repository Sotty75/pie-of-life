import sys
import time
import random

ROWS = 20
COLS = 20
ALIVE = 'X'
DEAD = '.'

CURSOR_HOME = "\033[H"       # Moves cursor to line 1, column 1
CLEAR_SCREEN = "\033[2J"     # Clears the entire visible screen
HIDE_CURSOR  = "\033[?25l"   # Hides the blinking cursor
SHOW_CURSOR  = "\033[?25h"   # Restores the blinking cursor

def cell_to_x(x):
    if x >= COLS: x = x % COLS
    if x < 0 : 
        x = (-x) % COLS
        x = COLS - x
    return x

def cell_to_y(y):
    if y >= ROWS: y = y % ROWS
    if y < 0 : 
        y = (-y) % ROWS
        y = ROWS - y
    return y

def set_cell(grid,x,y,state):
    grid[cell_to_x(x)][cell_to_y(y)] = state
    return

def get_cell(grid,x,y):
    return grid[cell_to_x(x)][cell_to_y(y)]

def init_grid(grid,state):
    for y in range(ROWS):
        for x in range(COLS):
            set_cell(grid,x,y, state)

def play_loop(old,new):
    while True:
        compute_new_state(old, new)
        time.sleep(0.5)
        clear_terminal()
        for y in range(ROWS):
            for x in range(COLS):
                print(old[x][y], end="")
            print()

def clear_terminal() -> None:
    # Clear once and hide cursor
    sys.stdout.write(CLEAR_SCREEN + HIDE_CURSOR)
    sys.stdout.write(CURSOR_HOME)
    sys.stdout.flush()

def count_living_neighbors(grid, x, y) -> int:
    alive = 0
    for dy in range(-1,2):
        for dx in range(-1,2):
            if dx == 0 and dy == 0: 
                continue
            if get_cell(grid,x + dx,y + dy) == ALIVE:
                alive+=1
    return alive

def update_grid(old,new) -> None:
    for y in range(ROWS):
        for x in range(COLS):
            old[x][y]=new[x][y]
    return
    
def compute_new_state(old, new) -> None:
    for y in range(ROWS):
        for x in range(COLS):
            n_alive = count_living_neighbors(old,x,y)
            new_state = DEAD
            if get_cell(old,x,y) == ALIVE:
                new_state = ALIVE if n_alive == 2 or n_alive == 3 else DEAD
            else:
                if n_alive == 3:
                    new_state = ALIVE
            set_cell(new,x,y,new_state)
    update_grid(old,new)            
    return

def random_setup(grid) -> None:
    for y in range(ROWS):
        for x in range(COLS):
            num = random.randint(0, 1)
            if num == 0: set_cell(grid,x,y,DEAD)
            if num == 1: set_cell(grid,x,y,ALIVE)
    return
    

def main():
    old_grid = [[0]*COLS for _ in range(ROWS)]
    new_grid = [[0]*COLS for _ in range(ROWS)]
    init_grid(old_grid,DEAD)
    set_cell(old_grid,10,10,ALIVE)
    set_cell(old_grid,10,11,ALIVE)
    set_cell(old_grid,10,12,ALIVE)
    random_setup(old_grid) 
    play_loop(old_grid,new_grid)
    return

if __name__ == "__main__":
    main()
