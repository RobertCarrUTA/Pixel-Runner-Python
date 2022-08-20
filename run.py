# This code could be heavily commented because it is for me to learn, so I will take notes

import pygame
from sys import exit # Secure way to end the program

# pygame.init() - starts pygame and initiates all the sub parts of pygame
pygame.init()
screen = pygame.display.set_mode((800, 400)) # width of 800 pixels, height of 400 pixels

while True:
    # We need to check for all the possible types of player input
    for event in pygame.event.get():
        # When a user clicks the X on the window to close it
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    

    pygame.display.update()