import pygame
import os

pygame.font.init()

# Constants
HEIGHT = 600
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
FPS = 60
SHIP_WIDTH, SHIP_HEIGHT = 60, 40
BULLET_VEL = 10
VELOCITY = 5
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)
MAX_BULLETS = 3
RED_HIT = pygame.USEREVENT + 1
YELLOW_HIT = pygame.USEREVENT + 2

# Initialize Pygame and Mixer
pygame.init()
pygame.mixer.init()

# Load and transform images
YELLOW_SPACESHIP = pygame.image.load('E:/Programming/PYTHON/game/space tanks/objects/spaceship_yellow.png')
YELLOW_SPACESHIP = pygame.transform.scale(YELLOW_SPACESHIP, (SHIP_WIDTH, SHIP_HEIGHT))
YELLOW_SPACESHIP = pygame.transform.rotate(YELLOW_SPACESHIP, 90)

RED_SPACESHIP = pygame.image.load('E:/Programming/PYTHON/game/space tanks/objects/spaceship_red.png')
RED_SPACESHIP = pygame.transform.scale(RED_SPACESHIP, (SHIP_WIDTH, SHIP_HEIGHT))
RED_SPACESHIP = pygame.transform.rotate(RED_SPACESHIP, 270)

SPACE = pygame.transform.scale(pygame.image.load('E:/Programming/PYTHON/game/space tanks/objects/space.png'), (WIDTH, HEIGHT))

# Load sound effects
SHOT_SOUND = pygame.mixer.Sound('E:/Programming/PYTHON/game/space tanks/objects/Grenade.mp3')

# Initialize font for scoreboard
SCORE_FONT = pygame.font.Font(None, 36)

def draw(red, yellow, red_bullets, yellow_bullets, red_score, yellow_score, red_health, yellow_health, winner_text):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    # Draw scores
    red_score_text = SCORE_FONT.render(f"Red: {red_score}", 1, WHITE)
    yellow_score_text = SCORE_FONT.render(f"Yellow: {yellow_score}", 1, WHITE)
    WIN.blit(red_score_text, (WIDTH - red_score_text.get_width() - 10, 10))
    WIN.blit(yellow_score_text, (10, 10))

    # Draw health
    red_health_text = SCORE_FONT.render(f"Health: {red_health}", 1, WHITE)
    yellow_health_text = SCORE_FONT.render(f"Health: {yellow_health}", 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 30))
    WIN.blit(yellow_health_text, (10, 30))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    # Display winner text if any
    if winner_text:
        winner_text_render = SCORE_FONT.render(winner_text, 1, WHITE)
        WIN.blit(winner_text_render, (WIDTH // 2 - winner_text_render.get_width() // 2, HEIGHT // 2))

    pygame.display.update()

def RedMovement(keyPress, red):
    if keyPress[pygame.K_LEFT] and red.x - VELOCITY > BORDER.x + BORDER.width:
        red.x -= VELOCITY
    if keyPress[pygame.K_RIGHT] and red.x + VELOCITY + red.width < WIDTH:
        red.x += VELOCITY
    if keyPress[pygame.K_UP] and red.y - VELOCITY > 0:
        red.y -= VELOCITY
    if keyPress[pygame.K_DOWN] and red.y + VELOCITY + red.height < HEIGHT:
        red.y += VELOCITY

def YellowMovement(keyPress, yellow):
    if keyPress[pygame.K_a] and yellow.x - VELOCITY > 0:
        yellow.x -= VELOCITY
    if keyPress[pygame.K_d] and yellow.x + VELOCITY + yellow.width < BORDER.x:
        yellow.x += VELOCITY
    if keyPress[pygame.K_w] and yellow.y - VELOCITY > 0:
        yellow.y -= VELOCITY
    if keyPress[pygame.K_s] and yellow.y + VELOCITY + yellow.height < HEIGHT - 6:
        yellow.y += VELOCITY

def handleBullets(yellow_bullets, red_bullets, red, yellow, red_score, yellow_score):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
            red_score += 1
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
            yellow_score += 1
        elif bullet.x < 0:
            red_bullets.remove(bullet)

    return red_score, yellow_score

def main():
    red = pygame.Rect(700, 300, SHIP_WIDTH, SHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SHIP_WIDTH, SHIP_HEIGHT)
    red_bullets = []
    yellow_bullets = []
    red_health = 10
    yellow_health = 10
    clock = pygame.time.Clock()
    red_score = 0
    yellow_score = 0
    pygame.display.set_caption("Space Tanks")
    run = True
    winner_text = ""

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    SHOT_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    SHOT_SOUND.play()
            if event.type == RED_HIT:
                red_health -= 1
            if event.type == YELLOW_HIT:
                yellow_health -= 1

        # Check for win conditions
        if red_health <= 0:
            winner_text = "YELLOW WINS!"
        if yellow_health <= 0:
            winner_text = "RED WINS!"

        keyPress = pygame.key.get_pressed()
        YellowMovement(keyPress, yellow)
        RedMovement(keyPress, red)
        red_score, yellow_score = handleBullets(yellow_bullets, red_bullets, red, yellow, red_score, yellow_score)

        draw(red, yellow, red_bullets, yellow_bullets, red_score, yellow_score, red_health, yellow_health, winner_text)

        if winner_text:
            pygame.time.delay(3000)  # Pause for a moment to display winner
            run = False  # Exit game loop after showing winner

    pygame.quit()

if __name__ == "__main__":
    main()
