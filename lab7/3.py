import pygame
import sys
pygame.init()

WIDTH, HEIGHT = 500, 500
SQUARE_SIZE = 50  
SQUARE_COLOR = (255, 255, 138)  
BACKGROUND_COLOR = (255, 255, 255)  
MOVE_DISTANCE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Prikol'niy square")

square_x = WIDTH // 2
square_y = HEIGHT // 2

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_UP]:
        if square_y - MOVE_DISTANCE >= 0:
            square_y -= MOVE_DISTANCE
    if keys[pygame.K_DOWN]:
        if square_y + SQUARE_SIZE + MOVE_DISTANCE <= HEIGHT:
            square_y += MOVE_DISTANCE
    if keys[pygame.K_LEFT]:
        if square_x - MOVE_DISTANCE >= 0: 
            square_x -= MOVE_DISTANCE
    if keys[pygame.K_RIGHT]:
        if square_x + SQUARE_SIZE + MOVE_DISTANCE <= WIDTH: 
            square_x += MOVE_DISTANCE

    screen.fill(BACKGROUND_COLOR)

    pygame.draw.rect(screen, SQUARE_COLOR, (square_x, square_y, SQUARE_SIZE, SQUARE_SIZE))

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()