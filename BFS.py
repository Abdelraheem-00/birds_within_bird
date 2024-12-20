
import numpy as np
from collections import deque

maze = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
])

start = (1, 1)
end = (9, 13)

directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def is_valid(maze, pos):
    x, y = pos
    return 0 <= x < maze.shape[0] and 0 <= y < maze.shape[1] and maze[x, y] == 0

def bfs(maze, start, end):
    queue = deque([start])
    visited = set()
    parent = {}
    
    while queue:
        current = queue.popleft()
        if current == end:
            break
        for direction in directions:
            next_pos = (current[0] + direction[0], current[1] + direction[1])
            if is_valid(maze, next_pos) and next_pos not in visited:
                queue.append(next_pos)
                visited.add(next_pos)
                parent[next_pos] = current
    
    path = []
    step = end
    while step != start:
        path.append(step)
        step = parent.get(step, start)
    path.append(start)
    path.reverse()
    return path

def display_maze(maze, player_pos, path):
    display = maze.copy()
    for pos in path:
        x, y = pos
        display[x, y] = 3 
    x, y = player_pos
    display[x, y] = 2 
    for row in display:
        print(''.join(['#' if cell == 1 else ' ' if cell == 0 else 'P' if cell == 2 else '.' for cell in row]))

player_pos = start
path = bfs(maze, start, end)
path_index = 0

while player_pos != end:
    display_maze(maze, player_pos, path)
    move = input("Move (Up/Down/Left/Right): ")
    if move in ["Up", "Down", "Left", "Right"]:
        new_pos = (player_pos[0] + directions[["Up", "Down", "Left", "Right"].index(move)][0],
                   player_pos[1] + directions[["Up", "Down", "Left", "Right"].index(move)][1])
        if is_valid(maze, new_pos):
            player_pos = new_pos
            path_index += 1

print("Congratulations! You reached the end.")
