import pygame
from sys import exit
from random import randint, choice
import json
# from main_menu import main_menu
pygame.init()

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 900

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Duck Hunter Simulator")

try:
    # loading pictures in try so it wouldn't crash
    duck0_img = pygame.image.load('assets/duck/duck0.png').convert_alpha()
    duck1_img = pygame.image.load('assets/duck/duck1.png').convert_alpha()
    duck2_img = pygame.image.load('assets/duck/duck2.png').convert_alpha()
    duck3_img = pygame.image.load('assets/duck/duck3.png').convert_alpha()

    crosshair_img = pygame.image.load('assets/crosshair.png').convert_alpha()
    background_img = pygame.image.load('assets/background.jpg').convert_alpha()
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    ammo_img = pygame.image.load('assets/ammo.png').convert_alpha()
    ammo_pack_img = pygame.image.load('assets/ammo_pack.png').convert_alpha()

except FileNotFoundError as e:
    print("Couldn't load one or multiple images.")
    print(f"Error message:\n{e}")

    with open("error_log.txt", "w") as file:
        file.write(f"An error occured: {str(e)}")

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
text_font = pygame.font.SysFont('Roboco', 50)

# variables
cursor_img_rect = crosshair_img.get_rect()
pygame.mouse.set_visible(False)

def draw_background():
    # screen.fill(YELLOW)
    screen.blit(background_img, (0, 0))


def draw_score():
    score_text = score_font.render(f"Score:{str(player.score)}", True, BLACK)
    screen.blit(score_text, (10, 50))
    
    ammo_text = score_font.render(f"Ammo:", True, BLACK)
    screen.blit(ammo_text, (10, 100))


def write_text(text, x, y, colour):
    text_to_write = text_font.render(text, True, colour)
    screen.blit(text_to_write, (x, y))


def save_game():
    data = {
        'score': player.score,
        'ammo': player.ammo
    }

    with open("save.json", "w") as file:
        json.dump(data, file)
    print("Game saved")

def load_game():
    try:
        with open("save.json", "r") as file:
            data = json.load(file)

    except FileNotFoundError:
        print("Sorry, couldn't find the save.json")

    player.score = data.get("score")
    player.ammo = data.get("ammo")
    print("Game loaded")

class Duck(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed):
        pygame.sprite.Sprite.__init__(self)
        self.pressed = False
        self.speed = speed
        self.x = x
        self.y = y
        self.image = duck0_img
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.rect.center = (x, y)
        self.direction = direction
        self.animation_frames = (duck0_img, duck1_img, duck2_img, duck3_img)
        self.animation_cooldown = 200
        self.update_time = pygame.time.get_ticks()
        self.animation_index = 0

        if self.direction == 1:
            self.flip = False
        else:
            self.flip = True

    def update(self):
        self.move()
        self.animation()
        self.draw()
        self.hit()


    def animation(self):
        self.image = self.animation_frames[self.animation_index]

        if pygame.time.get_ticks() - self.update_time > self.animation_cooldown:
            self.animation_index += 1
            self.update_time = pygame.time.get_ticks()

        if self.animation_index > 3:
            self.animation_index = 0


    def move(self):
        self.rect.x += (self.speed * self.direction)

        if self.rect.x >= SCREEN_WIDTH - self.width:
            self.direction = -1
            self.flip = True

        if self.rect.x <= 0:
            self.direction = 1
            self.flip = False

    def hit(self):
        self.mouse_pos = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed()[0] == 1 and not self.pressed and player.ammo > 0:
            self.pressed = True
            if self.rect.collidepoint(self.mouse_pos):
                self.kill()
                player.score += 1
                self.spawn()
                # print("HIT")
            else:
                # print("MISSED")
                player.ammo -= 1


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
        self.ammo_counter()


    def ammo_counter(self):
        for i in range(self.ammo):
            screen.blit(ammo_img, (170+15*i, 110))

        if player.ammo <= 0:
            write_text("OUT OF AMMO!", 10, 150, RED)



    def spawn_ammo(self):
        spawn_x = randint(30, 800)
        spawn_y = randint(400, 700)
        ammo_box = Ammo(spawn_x, spawn_y)
        ammo_group.add(ammo_box)

    def draw(self):
        x = self.position[0]
        if x <= 300:
            x = 300
        elif x >= 700:
            x = 700
        y = 700
        pygame.draw.line(screen, BLACK, (500, 900), (x, y), 10)


class Ammo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = ammo_pack_img
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

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_s:
                confirm_input = input("Do you want to save the game? [y/N] ")
                if confirm_input.lower() == "y":
                    save_game() 
                else:
                    print("Save aborted")

            if event.key == pygame.K_l:
                confirm_input = input("Do you want to load the game? [y/N] ")
                if confirm_input.lower() == "y":
                    load_game() 
                else:
                    print("Load aborted")

    pygame.display.update()


pygame.quit()