# This code could be heavily commented because it is for me to learn, so I will take notes

import pygame
from sys import exit        # Secure way to end the program
import math                 # For rounding seconds
from random import randint  # For generating random numbers

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

def obstacle_movement(enemy_list):
    if enemy_list:
        for enemy_rect in enemy_list:
            enemy_rect.x -= 5

            # Differentiate between snail and fly rectangles
            if enemy_rect.bottom == 300:
                screen.blit(snail_surface, enemy_rect)
            else:
                screen.blit(fly_surface, enemy_rect)

        # List comprehension to check if enemies need to be removed (they have gone off screen)
        # This copies every item in the list if the enemy has not gone off the left side border of the window
        enemy_list = [enemy for enemy in enemy_list if enemy.x > -100]

        return enemy_list
    else:
        # If the list is empty, which it will be when we start, we need to return an empty list
        # If we do not return an empty list, this function will return NoneType, which cannot use append. See error:
        # AttributeError: 'NoneType' object has no attribute 'append'
        return []


# pygame.init() - starts pygame and initiates all the sub parts of pygame
pygame.init()
screen = pygame.display.set_mode((800, 400)) # Width of 800 pixels, height of 400 pixels
pygame.display.set_caption("Run") # Sets the title of the window
clock = pygame.time.Clock() # A Clock object is used to keep track of time and manage the framerate
smooth_font = pygame.font.Font(None, 50) # Arguments: (font type, font size)
pixel_font = pygame.font.Font("fonts\Pixeltype.ttf", 50)

# Background music
background_music = pygame.mixer.Sound("audio/music.wav")
background_music.set_volume(0.1)
background_music.play(loops = -1) # loops = -1 means play loop it forever

# Making the pygame surfaces
# .convert() on .png images makes the image more friendly to work with for pygame
# .convert_alpha() removes black and white background behind something like the snail
sky_surface = pygame.image.load("graphics/sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()

# Player
# Creating a player rectangle to gain more control over positioning as opposed to a surface
# .get_rect() gets the surface and draws a rectangle around it
player_surface = pygame.image.load("graphics\player\player_walk_1.png").convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80, 300))
player_gravity = 0

# Enemies
# Use r"Path" to avoid errors caused by \ in the string
snail_surface = pygame.image.load(r"graphics\snail\snail1.png").convert_alpha()
fly_surface = pygame.image.load(r"graphics\bug\bug1.png").convert_alpha()

# A list of all the current enemies
enemy_rect_list = []

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

jump_sound = pygame.mixer.Sound("audio\jump.mp3")
jump_sound.set_volume(0.1)

# Enemy timers
# Create a custom user event: We need to + 1 to avoid any conflicts with other events
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500) # (event we want to trigger, how ofter we want to trigger it in milliseconds)



while True:
    # We need to check for all the possible types of player input
    for event in pygame.event.get():
        # When a user clicks the X on the window to close it
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                if randint(0, 2):
                    enemy_rect_list.append(snail_surface.get_rect(midbottom = (randint(900, 1100), 300)))
                else:
                    enemy_rect_list.append(fly_surface.get_rect(midbottom = (randint(900, 1100), 210)))

                
            if event.type == pygame.KEYDOWN:
                # When the player jumps using SPACE
                if event.key == pygame.K_SPACE:
                    # Only allow the player to jump if they are touching the ground
                    if player_rect.bottom == 300:
                        jump_sound.play()
                        player_gravity = -20
        else:
            # Reset the game if the player presses space again
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True

                # Lets us restart our time every time we restart
                start_time = pygame.time.get_ticks()

    # While the game is active
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

        # Player
        # I would like to note that you can print the value of a rectangle. Example:
        # print(player_rect.left)
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player_surface, player_rect)

        # Enemy movement
        enemy_rect_list = obstacle_movement(enemy_rect_list)

    # A menu for after the player dies
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_name, game_name_rect)

        score_message = smooth_font.render(f'Your score: {score}', True, (111, 196, 169))
        score_message_rect = score_message.get_rect(center = (400, 330))

        # If the score is 0, the player just started the game. They are not coming from a death
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()

    clock.tick(60) # Tells pygame it should never run faster than 60 fps
