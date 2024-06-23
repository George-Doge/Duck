import pygame

# Right now the main menu is in WIP and can't be found in the game


SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 900

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Duck Hunter Simulator Main Menu")

# variables
text_font = pygame.font.SysFont('Roboco', 50)

def write_text(text, x, y, colour):
    text_to_write = text_font.render(text, True, colour)
    screen.blit(text_to_write, (x, y))

class main_menu:
    def __init__(self):
        self.menu_state = 0
        self.clicked = False

    def menu_scene(self):
        pass

    def credits_scene(self):
        pass