import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Player Gravity")

# Load images
player_image = pygame.image.load("sexy.png").convert_alpha()
ground_image = pygame.image.load("groundTest.png").convert_alpha()

# Define the Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_y = 0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        # Apply gravity
        self.velocity_y += 1

        # Move the player vertically based on velocity
        self.rect.y += self.velocity_y

        # Check if the player has collided with the ground
        offset = (self.rect.x - ground.rect.x, self.rect.y - ground.rect.y)
        if ground.mask.overlap(self.mask, offset):
            # Stop the player from falling
            self.velocity_y = 0

# Define the Ground class
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ground_image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        pass

# Create a Group for the player and ground
all_sprites = pygame.sprite.Group()
ground = Ground()
all_sprites.add(ground)

# Create the player and add it to the Group
player = Player(400, 0)
all_sprites.add(player)

# Set up the clock
clock = pygame.time.Clock()

# Run the game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update the player and ground
    player.update()
    ground.update()

    # Draw the sprites on the screen
    screen.fill((255, 255, 255))
    all_sprites.draw(screen)

    # Update the display
    pygame.display.update()

    # Set the frame rate
    clock.tick(60)