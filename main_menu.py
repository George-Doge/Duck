import pygame
from sys import exit
pygame.init()
# Right now the main menu is in WIP and can't be found in the game


SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 900

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Duck Hunter Simulator Main Menu")

# images
try:

    bg_image = pygame.image.load('assets/background.jpg').convert_alpha()
    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    play_button_image = pygame.image.load('assets/buttons/play_button.png').convert_alpha()
    quit_button_image = pygame.image.load('assets/buttons/quit_button.png').convert_alpha()
    controls_button_image = pygame.image.load('assets/buttons/controls_button.png').convert_alpha()
    test_button_img = pygame.image.load('assets/buttons/test_button.png').convert_alpha()

    back_img = pygame.image.load('assets/buttons/back_button.png').convert_alpha()

except FileNotFoundError as e:
    print("Couldn't load one or multiple images.")
    print(f"Error message:\n{e}")

    with open("error_log.txt", "w") as file:
        file.write(f"An error occured: {str(e)}")

    exit(1)

# variables
text_font = pygame.font.SysFont('Roboco', 50)
text_font_small = pygame.font.SysFont('Roboco', 35)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

class Button():
    def __init__(self,image, x, y, size):
        self.image = pygame.transform.scale(image, ( int(image.get_width()*size), int(image.get_height()*size) ))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.pressed = False


    def action(self):
        pressed = self.click()
        self.draw()

        return pressed

    def click(self):
        mouse_position = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()[0]
        
        if self.rect.collidepoint(mouse_position) and self.pressed == False and mouse_press == 1:
            self.pressed = True
            return True

        if mouse_press == 0:
            self.pressed = False


    def draw(self):
        screen.blit(self.image, self.rect)


def write_text(text, x, y, colour, font_write):
    text_to_write = font_write.render(text, True, colour)
    screen.blit(text_to_write, (x, y))

class main_menu():
    def __init__(self):
        self.menu_state = 1
        self.playButton = Button(play_button_image, 550, 300, 0.5)
        self.quitButton = Button(quit_button_image, 550, 600, 0.5)
        self.testButton = Button(test_button_img, 550, 600, 0.3)
        self.backButton = Button(back_img, 40, 40, 0.3)
        self.controlsButton = Button(controls_button_image, 550, 450, 0.5)

    def menu_scene(self):
        pygame.mouse.set_visible(True)

        if self.playButton.action() and self.menu_state == 1:
            self.menu_state = 0

        if self.quitButton.action() and self.menu_state == 1:
            self.menu_state = 2

        if self.controlsButton.action() and self.menu_state == 1:
            self.menu_state = 3


    def back_button_func(self):
        if self.backButton.action():
            self.menu_state = 1

    def controls_scene(self):
        screen.blit(bg_image, (0, 0))
        write_text("CONTROLS", 400, 200, BLACK, text_font)
        write_text("Mouse - aiming", 400, 300, BLACK, text_font)
        write_text("Left mouse button - shooting", 400, 350, BLACK, text_font)
        write_text("ESC - quits game", 400, 400, BLACK, text_font)
        write_text("L - loading / S - saving", 400,450, BLACK, text_font)
        write_text("There are more types of ducks", 400, 500, BLACK, text_font)
        write_text("NOTE - run this game from terminal, because loading and saving won't work", 50, 600, BLACK, text_font_small)
        self.back_button_func()


    def credits_scene(self):
        screen.blit(bg_image, (0, 0))
        write_text("TEST CREDITS SCENE", 200, 200, RED)
        self.back_button_func()