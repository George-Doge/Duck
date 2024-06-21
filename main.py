import pygame
from sys import exit
pygame.init()

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 900

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Duck Hunter Simulator")

try:
    # loading pictures in try so it wouldn't crash
    duck_img = pygame.image.load('assets/duck.png').convert_alpha()
    crosshair_img = pygame.image.load('assets/crosshair.png').convert_alpha()

except FileNotFoundError as e:
    print("Couldn't load one or multiple images.")
    print(f"Error message:\n{e}")

    exit(1)

# framerate
clock = pygame.time.Clock()
FPS = 60

# Colours and fonts
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (211, 174, 54)
score_font = pygame.font.SysFont('Arial', 50)

# variables
cursor_img_rect = crosshair_img.get_rect()
pygame.mouse.set_visible(False)

def draw_background():
    screen.fill(YELLOW)


def draw_score():
    score_text = score_font.render(f"Score:{str(player.score)}", True, BLACK)
    screen.blit(score_text, (10, 50))

class Duck(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.flip = False
        self.pressed = False
        self.speed = speed
        self.x = x
        self.y = y
        self.image = duck_img
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.rect.center = (x, y)
        self.direction = 1

    def update(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.move()
        self.draw()
        self.hit()

    def move(self):
        self.rect.x += (self.speed * self.direction)

        if self.rect.x == SCREEN_WIDTH - self.width:
            self.direction = -1
            self.flip = True

        if self.rect.x == 0:
            self.direction = 1
            self.flip = False

    def hit(self):
        if self.rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0] == 1 and not self.pressed:
            self.pressed = True
            player.score += 1

        if pygame.mouse.get_pressed()[0] == 0:
            self.pressed = False

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class Hunter:
    def __init__(self):
        self.position = pygame.mouse.get_pos()
        self.score = 0

    def update(self):
        self.position = pygame.mouse.get_pos()
        self.draw()

    def draw(self):
        x, y = self.position
        y = 700
        pygame.draw.line(screen, BLACK, (500, 900), (x, y), 10)

run = True

# declare instances
ducky = Duck(500, 200, 5)
player = Hunter()

while run:
    clock.tick(FPS)
    
    draw_background()


    ducky.update()
    player.update()

    draw_score()
    
    cursor_img_rect.center = pygame.mouse.get_pos()
    screen.blit(crosshair_img, cursor_img_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    pygame.display.update()


pygame.quit()