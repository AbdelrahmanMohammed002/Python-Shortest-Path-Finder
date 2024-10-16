import curses
from curses import wrapper
import queue
import time

# Define the maze layout
maze = [
    ["#", "O", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]

def print_maze(maze, stdscr, path=[]):
    """
    Prints the maze on the screen with the path highlighted.
    
    Args:
        maze (list): The maze layout.
        stdscr (curses window): The window where the maze will be displayed.
        path (list): The list of positions in the current path to highlight.
    """
    BLUE = curses.color_pair(1)
    RED = curses.color_pair(2)
    
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j*2, "X", RED)  # Highlight the path in red
            else:
                stdscr.addstr(i, j*2, value, BLUE)  # Draw the maze in blue

def find_start(maze, start):
    """
    Finds the starting position in the maze.
    
    Args:
        maze (list): The maze layout.
        start (str): The character representing the start point.

    Returns:
        tuple: Coordinates of the start point or None if not found.
    """
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i, j
    return None

def find_neighbors(maze, row, col):
    """
    Finds the valid neighbors for the given position in the maze.
    
    Args:
        maze (list): The maze layout.
        row (int): Current row.
        col (int): Current column.
        
    Returns:
        list: List of neighboring coordinates.
    """
    neighbors = []
    if row > 0:  # Check the top neighbor
        neighbors.append((row - 1, col))
    if row + 1 < len(maze):  # Check the bottom neighbor
        neighbors.append((row + 1, col))
    if col > 0:  # Check the left neighbor
        neighbors.append((row, col - 1))
    if col + 1 < len(maze[0]):  # Check the right neighbor
        neighbors.append((row, col + 1))

    return neighbors

def find_path(maze, stdscr):
    """
    Performs a breadth-first search (BFS) to find the path from start to end in the maze.
    
    Args:
        maze (list): The maze layout.
        stdscr (curses window): The window where the maze will be displayed.
    
    Returns:
        list: The path from the start to the end if found, or an empty list otherwise.
    """
    start = 'O'
    end = 'X'
    start_position = find_start(maze, start)

    if start_position is None:
        return []

    q = queue.Queue()
    q.put((start_position, [start_position]))

    visited_nodes = set()

    while not q.empty():
        current_position, path = q.get()
        row, col = current_position

        stdscr.clear()
        print_maze(maze, stdscr, path)
        stdscr.refresh()
        time.sleep(0.2)

        if maze[row][col] == end:
            return path

        neighbors = find_neighbors(maze, row, col)
        for neighbor in neighbors:
            if neighbor in visited_nodes:
                continue

            r, c = neighbor
            if maze[r][c] == '#':
                continue

            new_path = path + [neighbor]
            q.put((neighbor, new_path))
            visited_nodes.add(neighbor)

    return []  # Return empty path if no solution is found

def main(stdscr):
    """
    Main function to initialize the curses window and solve the maze.
    
    Args:
        stdscr (curses window): The window where the maze and path will be displayed.
    """
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)  # Maze color
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)   # Path color

    find_path(maze, stdscr)
    stdscr.getch()  # Wait for a key press before exiting

# Call the main function with the curses wrapper
wrapper(main)
