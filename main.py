import pygame
import os
import math
pygame.font.init()
pygame.mixer.init()


# https://www.youtube.com/watch?v=jO6qQDNa2UY - Finished
# WINDOW

WIDTH, HEIGHT = 900, 500 # Width and Height
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # Creating window with Width and Height
pygame.display.set_caption("Space Game") # Settings title/caption
FPS = 60 # Frames Per Second
SPLITBORDER = pygame.Rect(WIDTH//2, 0, 10, HEIGHT) # Border
BGM = pygame.mixer.music.load('Assets/BG.wav') # Background Music
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.1)

# COLOURS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# BULLETS

MAX_BULLETS = 40

# EVENTS

RED_HIT = pygame.USEREVENT  +1
YELLOW_HIT = pygame.USEREVENT + 2

# FONTS

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# ASSETS

#| Sounds

#BULLET_HIT_SOUND = pygame.mixer.Sound('HIT.ogg')
#BULLET_FIRE_SOUND = pygame.mixer.Sound('GUN_FIRE.ogg')

# | audio having problems, couldn't find the problem even after diagnosing and following pygame docs

#| Scale
SS_WIDTH, SS_HEIGHT = 55,40 # Spaceship Height and Width

#| Velocity
VEL = 5 # Spaceship Velocity
BULLET_VEL = 7 # Bullet Velocity

#| Images

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT)) # Background

#| Ships

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png')) # Yellow Ship

YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SS_WIDTH, SS_HEIGHT)), 90) # Yellow Ship Rotation and Scale

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png')) # Red Ship

RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SS_WIDTH, SS_HEIGHT)), 270) # Red Ship Rotation and Scale

# WINDOW DATA

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0)) # Draw Background onto surface
    pygame.draw.rect(WIN, BLACK, SPLITBORDER) # Draw on WIN, BLACK coloured SPLITBORDER

    red_health_text = HEALTH_FONT.render("Health: "  + str(red_health), 1, WHITE) # Health Text
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE) # Health Text
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10)) # Draw Health text to surface
    WIN.blit(yellow_health_text, (10, 10)) # Draw Health text to surface

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y)) # Draw Player to Surface
    WIN.blit(RED_SPACESHIP, (red.x, red.y)) # Draw Player to Surface

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet) # Draw Bullet

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet) # Draw Bullet


    pygame.display.update()


# MOVEMENT

def yellow_movementhandler(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < SPLITBORDER.x:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.width < HEIGHT - 10:  # DOWN
        yellow.y += VEL

def red_movementhandler(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > SPLITBORDER.x + SPLITBORDER.width:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.width < HEIGHT - 10:  # DOWN
        red.y += VEL

def bullet_handler(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet): # If collides with bullet, remove bullet and do Event
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove((bullet))
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet) # Remove Bullet if off screen

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet): #  If collides with bullet, remove bullet and do Event
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove((bullet))
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet) # Remove Bullet if off screen


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE) # Variable with font data
    WIN.blit(draw_text, (
        WIDTH/2 - draw_text.get_width()/2,
        HEIGHT/2 - draw_text.get_height()/2
    )) # Drawing it
    pygame.display.update()
    pygame.time.delay(5000) # Delay 5 secs before restarting

def main():


    red = pygame.Rect(700, 300, SS_WIDTH, SS_HEIGHT) # Starting Positions
    yellow = pygame.Rect(100, 300, SS_WIDTH, SS_HEIGHT) # Starting Positions

    red_bullets = [] # List for handling bullets
    yellow_bullets = [] # List for handling bullets

    red_health = 10 # Health
    yellow_health = 10 # Health

    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get(): # 'Pressing the X icon while running' Management
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN: # Activating once on KEYDOWN
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS: # Checks for KEY and Ammo
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet) # Adds Bullet to list
                    #wBULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS: # Checks for KEY and Ammo
                    bullet = pygame.Rect(
                        red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet) # Adds Bullet to list
                    #BULLET_FIRE_SOUND.play()
            if event.type == RED_HIT: # On hit
                red_health -= 1 # Remove 1 from Red Spaceship's Health
                #BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT: # On hit
                yellow_health -= 1 # Remove 1 from Yellow Spaceship's Health
                #BULLET_HIT_SOUND.play()

        winner_text = "" # Winner Text String
        if red_health <= 0: # If red's health is 0
            winner_text = "Yellow Wins!" #
        if yellow_health <= 0: # If yellow's health is 0
            winner_text = "Red Wins!" # Edits Str, notifying the IF statement below

        if winner_text != "": # if text is not Blank then
            draw_winner(winner_text) # Draw winner text, wait for delay to finish:
            break # Runs the Main() line outside of the loop, restarting the game

        keys_pressed = pygame.key.get_pressed() # Key Management for Movement
        yellow_movementhandler(keys_pressed, yellow) # Yellow Movement
        red_movementhandler(keys_pressed, red) # Red Movement
        bullet_handler(yellow_bullets, red_bullets, yellow, red) # Bullet Handler handling

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health) # Drawing all the stuff

    main()


if __name__ == "__main__":
    main()