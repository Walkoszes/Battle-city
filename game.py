from scenes import MainMenu, Playing
from player import Player
from point import Point
from coin import Coin
import random
import pygame
import time
import sys

class Game:
    def __init__(self):
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((583, 546))
        pygame.display.set_caption("Battle City")

        # Load images and masks
        self.background = pygame.image.load("images/background.png")
        self.playground = pygame.image.load("images/playground.png")
        self.borders_img = pygame.image.load("images/boarders.png")
        self.player_img = pygame.image.load("images/player.png")
        self.player_img = pygame.transform.scale(self.player_img, (25, 25))
        self.player_mask = pygame.mask.from_surface(self.player_img)
        self.borders_mask = pygame.mask.from_surface(self.borders_img)

        # Initialize player and scene
        self.player = Player(100, Point(75, 125))
        self.current_scene = MainMenu(self)
        self.bullets = []
        self.coins = []            # New list to store coins
        self.collected_coins = []  # List to store obtainde coins
        self.removed_enemies = []  # List to track removed enemies and their respawn times

        # Load sound effects
        self.collision_sound = pygame.mixer.Sound("sounds/collision_coin.wav")

        # Flag to control coin generation
        self.coins_enabled = False  # Coins generation disabled by default

    def start(self):
        while True:
            self.update()

    def update(self):
        self.current_scene.update()
        self.update_bullets()
        if self.coins_enabled:  # Only update coins if coins are enabled
            self.update_coins()
        self.respawn_enemies()

    def update_coins(self):
        # Generate coins occasionally in limited area
        min_x, min_y = 8, 60
        max_x, max_y = 462 - 40, 485 - 40

        if random.random() < 0.01: #
            valid_position_found = False
            while not valid_position_found:
                coin_x = random.randint(min_x, max_x)
                coin_y = random.randint(min_y, max_y)
                coin_position = Point(coin_x, coin_y)

                coin = Coin(coin_position)

                if not self.check_coin_collision(coin):
                    valid_position_found = True

            self.coins.append(coin)

        # Check collision with player and update collected coins
        for coin in self.coins[:]:
            if coin.check_collision_with_player(self.player):
                self.coins.remove(coin)
                self.collected_coins.append(coin)
                self.collision_sound.play()

    def update_bullets(self):
        # Update bullets' positions and check collisions with enemies
        min_x, min_y = 8, 60
        max_x, max_y = 462.8 - 15, 485 - 15
        for bullet in self.bullets[:]:
            bullet.move(self)
            #Check if the bullet collided with enemy
            if bullet.check_collision(self.current_scene.enemies):
                self.bullets.remove(bullet)
            #Check if bullet goes out from field
            if bullet.position.getX() < min_x or bullet.position.getX() > max_x or bullet.position.getY() < min_y or bullet.position.getY() > max_y:
                self.bullets.remove(bullet)

    def respawn_enemies(self):
        # Respawn enemies after a certain time
        current_time = time.time()
        for enemy, respawn_time in self.removed_enemies[:]:
            if current_time >= respawn_time: #respawn_time = 3 sec
                self.removed_enemies.remove((enemy, respawn_time))
                enemy.health = enemy.initial_health  # Reset enemy health
                self.current_scene.enemies.append(enemy)

    def change_scene(self, new_scene):
        # Change the current scene
        self.current_scene = new_scene
        self.current_scene.start()

    def end(self):
        pygame.quit()
        sys.exit()

    def draw(self):
        # Draw game elements on the screen
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.playground, (0, 0))
        self.screen.blit(self.borders_img, (0, 0))
        player_position = (self.player.position.getX(), self.player.position.getY())
        self.screen.blit(self.player_img, player_position)

        # Display score
        pygame.font.init()
        font = pygame.font.Font(pygame.font.get_default_font(), 24)
        score_text = f"Score: {len(self.collected_coins)}"
        score_rendered = font.render(score_text, True, (0, 0, 0))
        score_rect = score_rendered.get_rect(right=583 - 20, top=150)
        self.screen.blit(score_rendered, score_rect)

        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(self.screen)

        # Draw enemies if the current scene is Playing
        if isinstance(self.current_scene, Playing): #scene are only performed when self.current_scene is an instance of Playing
            for enemy in self.current_scene.enemies:
                self.screen.blit(enemy.image, (enemy.position.getX(), enemy.position.getY()))

        # Draw coins
        for coin in self.coins:
            coin.draw(self.screen)

        pygame.display.flip()  # Update the display to show changes

    def check_collision(self, x, y):
        # Check collision with borders
        offset = (int(x), int(y))
        overlap = self.borders_mask.overlap(self.player.mask, offset)
        return overlap is not None

    def check_enemy_collision(self, enemy):
        # Check collision between enemy and borders
        offset = (enemy.position.getX(), enemy.position.getY())
        return self.borders_mask.overlap(enemy.mask, offset) is not None

    def check_coin_collision(self, coin):
        # Check collision between coins and borders
        offset = (coin.position.getX(), coin.position.getY())
        return self.borders_mask.overlap(coin.mask, offset) is not None

    def start_coin_generation(self):
        # Enable coin generation
        self.coins_enabled = True

    def stop_coin_generation(self):
        # Disable coin generation
        self.coins_enabled = False