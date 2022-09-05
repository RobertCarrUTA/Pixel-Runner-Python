# This code could be heavily commented because it is for me to learn, so I will take notes

import pygame
from sys import exit # Secure way to end the program

# pygame.init() - starts pygame and initiates all the sub parts of pygame
pygame.init()
screen = pygame.display.set_mode((800, 400)) # Width of 800 pixels, height of 400 pixels
pygame.display.set_caption("Run") # Sets the title of the window

# A Clock object is used to keep track of time and manage the framerate
clock = pygame.time.Clock()

# Making a pygame surface
test_surface = pygame.Surface((100, 200))
test_surface.fill("Red")

while True:
    # We need to check for all the possible types of player input
    for event in pygame.event.get():
        # When a user clicks the X on the window to close it
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Attach the test surface to the display surface
    # .blit() stands for block image transfer
    # .blit() takes two arguments, the surface and the position
    #   I also want to note that the reason that the rectangle is not in the center is because position (0, 0)
    #   starts at the top left corner of the window. So if we do (200, 100), it moves 200 pixels to the right
    #   and 100 pixels from the top
    screen.blit(test_surface, (200, 100))

    pygame.display.update()

    clock.tick(60) # Tells pygame it should never run faster than 60 fps
