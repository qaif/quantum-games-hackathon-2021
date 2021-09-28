import pygame
import sys
pygame.init()
screen = pygame.display.set_mode((576, 1024))  # the resolution of the canvas
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # image of player 1
    # background image
    pygame.display.update()
    clock.tick(120)
