import pygame
import sys
pygame.init()

WIDTH, HEIGHT = 500, 500
BALL_RADIUS = 25
BALL_COLOR = (255, 0, 0)  # Red color
BACKGROUND_COLOR = (255, 255, 255)  # White color
MOVE_DISTANCE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Prikol'niy ball")

ball_x = WIDTH // 2
ball_y = HEIGHT // 2

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_UP]:
        if ball_y - BALL_RADIUS - MOVE_DISTANCE >= 0:
            ball_y -= MOVE_DISTANCE
    if keys[pygame.K_DOWN]:
        if ball_y + BALL_RADIUS + MOVE_DISTANCE <= HEIGHT:
            ball_y += MOVE_DISTANCE
    if keys[pygame.K_LEFT]:
        if ball_x - BALL_RADIUS - MOVE_DISTANCE >= 0: 
            ball_x -= MOVE_DISTANCE
    if keys[pygame.K_RIGHT]:
        if ball_x + BALL_RADIUS + MOVE_DISTANCE <= WIDTH: 
            ball_x += MOVE_DISTANCE

    screen.fill(BACKGROUND_COLOR)

    pygame.draw.circle(screen, BALL_COLOR, (ball_x, ball_y), BALL_RADIUS)

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()