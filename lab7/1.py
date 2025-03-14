import pygame
import time
import math

pygame.init()

WIDTH, HEIGHT = 400, 400
CENTER = (WIDTH // 2, HEIGHT // 2)
FPS = 60

clock_image = pygame.image.load('mickeyclock.jpeg')
clock_image = pygame.transform.scale(clock_image, (WIDTH, HEIGHT))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")

def draw_clock(minute_angle, second_angle):
    screen.blit(clock_image, (0, 0))  
    minute_hand_length = 60  
    minute_x = CENTER[0] + minute_hand_length * math.cos(math.radians(minute_angle))
    minute_y = CENTER[1] + minute_hand_length * math.sin(math.radians(minute_angle))
    second_hand_length = 90  
    second_x = CENTER[0] + second_hand_length * math.cos(math.radians(second_angle))
    second_y = CENTER[1] + second_hand_length * math.sin(math.radians(second_angle))

    pygame.draw.line(screen, (128, 255, 0), CENTER, (minute_x, minute_y), 6)  # Right hand (minutes)
    pygame.draw.line(screen, (255, 0, 0), CENTER, (second_x, second_y), 3)  # Left hand (seconds)

    pygame.display.flip() 

def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        current_time = time.localtime()
        minutes = current_time.tm_min
        seconds = current_time.tm_sec

        minute_angle = (minutes + seconds / 60) * 6  
        second_angle = seconds * 6  

        draw_clock(minute_angle, second_angle)

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()