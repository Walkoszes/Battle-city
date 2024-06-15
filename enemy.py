from abc import ABC, abstractmethod
from point import Point
import pygame

class EnemyFactory:
    def create_enemy(enemy_type, health, position: Point):
        # Creates and returns an enemy object based on the provided enemy_type.
        if enemy_type == "basic":
            return BasicEnemy(health, position)
        elif enemy_type == "advanced":
            return AdvancedEnemy(health, position)

class Enemy(ABC):
    def __init__(self, health: int, position: Point, image_path: str, damage_on_collision: int):
        self.health = health
        self.initial_health = health  # Store the initial health
        self.position = position
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.mask = pygame.mask.from_surface(self.image)
        self.damage_on_collision = damage_on_collision

    @abstractmethod
    def move(self, game):
        pass

    @abstractmethod
    def check_collision_with_player(self, player):
        pass

    def move_towards_player(self, game, step_size):
        # Moves the enemy towards the player based on step size
        player_pos = game.player.position
        dir_x = player_pos.getX() - self.position.getX()
        dir_y = player_pos.getY() - self.position.getY()

        step_x = 1 if dir_x > 0 else -1
        step_y = 1 if dir_y > 0 else -1

        new_x = self.position.getX() + step_x * step_size
        new_y = self.position.getY() + step_y * step_size

        min_x, min_y = 75, 125
        max_x, max_y = 583 - 25, 546 - 25

        # Check boundaries and collisions
        if min_x <= new_x <= max_x and min_y <= new_y <= max_y and not game.check_collision(new_x, new_y):
            self.position.setX(new_x)
            self.position.setY(new_y)

    def check_collision_with_player(self, player):
        offset = (player.position.getX() - self.position.getX(), player.position.getY() - self.position.getY())
        if self.mask.overlap(player.mask, offset):
            player.decrease_health(10)
            return True
        return False

class BasicEnemy(Enemy):
    def __init__(self, health, position):
        super().__init__(health, position, 'images/enemy_pc.png', 10)

    def move(self, game):
        # Move method to move BasicEnemy towards the player
        self.move_towards_player(game, 1)
        # Check collision with player
        if self.check_collision_with_player(game.player):
            game.player.decrease_health(10)

class AdvancedEnemy(Enemy):
    def __init__(self, health, position):
        super().__init__(health, position, 'images/enemy_pc_adv.png', 50)

    def move(self, game):
        # Move method to move AdvancedEnemy towards the player
        self.move_towards_player(game, 1)

        # Check collision with player
        if self.check_collision_with_player(game.player):
            game.player.decrease_health(10)