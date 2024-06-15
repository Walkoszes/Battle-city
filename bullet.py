from point import Point
from coin import Coin
import pygame
import time

class Bullet:
    def __init__(self, game, damage, position: Point, direction: Point):
        # Initialize a Bullet object with specified game, damage, position, and direction
        self.game = game
        self.damage = damage
        self.position = position
        self.direction = direction
        self.image = pygame.image.load('bullet.png')
        self.image = pygame.transform.scale(self.image, (15, 15))
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, game):
        # Move the bullet in its current direction
        new_x = self.position.getX() + self.direction.getX() * 2  # Bullet speed
        new_y = self.position.getY() + self.direction.getY() * 2

        min_x, min_y = 8, 60
        max_x, max_y = 462.8 - 15, 485 - 15

        # Check if the new position is within borders and does not collide with limit area
        if min_x <= new_x <= max_x and min_y <= new_y <= max_y and not game.check_collision(new_x, new_y):
            self.position.setX(new_x)
            self.position.setY(new_y)
        else:
            game.bullets.remove(self) # Remove the bullet if it goes out of borders or collides with enemy

    def draw(self, screen):
        # Draw the bullet on the screen
        screen.blit(self.image, (self.position.getX(), self.position.getY()))

    def check_collision(self, enemies):
        # Check collision between the bullet and enemies
        for enemy in enemies[:]: # Iterate through a copy of enemies list to safely modify original list
            offset = (enemy.position.getX() - self.position.getX(), enemy.position.getY() - self.position.getY())
            # Check if bullet's mask overlaps with enemy's mask
            if self.mask.overlap(enemy.mask, offset):
                enemy.health = enemy.health - self.damage # Decrease enemy's health by bullet's damage
                if enemy.health <= 0:
                    respawn_time = time.time() + 3  # Set the respawn time to 3 seconds later
                    self.game.removed_enemies.append((enemy, respawn_time))
                    enemies.remove(enemy)

                    # Add 5 coins to collected_coins for removing one enemy
                    for _ in range(5):
                        self.game.collected_coins.append(Coin(enemy.position))

                return True
        return False