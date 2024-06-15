from point import Point
import pygame

class Coin:
    def __init__(self, position: Point):
        # Initialize a Coin object with a given position
        self.position = position
        self.image = pygame.image.load('images/coin.png')
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.mask = pygame.mask.from_surface(self.image) # Create a mask for collision detection

    def draw(self, screen):
        # Draw the coin on the screen
        screen.blit(self.image, (self.position.getX(), self.position.getY()))

    def check_collision_with_player(self, player):
        # Check collision between the coin and the player
        offset = (player.position.getX() - self.position.getX(), player.position.getY() - self.position.getY())
        if self.mask.overlap(player.mask, offset): # Check if masks overlap
            return True # Collision detected
        return False    # No collision