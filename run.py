# This code could be heavily commented because it is for me to learn, so I will take notes

import pygame
from sys import exit # Secure way to end the program

# pygame.init() - starts pygame and initiates all the sub parts of pygame
pygame.init()
screen = pygame.display.set_mode((800, 400)) # Width of 800 pixels, height of 400 pixels
pygame.display.set_caption("Run") # Sets the title of the window
clock = pygame.time.Clock() # A Clock object is used to keep track of time and manage the framerate
test_font = pygame.font.Font(None, 50) # Arguments: (font type, font size)

# Making the pygame surfaces
# .convert() on .png images makes the image more friendly to work with for pygame
# .convert_alpha() removes black and white background behind something like the snail
sky_surface = pygame.image.load("graphics/sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()
snail_surface = pygame.image.load("graphics\snail\snail1.png").convert_alpha()
player_surface = pygame.image.load("graphics\player\player_walk_1.png").convert_alpha()
text_surface = test_font.render("Score: ", True, "Black") # Arguments: (text, AA, color) - AA - anti-alias option

# Creating a player rectangle to gain more control over positioning as opposed to a surface
# .get_rect() gets the surface and draws a rectangle around it
player_rect = player_surface.get_rect(midbottom = (80, 300))
snail_rect = snail_surface.get_rect(midbottom = (600, 300))

while True:
    # We need to check for all the possible types of player input
    for event in pygame.event.get():
        # When a user clicks the X on the window to close it
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Attach the test surface to the display surface
    # .blit() stands for block image transfer
    # .blit() takes two arguments, the surface and the position, and draws in the order of when you called the code
    #   I also want to note that the reason that the rectangle is not in the center is because position (0, 0)
    #   starts at the top left corner of the window. So if we do (200, 100), it moves 200 pixels to the right
    #   and 100 pixels from the top
    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 300)) # 300 because that is when the sky_surface image ends
    screen.blit(text_surface, (320, 30))
    screen.blit(snail_surface, snail_rect)

    # snail_rect.x is updated in the loop to animate the snail moving towards the player
    snail_rect.x -= 4
    if snail_rect.right <= 0:
        snail_rect.left = 800
    
    # I would like to note that you can print the value of a rectangle. Example:
    # print(player_rect.left)
    screen.blit(player_surface, player_rect)

    pygame.display.update()

    clock.tick(60) # Tells pygame it should never run faster than 60 fps
