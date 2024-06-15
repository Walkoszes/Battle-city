from point import Point
from bullet import Bullet
import pygame

class Player:
    def __init__(self, health: int, position: Point):
        # Initialize player attributes
        self.health = health
        self.position = position
        self.image = pygame.image.load("images/player.png")
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, x: int, y: int, game):
        # Move player based on keyboard input
        new_x = self.position.getX() + x
        new_y = self.position.getY() + y

        min_x, min_y = 8, 60
        max_x, max_y = 462.8 - 25, 485 - 25 

        # Check if player doesn't go out from limited coordinates and doesn't collide with borders
        if min_x <= new_x <= max_x and min_y <= new_y <= max_y and not game.check_collision(new_x, new_y):
            self.position.setX(new_x)
            self.position.setY(new_y)
            self.direction = Point(x, y)  # Update direction based on movement

    def shoot(self, game):
        # Create a bullet and add it to the game's bullet list
        bullet_position = Point(self.position.getX(), self.position.getY())
        bullet = Bullet(game, 10, bullet_position, self.direction)
        game.bullets.append(bullet)

    def decrease_health(self, damage):
        # Decrease player's health
        self.health = self.health - damage