import pygame
import sys
# import os
import subprocess

pygame.init()

screen = pygame.display.set_mode((1200, 900), pygame.RESIZABLE)
pygame.display.set_caption("Birds within Bird")

background_image = pygame.image.load("main_assets/mmm.jpg") 
button_hover_sound = pygame.mixer.Sound("main_assets/tunetank.com_select-option.wav") 
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
            if not self.hovered:
                pygame.mixer.Sound.play(button_hover_sound)
                self.hovered = True
            screen.blit(self.hover_image, self.rect)
        else:
            self.hovered = False
            screen.blit(self.image, self.rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# def run_pacman_file():
#     pygame.mixer.Sound.play(button_click_sound)
#     os.system("python3.10 pacman.py")

# def run_bird_file():
#     pygame.mixer.Sound.play(button_click_sound)
#     os.system("python3.10 main.py")
load_music()


def run_pacman_file():
    pygame.mixer.Sound.play(button_click_sound)
    try:
        subprocess.run(["python3.10", "pacman.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running pacman.py: {e}")

def run_bird_file():
    pygame.mixer.Sound.play(button_click_sound)
    try:
        subprocess.run(["python3.10", "main.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running main.py: {e}")
        
def main_menu():
    clock = pygame.time.Clock()

    bird_button = Button("main_assets/birds3.png", (200, 200))
    pacman_button = Button("main_assets/baaaac.png", (200, 200))
    exit_button = Button("pacman_Assets/ghost_images/blue.png", (150, 150))

    while True:
        screen_width, screen_height = screen.get_size()  
        screen.blit(pygame.transform.scale(background_image, (screen_width, screen_height)), (0, 0))  

        # Menu text
        menu_font = pygame.font.Font("freesansbold.ttf", 70)
        menu_text = menu_font.render("Birds within Bird", True, "#ffffff")
        menu_rect = menu_text.get_rect(center=(screen_width // 2, screen_height // 6))
        screen.blit(menu_text, menu_rect)

        mouse_pos = pygame.mouse.get_pos()

        bird_pos = (screen_width // 4, screen_height // 2)
        pacman_pos = (screen_width // 2, screen_height // 2)
        exit_pos = (3 * screen_width // 4, screen_height // 2)

        bird_button.draw(screen, mouse_pos, bird_pos)
        pacman_button.draw(screen, mouse_pos, pacman_pos)
        exit_button.draw(screen, mouse_pos, exit_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pacman_button.is_clicked(mouse_pos):
                    run_pacman_file()
                if bird_button.is_clicked(mouse_pos):
                    run_bird_file()
                elif exit_button.is_clicked(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)

main_menu()
