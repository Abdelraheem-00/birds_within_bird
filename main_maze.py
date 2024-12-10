from maze import *

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
