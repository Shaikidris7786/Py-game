# Import the pygame module
import pygame

# Import random for random numbers
import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
from pygame.sprite import GroupSingle

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        
        # Default setting
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        
        # Image Loaders RLEACCEL
        # self.surf = pygame.image.load("alien1.gif").convert()
        # self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        
        self.rect = self.surf.get_rect()
    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0,-1)
            print("up",self.rect.top)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,1)
            print("down",self.rect.bottom)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(1,0)
            print("right",self.rect.right)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-1,0)
            print("left",self.rect.left)

        # Keep player on Screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy,self).__init__()
        self.surf = pygame.Surface((20,10))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH+20,SCREEN_WIDTH+100),
                random.randint(0,SCREEN_HEIGHT),
            )
        )
        
        # self.speed = random.randint(5,20)
    def update(self):
        self.rect.move_ip(-1,0)
        if(self.rect.right < 0):
            self.kill()

# Initialize pygame
pygame.init()


# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create a custom event for adding a new Enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY,1000)

# Instantiate player. Right now, this is just a rectangle.
player = Player()

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detectiona and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Variable to keep the main loop running
running = True

# Main loop
while running:
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                print("ESC pressed")
                running = False
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False
            
        # Add a new enemy
        elif event.type == ADDENEMY:
            # Create new enemy and add it to sprite Groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    # Get the set of keys pressed and check for user input
    pressed_keys=pygame.key.get_pressed()

    # Update the player sprite based on user keypresses
    player.update(pressed_keys)
    
    # update enemy position
    enemies.update()

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Draw the player on the screen
    # screen.blit(player.surf, player.rect)

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf,entity.rect)
        
    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player,enemies):
        # If so, remove the player and stop the loop
        player.kill()
        running = False
        print("Enemy touched / Collided with player")        

    # Update the display
    pygame.display.flip()