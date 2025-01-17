import pygame
from random import randrange, choice


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




class Food:
    def __init__(self, pos):
        self.img = pygame.image.load('resources/images/pig_failed.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (TILE - 10, TILE - 10))
        self.rect = self.img.get_rect()
        self.rect.topleft = pos  

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
            food_list.remove(food)  
            return True
    return False

def is_game_over():
    global score, record
    if score <= 0:
        pygame.time.wait(700)
        player_rect.center = TILE // 2, TILE // 2
        score = 0

def check_win():
    global score
    if score == 160:  # إذا وصلت النقاط إلى 140 أو أكثر
        win_message = text_font.render("You Win!", True, pygame.Color('green'))  # إنشاء رسالة الفوز
        game_surface.blit(win_message, (RES[0] // 2 - 150, RES[1] // 2 - 50))  # رسم الرسالة في منتصف شاشة اللعبة
        surface.blit(game_surface, (0, 0))  # تحديث السطح الرئيسي
        pygame.display.flip()  # تحديث الشاشة لعرض الرسالة
        pygame.time.wait(3000)  # انتظار لمدة 3 ثوانٍ
        pygame.quit()  # إغلاق Pygame
        exit()  # إنهاء البرنامجج

# A* search algorithm with wall collision check
def astar(start, goal):
    open_list = [start]
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_list:
        current = min(open_list, key=lambda x: f_score.get(x, float('inf')))
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1] 

        open_list.remove(current)
        for neighbor in get_neighbors(current):
            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                if neighbor not in open_list:
                    open_list.append(neighbor)

    return []   

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(cell):
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
    for dx, dy in directions:
        neighbor = (cell[0] + dx, cell[1] + dy)
        if 0 <= neighbor[0] < cols and 0 <= neighbor[1] < rows:
            # Check if the neighbor is a free space (no collision)
            if not is_collide(neighbor[0] * TILE, neighbor[1] * TILE):  
                neighbors.append(neighbor)
    return neighbors


def draw_path(path):
    if path: 
        for i in range(len(path) - 1):
            start_pos = (path[i][0] * TILE + TILE // 2, path[i][1] * TILE + TILE // 2)
            end_pos = (path[i + 1][0] * TILE + TILE // 2, path[i + 1][1] * TILE + TILE // 2)
            pygame.draw.line(game_surface, pygame.Color('green'), start_pos, end_pos, 6)  # Draw path line

FPS = 60
pygame.init()
game_surface = pygame.Surface(RES)
surface = pygame.display.set_mode((WIDTH + 300, HEIGHT))


bg_game = pygame.image.load('resources/images/background2.jpg').convert()
bg_game = pygame.transform.scale(bg_game, RES)  # Scale the background to fit the game screen
bg = pygame.image.load('maze_assets/21191 .jpg').convert()

maze = generate_maze()

player_speed = 4
player_img = pygame.image.load('resources/images/red-bird.png').convert_alpha()
player_img = pygame.transform.scale(player_img, (TILE - 2 * maze[0].thickness, TILE - 2 * maze[0].thickness))
player_rect = player_img.get_rect()
player_rect.topleft = (200, 200)  # Set the fixed position here

food_list = [Food((100,100)) ,Food((200, 200)), Food((300, 300)), Food((400, 400)), Food((500, 500)), Food((600, 600)), Food((700, 700)), Food((800, 800)), Food((900, 900)), Food((1000, 1000))]  


walls_collide_list = sum([cell.get_rects() for cell in maze], [])

score = 0

font = pygame.font.SysFont('Impact', 150)
text_font = pygame.font.SysFont('Impact', 80)

keys = {
    pygame.K_LEFT: (-player_speed, 0),
    pygame.K_RIGHT: (player_speed, 0),
    pygame.K_UP: (0, -player_speed),
    pygame.K_DOWN: (0, player_speed)
}

while True:
    surface.blit(bg, (WIDTH, 0))
    surface.blit(game_surface, (0, 0))
    game_surface.blit(bg_game, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    # Player controls and movement
    pressed_keys = pygame.key.get_pressed()
    direction = (0, 0)
    for key in keys:
        if pressed_keys[key]:
            direction = keys[key]
            break

    if not is_collide(*direction):
        player_rect.move_ip(direction)

    [cell.draw(game_surface) for cell in maze]

    if eat_food():
        score += 20

    is_game_over()
    check_win()
    game_surface.blit(player_img, player_rect)

    [food.draw() for food in food_list]

    if food_list:
        player_pos = (player_rect.centerx // TILE, player_rect.centery // TILE)
        food_pos = (food_list[0].rect.centerx // TILE, food_list[0].rect.centery // TILE)
        path = astar(player_pos, food_pos)
        draw_path(path)

    surface.blit(text_font.render('score:', True, pygame.Color('white')), (WIDTH + 50, 350))
    surface.blit(font.render(f'{score}', True, pygame.Color('white')), (WIDTH + 70, 430))

    pygame.display.flip()
   