import pygame
import os

pygame.init()

WIDTH, HEIGHT = 500, 300
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Player")

music_files = [file for file in os.listdir() if file.endswith(('.mp3'))]
current_track_index = 0

def play_music():
    if music_files:
        pygame.mixer.music.load(music_files[current_track_index])
        pygame.mixer.music.play()

def stop_music():
    pygame.mixer.music.stop()

def next_track():
    global current_track_index
    current_track_index = (current_track_index + 1) % len(music_files)
    play_music()

def previous_track():
    global current_track_index
    current_track_index = (current_track_index - 1) % len(music_files)
    play_music()

running = True
play_music()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if pygame.mixer.music.get_busy():
                stop_music()
            else:
                play_music()
        if keys[pygame.K_RIGHT]:
            next_track()
        if keys[pygame.K_LEFT]:
            previous_track()

    screen.fill((200, 200, 200))

    if music_files:
        font = pygame.font.Font(None, 36)
        text = font.render(f"Playing: {music_files[current_track_index]}", True, (0, 0, 0))
        screen.blit(text, (20, HEIGHT // 2))

    pygame.display.flip()
    pygame.time.Clock().tick(FPS)

pygame.quit()