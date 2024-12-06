import pygame 
import subprocess
import sys


pygame.init()

clock = pygame.time.Clock()
FPS = 60

info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

screen = pygame.display.set_mode((1200 , 900), pygame.RESIZABLE)
pygame.display.set_caption("parallex")

scroll = 0
scroll_speed = 1.5

ground_image = pygame.image.load("main_assets/ground.png").convert_alpha()
ground_image = pygame.transform.scale(ground_image, (SCREEN_WIDTH, SCREEN_HEIGHT // 4))
ground_width = ground_image.get_width()
ground_height = ground_image.get_height()
# button_hover_sound = pygame.mixer.Sound("main_assets/tunetank.com_select-option.wav") 
button_click_sound = pygame.mixer.Sound("main_assets/tunetank.com_menu-option-hover.wav") 




def load_music():
    song1 = 'main_assets/vivaldi.mp3'
    pygame.mixer.music.load(song1)
    pygame.mixer.music.play(-1)
    
    
    
class Button:
    def __init__(self, image_path, size=None, hover_scale=1.1):
        self.default_image = pygame.image.load(image_path)
        self.hover_image = pygame.transform.scale(self.default_image, 
                        (int(self.default_image.get_width() * hover_scale), int(self.default_image.get_height() * hover_scale)))
        self.image = self.default_image
        if size:
            self.image = pygame.transform.scale(self.image, size)
            self.hover_image = pygame.transform.scale(self.image, 
                        (int(size[0] * hover_scale), int(size[1] * hover_scale)))
        self.rect = self.image.get_rect()
        self.hovered = False

    def draw(self, screen, mouse_pos, pos):
        self.rect.center = pos 
        if self.rect.collidepoint(mouse_pos):
            # if not self.hovered:
            #     pygame.mixer.Sound.play(button_hover_sound)
            #     self.hovered = True
            screen.blit(self.hover_image, self.rect)
        else:
            self.hovered = False
            screen.blit(self.image, self.rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    
    
load_music()

    
bg_images = []
for i in range (1, 6):
    bg_image = pygame.image.load(f"main_assets/plx-{i}.png").convert_alpha()
    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_images.append(bg_image)
bg_width = bg_images[0].get_width()

def draw_bg():
    for x in range(6):
     speed = 1
     for i in bg_images:    
        screen.blit(i, ((x * bg_width) - scroll * speed, 0))
        speed += 0.2

def draw_ground():
   for x in range(15):
      screen.blit(ground_image, ((x * ground_width) - scroll * 2.2, SCREEN_HEIGHT - ground_height))

def run_pacman_file():
    pygame.mixer.music.stop()  
    pygame.mixer.Sound.play(button_click_sound)
    try:
        subprocess.run(["python3.10", "pacman.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running pacman.py: {e}")
    finally:
        load_music() 
        
def run_bird_file():
    pygame.mixer.music.stop()  
    pygame.mixer.Sound.play(button_click_sound)
    try:
        subprocess.run(["python3.10", "main.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running main.py: {e}")
    finally:
        load_music() 
        
        


run = True
while run:
    clock.tick(FPS)
    clock = pygame.time.Clock()

    screen_width, screen_height = screen.get_size()  
    screen.blit(pygame.transform.scale(ground_image, (screen_width, screen_height)), (0, 0))  
   
    

    mouse_pos = pygame.mouse.get_pos()

   
  
    draw_bg()
    draw_ground()
    menu_font = pygame.font.Font("freesansbold.ttf", 70)
    menu_text = menu_font.render("Birds Within Bird", True, "#ffffff")
    menu_rect = menu_text.get_rect(center=(screen_width // 2, screen_height // 6))
    screen.blit(menu_text, menu_rect)
    bird_button = Button("main_assets/birds3.png", (200, 200))
    pacman_button = Button("main_assets/baaaac.png", (200, 200))    
    exit_button = Button("pacman_Assets/ghost_images/blue.png", (150, 150))
    
    bird_pos = (screen_width // 4, screen_height // 2)
    pacman_pos = (screen_width // 2, screen_height // 2)
    exit_pos = (3 * screen_width // 4, screen_height // 2)

    bird_button.draw(screen, mouse_pos, bird_pos)
    pacman_button.draw(screen, mouse_pos, pacman_pos)
    exit_button.draw(screen, mouse_pos, exit_pos)

    scroll += scroll_speed
    
    if scroll >= bg_width:
        scroll = 0
    
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            run = False     
        if event.type == pygame.MOUSEBUTTONDOWN:
                if pacman_button.is_clicked(mouse_pos):
                    run_pacman_file()
                if bird_button.is_clicked(mouse_pos):
                    run_bird_file()
                elif exit_button.is_clicked(mouse_pos):
                    pygame.quit()
                    sys.exit()
    pygame.display.update()

pygame.quit()        
