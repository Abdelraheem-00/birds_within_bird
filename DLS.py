import pygame
from random import choice, randrange

RES = WIDTH, HEIGHT = 1000, 700
TILE = 100

cols, rows = WIDTH // TILE, HEIGHT // TILE

# pygame.init()
# sc = pygame.Surface(RES)
# clock = pygame.time.Clock()

class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        self.thickness = 4

    def draw(self, sc):
        x, y = self.x * TILE, self.y * TILE
        if self.walls['top']:
            pygame.draw.line(sc, pygame.Color('#070b3d'), (x, y), (x + TILE, y), self.thickness)
        if self.walls['right']:
            pygame.draw.line(sc, pygame.Color('#070b3d'), (x + TILE, y), (x + TILE, y + TILE), self.thickness)
        if self.walls['bottom']:
            pygame.draw.line(sc, pygame.Color('#070b3d'), (x + TILE, y + TILE), (x , y + TILE), self.thickness)
        if self.walls['left']:
            pygame.draw.line(sc, pygame.Color('#070b3d'), (x, y + TILE), (x, y), self.thickness)

    def get_rects(self):
        rects = []
        x, y = self.x * TILE, self.y * TILE
        if self.walls['top']:
            rects.append(pygame.Rect( (x, y), (TILE, self.thickness) ))
        if self.walls['right']:
            rects.append(pygame.Rect( (x + TILE, y), (self.thickness, TILE) ))
        if self.walls['bottom']:
            rects.append(pygame.Rect( (x, y + TILE), (TILE , self.thickness) ))
        if self.walls['left']:
            rects.append(pygame.Rect( (x, y), (self.thickness, TILE) ))
        return rects

    def check_cell(self, x, y):
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return self.grid_cells[find_index(x, y)]

    def check_neighbors(self, grid_cells):
        self.grid_cells = grid_cells
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False
            
def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
        dy = current.y - next.y
        
        if dy == 1:
            current.walls['top'] = False
            next.walls['bottom'] = False
        elif dy == -1:
            current.walls['bottom'] = False
            next.walls['top'] = False
    
def DLS(current_cell, grid_cells, depth_limit):
    stack = [(current_cell, 0)]
    visited = set()
    path = []
    
    while stack:
        current, depth = stack.pop()
        if depth > depth_limit:
            continue
        if current not in visited:
            visited.add(current) 
            path.append(current) 
            
            next_cell = current.check_neighbors(grid_cells)
            if next_cell:
                stack.append((next_cell, depth + 1))
    return path

def generate_maze():
    grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
    current_cell = grid_cells[0]
    depth_limit = 10

    # array = []
    # break_count = 1

    # while break_count != len(grid_cells):
    #     current_cell.visited = True
    #     next_cell = current_cell.check_neighbors(grid_cells)
        
    #     if next_cell:
    #         next_cell.visited = True
    #         break_count += 1
    #         array.append(current_cell)
    #         remove_walls(current_cell, next_cell)
    #         current_cell = next_cell
    #     elif array:
    #         current_cell = array.pop()
    path = DLS(current_cell, grid_cells, depth_limit)   
      
    for i in range(len(path) - 1):
        current_cell = path[i]
        next_cell = path[i + 1]
        remove_walls(current_cell, next_cell) 
           
    return grid_cells 







# grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
# current_cell = grid_cells[0]
# stack=[]
# colors,color=[],40
# break_count = 1

# while True:
#     sc.fill(pygame.Color('#000000'))
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             exit()

#     # [Cell.draw() for Cell in grid_cells]
#     current_cell.visited = True
#     [pygame.draw.rect(sc, colors[i],(cell.x * TILE+5,cell.y*TILE+5,
#                                     TILE -10 , TILE -10),border_radius=12) for i , cell in enumerate(stack)]
#     next_cell = current_cell.check_neighbors(grid_cells)

#     if next_cell:
#         next_cell.visited = True
#         stack.append(current_cell)
#         colors.append((min(color ,255),10,100))
#         color +=1
#         remove_walls(current_cell,next_cell)
#         current_cell = next_cell
#     elif stack:
#         current_cell = stack.pop()

#     # pygame.display.flip()
#     clock.tick(30)