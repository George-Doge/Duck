import pygame
from sys import exit
from random import randint, choice
pygame.init()

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 900

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Duck Hunter Simulator")

try:
    # loading pictures in try so it wouldn't crash
    duck_img = pygame.image.load('assets/duck.png').convert_alpha()
    crosshair_img = pygame.image.load('assets/crosshair.png').convert_alpha()
    background_img = pygame.image.load('assets/background.jpg').convert_alpha()
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    ammo_img = pygame.image.load('assets/ammo.png').convert_alpha()

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
    # screen.fill(YELLOW)
    screen.blit(background_img, (0, 0))


def draw_score():
    score_text = score_font.render(f"Score:{str(player.score)}", True, BLACK)
    screen.blit(score_text, (10, 50))
    
    ammo_text = score_font.render(f"Ammo:{str(player.ammo)}", True, BLACK)
    screen.blit(ammo_text, (10, 100))

class Duck(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed):
        pygame.sprite.Sprite.__init__(self)
        self.pressed = False
        self.speed = speed
        self.x = x
        self.y = y
        self.image = duck_img
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.rect.center = (x, y)
        self.direction = direction

        if self.direction == 1:
            self.flip = False
        else:
            self.flip = True

    def update(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.move()
        self.draw()
        self.hit()

    def move(self):
        self.rect.x += (self.speed * self.direction)

        if self.rect.x >= SCREEN_WIDTH - self.width:
            self.direction = -1
            self.flip = True

        if self.rect.x <= 0:
            self.direction = 1
            self.flip = False

    def hit(self):
        if self.rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0] == 1 and not self.pressed and player.ammo > 0:
            self.pressed = True
            player.score += 1
            player.ammo -= 1
            self.spawn()
            self.kill()

        elif pygame.mouse.get_pressed()[0] == 1 and not self.pressed and player.ammo > 0:
            self.pressed = True
            # player.ammo -= 1

        if pygame.mouse.get_pressed()[0] == 0:
            self.pressed = False

    def spawn(self):
        spawn_x = randint(30, 800)
        spawn_y = randint(50, 500)
        spawn_direction = choice([-1, 1])
        ducky = Duck(spawn_x, spawn_y, spawn_direction, 5)
        duck_group.add(ducky)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class Hunter:
    def __init__(self):
        self.position = pygame.mouse.get_pos()
        self.score = 0
        self.ammo = 7

    def update(self):
        self.position = pygame.mouse.get_pos()
        self.draw()

    def spawn_ammo(self):
        spawn_x = randint(30, 800)
        spawn_y = randint(400, 700)
        ammo_box = Ammo(spawn_x, spawn_y)
        ammo_group.add(ammo_box)

    def draw(self):
        x, y = self.position
        y = 700
        pygame.draw.line(screen, BLACK, (500, 900), (x, y), 10)


class Ammo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = ammo_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.add_ammo = 4
        self.pressed = False

    def update(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.draw()
        self.collect()


    def collect(self):
        if self.rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0] == 1 and not self.pressed:
            self.kill()
            player.ammo += self.add_ammo
            self.pressed = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.pressed = False


    def draw(self):
        screen.blit(self.image, self.rect)

run = True

# declare instances
duck_group = pygame.sprite.Group()
ammo_group = pygame.sprite.Group()

ducky = Duck(500, 200, 1, 5)
duck_group.add(ducky)
player = Hunter()

while run:
    clock.tick(FPS)
    
    draw_background()

    duck_group.update()
    player.update()
    ammo_group.update()

    draw_score()
    
    ammo_spawn_chance = randint(1, 1000)

    if ammo_spawn_chance == 3 and len(ammo_group) < 2:
        player.spawn_ammo()


    cursor_img_rect.center = pygame.mouse.get_pos()
    screen.blit(crosshair_img, cursor_img_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    pygame.display.update()


pygame.quit()