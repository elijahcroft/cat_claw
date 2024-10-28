import pygame
import random

class Cat:
    def __init__(self, screen_width, ground_level):
        # Spawn at a random x position, y starts at 0 (top of the screen)
        self.position = pygame.Vector2(random.randint(0, screen_width-300), 0)
        self.velocity = pygame.Vector2(0, 0)
        self.ground_level = ground_level  # Set the ground level for gravity to stop

    def fall(self, gravity=3.2):
        self.velocity.y += gravity  # Apply gravity
        self.position.y += self.velocity.y  # Update position by velocity

        # Stop falling if the cat reaches the ground
        if self.position.y >= self.ground_level:
            self.position.y = self.ground_level
            self.velocity.y = 0
