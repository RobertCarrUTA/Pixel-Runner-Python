# This code could be heavily commented because it is for me to learn, so I will take notes

import pygame
from sys import exit    # Secure way to end the program
import math             # For rounding seconds

def display_score():
    # pygame.time.get_ticks() will give us a time in milliseconds since we called pygame.init
    # We need to subtract the time since we last restarted to reset the timer to 0 every restart
    current_time_milliseconds = pygame.time.get_ticks() - start_time
    current_time = math.floor(current_time_milliseconds/1000)
    
    # f'{}' might be more secure and faster than str()?
    score_surface = smooth_font.render(f'Score: {current_time}', True, "Black") # Arguments: (text, AA, color) - AA - anti-alias option
    score_rect = score_surface.get_rect(center = (400, 50))
    screen.blit(score_surface, score_rect)
    
    return current_time


# pygame.init() - starts pygame and initiates all the sub parts of pygame
pygame.init()
screen = pygame.display.set_mode((800, 400)) # Width of 800 pixels, height of 400 pixels
pygame.display.set_caption("Run") # Sets the title of the window
clock = pygame.time.Clock() # A Clock object is used to keep track of time and manage the framerate
smooth_font = pygame.font.Font(None, 50) # Arguments: (font type, font size)
pixel_font = pygame.font.Font("fonts\Pixeltype.ttf", 50)

# Making the pygame surfaces
# .convert() on .png images makes the image more friendly to work with for pygame
# .convert_alpha() removes black and white background behind something like the snail
sky_surface = pygame.image.load("graphics/sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()
snail_surface = pygame.image.load("graphics\snail\snail1.png").convert_alpha()
player_surface = pygame.image.load("graphics\player\player_walk_1.png").convert_alpha()

# Creating a player rectangle to gain more control over positioning as opposed to a surface
# .get_rect() gets the surface and draws a rectangle around it
player_rect = player_surface.get_rect(midbottom = (80, 300))
snail_rect = snail_surface.get_rect(midbottom = (600, 300))

player_gravity = 0

# Intro/Restart Screen
player_stand = pygame.image.load("graphics\player\player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2) # (surface, angel, scale)
player_stand_rect = player_stand.get_rect(center = (400, 200))

game_name = pixel_font.render("Pixel Runner", False, (111, 196, 169))
game_name_rect = game_name.get_rect(center = (400, 80))

# End message
game_message = smooth_font.render("Press Space to play", True, (111, 196, 169)) # Arguments: (text, AA, color) - AA - anti-alias option
game_message_rect = game_message.get_rect(center = (400, 340))

game_active = False
start_time = 0 # Keep track of our time
score = 0

while True:
    # We need to check for all the possible types of player input
    for event in pygame.event.get():
        # When a user clicks the X on the window to close it
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:    
            if event.type == pygame.KEYDOWN:
                # When the player jumps using SPACE
                if event.key == pygame.K_SPACE:
                    # Only allow the player to jump if they are touching the ground
                    if player_rect.bottom == 300:
                        player_gravity = -20
        else:
            # Reset the game if the player presses space again
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                snail_rect.left = 800
                game_active = True

                # Lets us restart our time every time we restart
                start_time = pygame.time.get_ticks()

    if game_active:
        # Attach the test surface to the display surface
        # .blit() stands for block image transfer
        # .blit() takes two arguments, the surface and the position, and draws in the order of when you called the code
        #   I also want to note that the reason that the rectangle is not in the center is because position (0, 0)
        #   starts at the top left corner of the window. So if we do (200, 100), it moves 200 pixels to the right
        #   and 100 pixels from the top
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300)) # 300 because that is when the sky_surface image ends
        score = display_score()

        # Snail
        # snail_rect.x is updated in the loop to animate the snail moving towards the player
        snail_rect.x -= 6
        if snail_rect.right <= 0:
            snail_rect.left = 800
        screen.blit(snail_surface, snail_rect)

        # Player
        # I would like to note that you can print the value of a rectangle. Example:
        # print(player_rect.left)
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player_surface, player_rect)

        # Collisions
        if snail_rect.colliderect(player_rect):
            game_active = False
    # A menu for after the player dies
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_name, game_name_rect)

        score_message = smooth_font.render(f'Your score: {score}', True, (111, 196, 169))
        score_message_rect = score_message.get_rect(center = (400, 330))

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()

    clock.tick(60) # Tells pygame it should never run faster than 60 fps
