import pygame
from random import choice, randrange
from queue import PriorityQueue

RES = WIDTH, HEIGHT = 1200, 900
TILE = 100
cols, rows = WIDTH // TILE, HEIGHT // TILE

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

def generate_maze():
    grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
    current_cell = grid_cells[0]
    array = []
    break_count = 1

    while break_count != len(grid_cells):
        current_cell.visited = True
        next_cell = current_cell.check_neighbors(grid_cells)
        
        if next_cell:
            next_cell.visited = True
            break_count += 1
            array.append(current_cell)
            remove_walls(current_cell, next_cell)
            current_cell = next_cell
        elif array:
            current_cell = array.pop()
    return grid_cells

def dijkstra(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    distances = { (x, y): float('inf') for x in range(cols) for y in range(rows) }
    distances[start] = 0
    previous = { (x, y): None for x in range(cols) for y in range(rows) }
    pq = PriorityQueue()
    pq.put((0, start))

    while not pq.empty():
        current_distance, current_node = pq.get()

        if current_node == goal:
            path = []
            while current_node:
                path.append(current_node)
                current_node = previous[current_node]
            return path[::-1]

        x, y = current_node
        for neighbor in [(x, y-1), (x+1, y), (x, y+1), (x-1, y)]:
            nx, ny = neighbor
            if 0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] == 0:
                new_distance = current_distance + 1
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current_node
                    pq.put((new_distance, neighbor))

    return None

class Food:
    def __init__(self):
        self.img = pygame.image.load('resources/images/pig_failed.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (TILE - 10, TILE - 10))
        self.rect = self.img.get_rect()
        self.set_pos()

    def set_pos(self):
        self.rect.topleft = randrange(cols) * TILE + 5, randrange(rows) * TILE + 5

    def draw(self):
        game_surface.blit(self.img, self.rect)

def is_collide(x, y):
    tmp_rect = player_rect.move(x, y)
    if tmp_rect.collidelist(walls_collide_list) == -1:
        return False
    return True

def eat_food():
    for food in food_list:
        if player_rect.collidepoint(food.rect.center):
            food.set_pos()
            return True
    return False

def is_game_over():
    global time, score, record, FPS
    if time < 0:
        pygame.time.wait(700)
        player_rect.center = TILE // 2, TILE // 2
        [food.set_pos() for food in food_list]
        set_record(record, score)
        record = get_record()
        time, score, FPS = 60, 0, 60

def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')
            return 0

def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))

FPS = 60
pygame.init()
game_surface = pygame.Surface(RES)
surface = pygame.display.set_mode((WIDTH + 300, HEIGHT))
clock = pygame.time.Clock()

bg_game = pygame.image.load('resources/images/background1.jpg').convert()
bg = pygame.image.load('maze_assets/21191 .jpg').convert()

maze = generate_maze()

player_speed = 5
player_img = pygame.image.load('resources/images/red-bird.png').convert_alpha()
player_img = pygame.transform.scale(player_img, (TILE - 2 * maze[0].thickness, TILE - 2 * maze[0].thickness))
player_rect = player_img.get_rect()
player_rect.center = TILE // 2, TILE // 2
directions = {'a': (-player_speed, 0), 'd': (player_speed, 0), 'w': (0, -player_speed), 's': (0, player_speed)}
keys = {'a': pygame.K_a, 'd': pygame.K_d, 'w': pygame.K_w, 's': pygame.K_s}
direction = (0, 0)

food_list = [Food() for i in range(3)]

walls_collide_list = sum([cell.get_rects() for cell in maze], [])
pygame.time.set_timer(pygame.USEREVENT, 1000)
time = 60
score = 0
record = get_record()

font = pygame.font.SysFont('Impact', 150)
text_font = pygame.font.SysFont('Impact', 80)

keys = {
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT,
    'up': pygame.K_UP,
    'down': pygame.K_DOWN
}

directions = {
    'left': (-player_speed, 0),
    'right': (player_speed, 0),
    'up': (0, -player_speed),
    'down': (0, player_speed)
}

while True:
    surface.blit(bg, (WIDTH, 0))
    surface.blit(game_surface, (0, 0))
    game_surface.blit(bg_game, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.USEREVENT:
            time -= 1

    pressed_key = pygame.key.get_pressed()
    for key, key_value in keys.items():
        if pressed_key[key_value] and not is_collide(*directions[key]):
            direction = directions[key]
            break
    else:
        direction = (0, 0)

    if not is_collide(*direction):
        player_rect.move_ip(direction)

    [cell.draw(game_surface) for cell in maze]

    if eat_food():
        FPS += 10
        score += 1
    is_game_over()

    game_surface.blit(player_img, player_rect)

    [food.draw() for food in food_list]

    surface.blit(text_font.render('TIME', True, pygame.Color('white')), (WIDTH + 70, 30))
    surface.blit(font.render(f'{time}', True, pygame.Color('white')), (WIDTH + 70, 130))

    surface.blit(text_font.render('score:', True, pygame.Color('white')), (WIDTH + 50, 350))
    surface.blit(font.render(f'{score}', True, pygame.Color('white')), (WIDTH + 70, 430))

    surface.blit(text_font.render('record:', True, pygame.Color('white')), (WIDTH + 30, 620))
    surface.blit(font.render(f'{record}', True, pygame.Color('white')), (WIDTH + 70, 700))

    pygame.display.flip()
    clock.tick(FPS)
