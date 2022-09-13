# This code could be heavily commented because it is for me to learn, so I will take notes

import pygame
from sys import exit                # Secure way to end the program
import math                         # For rounding seconds
from random import randint, choice  # For generating random numbers

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Use r"Path" to avoid errors caused by \ in the string
        # Possibly use / instead of \, see here: https://stackoverflow.com/questions/2953834/windows-path-in-python
        # Also consider using os.path
        player_walk_1 = pygame.image.load(r"graphics/player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load(r"graphics/player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0 # Used to pick the walking animation of the player
        self.player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()

        self.image = self.player_walk[self.player_index]

        self.image = pygame.image.load("graphics/player/player_walk_1.png")
        self.rect = self.image.get_rect(midbottom = (200, 300))
        self.gravity = 0

    def player_input(self):
        # This method of getting the keys that were pressed causes a minor delay
        keys = pygame.key.get_pressed()
        # When the player jumps using SPACE
        # Only allow the player to jump if they are touching the ground
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        
        # Block the player from going underneath the ground
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
    
    def animation_state(self):
        # Display the jumping animation when the player is not on the floor
        if self.rect.bottom < 300:
            self.image = self.player_jump
        # Play walking animation if the player is on the floor
        else:
            self.player_index += 0.1 # This allows us to slowly move to the next animation (relative to instant moving back and forth between frames)
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == "fly":
            fly_frame_1 = pygame.image.load(r"graphics/bug/bug1.png").convert_alpha()
            fly_frame_2 = pygame.image.load(r"graphics/bug/bug2.png").convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y_position = 210
        else:
            snail_frame_1 = pygame.image.load(r"graphics/snail/snail1.png").convert_alpha()
            snail_frame_2 = pygame.image.load(r"graphics/snail/snail2.png").convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2]
            y_position = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_position))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy

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

def collisions(player, enemies):
    if enemies:
        for enemies_rect in enemies:
            if player.colliderect(enemies_rect):
                # When we hit an enemy, set game_active = False
                return False
    # When we don't hit an enemy, set game_active = True
    return True

def player_animation():
    global player_surface, player_index

    # Display the jumping animation when the player is not on the floor
    if player_rect.bottom < 300:
        player_surface = player_jump
    # Play walking animation if the player is on the floor
    else:
        player_index += 0.1 # This allows us to slowly move to the next animation (relative to instant moving back and forth between frames)
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]

# pygame.init() - starts pygame and initiates all the sub parts of pygame
pygame.init()
screen = pygame.display.set_mode((800, 400))    # Width of 800 pixels, height of 400 pixels
pygame.display.set_caption("Run")               # Sets the title of the window
clock = pygame.time.Clock()                     # A Clock object is used to keep track of time and manage the framerate
smooth_font = pygame.font.Font(None, 50)        # Arguments: (font type, font size)
pixel_font = pygame.font.Font(r"fonts/Pixeltype.ttf", 50)

# We want to put our player into GroupSingle() because we only want a single sprite in the group
# Group() is for a group with multiple sprites. This will be good for our enemies
# Player Group
player = pygame.sprite.GroupSingle()
player.add(Player())

# Enemy Group
enemy_group = pygame.sprite.Group()

# Background music
background_music = pygame.mixer.Sound(r"audio/music.wav")
background_music.set_volume(0.1)
background_music.play(loops = -1) # loops = -1 means play loop it forever

# Making the pygame surfaces
# .convert() on .png images makes the image more friendly to work with for pygame
# .convert_alpha() removes black and white background behind something like the snail
sky_surface = pygame.image.load(r"graphics/sky.png").convert()
ground_surface = pygame.image.load(r"graphics/ground.png").convert()

# Player
# Creating a player rectangle to gain more control over positioning as opposed to a surface
# .get_rect() gets the surface and draws a rectangle around it
player_walk_1 = pygame.image.load(r"graphics/player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load(r"graphics/player/player_walk_2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0 # Used to pick the walking animation of the player
player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()
player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom = (80, 300))
player_gravity = 0

# Enemies

# A list of all the current enemies
enemy_rect_list = []

# Intro/Restart Screen
player_stand = pygame.image.load(r"graphics/player/player_stand.png").convert_alpha()
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

jump_sound = pygame.mixer.Sound(r"audio/jump.mp3")
jump_sound.set_volume(0.1)

# Enemy timers
# Create a custom user event: We need to + 1 to avoid any conflicts with other events
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500) # (event we want to trigger, how ofter we want to trigger it in milliseconds)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, randint(1800, 2300))

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, randint(1500, 2000))


while True:
    # We need to check for all the possible types of player input
    for event in pygame.event.get():
        # When a user clicks the X on the window to close it
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:

            # Just as a note:
                # choice will pick one of the items to select what enemy spawns
                # In this case, there is a 33% chance for a fly to spawn, 66% for a snail
                # enemy_group.add(Enemy(choice(["fly", "snail", "snail"])))
            if event.type == snail_animation_timer:
                enemy_group.add(Enemy("snail"))
            if event.type == fly_animation_timer:
                enemy_group.add(Enemy("fly"))
               
            #if event.type == obstacle_timer:
                # choice will pick one of the items to select what enemy spawns
                # In this case, there is a 33% chance for a fly to spawn, 66% for a snail
                # enemy_group.add(Enemy(choice(["fly", "snail", "snail"])))
                
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
        player_animation()
        screen.blit(player_surface, player_rect)
        
        player.draw(screen)
        # player.update() is better than doing something like player.jump()
        # Groups have two main functions in pygame, one is to draw them on the screen (.draw()) and
        # the other is to update all of the sprites (.update())
        player.update() # calls update(self) in Player class
        enemy_group.draw(screen)
        enemy_group.update()

        # Enemy movement
        enemy_rect_list = obstacle_movement(enemy_rect_list)

        # Collisions
        game_active = collisions(player_rect, enemy_rect_list)

    # A menu for after the player dies
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_name, game_name_rect)

        # Clear the enemy list so when the game restarts we are not colliding with an enemy
        enemy_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_gravity = 0

        score_message = smooth_font.render(f'Your score: {score}', True, (111, 196, 169))
        score_message_rect = score_message.get_rect(center = (400, 330))

        # If the score is 0, the player just started the game. They are not coming from a death
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()

    clock.tick(60) # Tells pygame it should never run faster than 60 fps
