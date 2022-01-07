import pygame
import os
from pygame import draw
pygame.font.init()
pygame.mixer.init()



WIDTH, HEIGHT = 900, 500

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game?")


WHITE = (255, 255, 255)
BLACK = (255, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLETS_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assetss', "Grenade+1.mp3"))
BULLETS_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assetss', "Gun+Silencer.mp3"))


HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VEL = 5
BULLETS_VEL = 7
MAX_BULLETS = 5


SPACESHIP_WIDTH, SPACESHIP_HIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

red_health = 10
yellow_health = 10


YELLOW_SPACESHIP_img = pygame.image.load(os.path.join('Assetss', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_img, (SPACESHIP_WIDTH, SPACESHIP_HIGHT)), 90)

RED_SPACESHIP_img = pygame.image.load(os.path.join('Assetss', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_img, (SPACESHIP_WIDTH, SPACESHIP_HIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assetss', 'space.png')), (WIDTH, HEIGHT))


def draw_window(red, yellow, red_buls, yellow_buls, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render(f"Health: {str(red_health)}" , 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(f"Health: {str(yellow_health)}" , 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_buls:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_buls:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # Left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: # Right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0 : # Up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 13: # Down
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: # Left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: # Right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0 : # Up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 13: # Down
        red.y += VEL

def handle_bullets(yellow_buls, red_buls, yellow, red):
    for bullet in yellow_buls:
        bullet.x += BULLETS_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_buls.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_buls.remove(bullet)
    for bullet in red_buls:
        bullet.x -= BULLETS_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_buls.remove(bullet)
        elif bullet.x < 0:
            red_buls.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(1000*5)

def mainn():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HIGHT)

    YEL_bullets = []
    RED_bullets = []

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h and len(YEL_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    YEL_bullets.append(bullet)
                    BULLETS_FIRE_SOUND.play()

                if event.key == pygame.K_KP_ENTER and len(RED_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    RED_bullets.append(bullet)
                    BULLETS_FIRE_SOUND.play()

            global red_health, yellow_health
            if event.type == RED_HIT:
                red_health -= 1
                BULLETS_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLETS_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break
    

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(YEL_bullets, RED_bullets, yellow, red)

        draw_window(red, yellow, RED_bullets, YEL_bullets, red_health, yellow_health)
def main_menu():
    title_font = pygame.font.SysFont("comicsans", 25)
    run = True
    while run:
        WIN.blit(SPACE, (0,0))
        title_label = title_font.render("Press on the mouse to start!...", 1, (0,255,0))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 250))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mainn()
    pygame.quit()

main_menu()