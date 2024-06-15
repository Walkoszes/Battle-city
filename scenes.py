from enemy import EnemyFactory
from player import Player
from point import Point
import random
import pygame
import sys
pygame.font.init()

class Scene:
    def __init__(self, game):
        self.game = game # Reference to the Game object

    def start(self):
        # Abstract method to be overridden by subclasses for scene initialization
        pass

    def update(self):
        # Abstract method to be overridden by subclasses for scene updates
        pass

class MainMenu(Scene):
    def __init__(self, game):
        # Initialize the MainMenu scene
        super().__init__(game)
        self.background = pygame.image.load("main_bg.jpg")
        self.document = pygame.image.load("document.png")
        self.play_button = pygame.image.load("play_btn.png")
        self.quit_button = pygame.image.load("quit_btn.png")
        self.play_button_rect = self.play_button.get_rect()
        self.quit_button_rect = self.quit_button.get_rect()
        self.document_rect = self.document.get_rect()
        self.play_button_rect.topleft = (583 // 2 - self.play_button_rect.width // 2, 500 - 200)
        self.quit_button_rect.topleft = (583 // 2 - self.quit_button_rect.width // 2, 500 - 100)
        self.document = pygame.transform.scale(self.document, (50, 50))
        self.document_rect.topright = (800, 40)  # Position in the top right corner

        # Load sound effects
        self.bg_sound = pygame.mixer.Sound("bg_sound_play.wav")

    def update(self):
        # Update method for MainMenu scene handling events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.end()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.game.end()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button_rect.collidepoint(event.pos):  # event.pos - position of the mouse cursor during event
                    self.game.change_scene(Playing(self.game))
                    self.bg_sound.set_volume(0)
                elif self.quit_button_rect.collidepoint(event.pos):
                    self.game.end()
                elif self.document_rect.collidepoint(event.pos):
                    self.game.change_scene(Instruction(self.game))
        # Draw the MainMenu scene
        self.draw()
        self.bg_sound.play()

    def draw(self):
        # Draw method to render MainMenu scene elements
        self.game.screen.blit(self.background, (0, 0))  # Blit layering objects
        self.game.screen.blit(self.play_button, self.play_button_rect.topleft)
        self.game.screen.blit(self.quit_button, self.quit_button_rect.topleft)
        self.game.screen.blit(self.document, self.document_rect.topleft)
        pygame.display.flip()  # Updates the entire display with everything

class Instruction(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.background = pygame.image.load("document_bg.jpg")
        self.document = pygame.image.load("document.png")
        self.document_rect = self.document.get_rect()
        self.document = pygame.transform.scale(self.document, (50, 50))
        self.document_rect.topright = (800, 40)

        # Instruction screen texts
        self.instructions = [
            "Instructions:",
            "Move with arrow keys.",
            "Shoot with spacebar.",
            "Avoid enemies.",
            "One collide with enemy - end.",
            "Collect coins.",
            "Survive as long as possible!"
        ]
        self.instruction_texts = []
        self.load_instruction_texts()

    def load_instruction_texts(self):
        self.font = pygame.font.Font(pygame.font.get_default_font(), 36)  # Use default system font
        for index, line in enumerate(self.instructions):
            text_surface = self.font.render(line, True, (192,192,192))
            text_rect = text_surface.get_rect(center=(self.game.screen.get_width() // 2, 200 + index * 40))
            self.instruction_texts.append((text_surface, text_rect))

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.end()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.game.end()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.document_rect.collidepoint(event.pos): 
                    self.game.change_scene(MainMenu(self.game))
        self.draw()

    def draw(self):
        self.game.screen.blit(self.background, (0, 0))
        self.game.screen.blit(self.document, self.document_rect.topleft)  # Instruction screen background

        # Display instruction texts
        for text_surface, text_rect in self.instruction_texts:
            self.game.screen.blit(text_surface, text_rect)

        pygame.display.flip()

class Playing(Scene):
    def start(self):
        # Initializing player, enemies list, and initial spawns
        self.player = Player(150, Point(150, 450))
        self.enemies = []
        self.spawn_initial_enemies()

    def spawn_initial_enemies(self):
        # Spawn initial enemies for the Playing scene with border limits and area limits
        min_x, min_y = 100, 200
        max_x, max_y = 462 - 40, 485 - 40

        # Spawn 4 basic enemies
        for _ in range(4):
            position = self.get_random_valid_position(min_x, min_y, max_x, max_y)
            self.spawn_enemy("basic", 50, position)

        # Spawn 4 advanced enemies
        for _ in range(4):
            position = self.get_random_valid_position(min_x, min_y, max_x, max_y)
            self.spawn_enemy("advanced", 100, position)

    def update(self):
        # Handling events, player controls, enemy updates, and game state checks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.end()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.game.change_scene(GameOver(self.game))
                if event.key == pygame.K_SPACE:
                    self.game.player.shoot(self.game)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.game.player.move(-2, 0, self.game)
        if keys[pygame.K_RIGHT]:
            self.game.player.move(2, 0, self.game)
        if keys[pygame.K_UP]:
            self.game.player.move(0, -2, self.game)
        if keys[pygame.K_DOWN]:
            self.game.player.move(0, 2, self.game)

        self.game.update_bullets()  # Update bullets
        self.check_player_health()  # Check player health after updates
        self.update_enemies()       # Update enemies
        self.game.draw()            # Update the game's display

    def get_random_valid_position(self, min_x, min_y, max_x, max_y):
        # Get a random valid position within accepteable area (limit borders and area)
        valid_position_found = False
        # Loop until valid position found
        while not valid_position_found:
            x = random.randint(min_x, max_x)
            y = random.randint(min_y, max_y)
            if not self.game.check_collision(x, y):
                valid_position_found = True
        return Point(x, y) # Return Point object with valid coordinates

    def spawn_enemy(self, enemy_type, health, position: Point):
        # Spawn an enemy of specified type at given position
        enemy = EnemyFactory.create_enemy(enemy_type, health, position)
        self.enemies.append(enemy)

    def update_enemies(self):
        # Update all enemies in the Playing scene
        for enemy in self.enemies:
            enemy.move(self.game)

    def check_player_health(self):
        # Check player health and change scene to GameOver if health drops to zero
        if self.game.player.health <= 0:
            self.game.change_scene(GameOver(self.game))

class GameOver(Scene):
    def __init__(self, game):
        # Initialize the GameOver scene
        super().__init__(game)
        self.background = pygame.image.load("over_bg.jpg")

        # Initialize Pygame font module
        self.font = pygame.font.Font(pygame.font.get_default_font(), 36) # Use default system font

    def update(self):
        # Scene handling events and drawing
        self.draw()

    def draw(self):
        # Draw method to render GameOver scene elements
        # Clear objects in the Playing scene
        if isinstance(self.game.current_scene, Playing):
            self.game.current_scene.enemies.clear()
            self.game.current_scene.bullets.clear()
            self.game.current_scene.coins.clear()
            self.game.current_scene.collected_coins.clear()

        # Display the background image
        self.game.screen.blit(self.background, (0, 0))

        # Display "Game Over" text
        text = self.font.render("Game Over", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.game.screen.get_width() // 2, 100))
        self.game.screen.blit(text, text_rect)

        # Calculate and display the score of collected coins
        score_text = f"Score: {len(self.game.collected_coins)}"
        score_rendered = self.font.render(score_text, True, (255, 255, 255))
        score_rect = score_rendered.get_rect(center=(self.game.screen.get_width() // 2, 150))
        self.game.screen.blit(score_rendered, score_rect)

        pygame.display.flip()  # Update the display

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()