import pygame
import random

from scripts.UI import Button
from scripts.Settings import Settings, static_settings
from scripts.SceneManager import SceneManager, static_scene_manager
from scripts.SoundMusic import Music, static_music
from entities.Player import Player
from scripts.Text import Text
from scripts.Camera import Camera
from scripts.Shapes import Block, StoneBlock, GrassBlock, DirtBlock
from entities.Bullet import Bullet
from entities.Enemy import Orc, Zombie, Skeleton, Boss
from scenes.GameOver import GameOver


#----------------------------------------------------------------------------------------------------
# Game Scene class
class GameScene:
    def __init__(self, screen: pygame.surface.Surface) -> None:
        self.screen: pygame.surface.Surface = screen
        self.settings: Settings = static_settings
        self.settings.score = 0
        self.scene_manager: SceneManager = static_scene_manager
        self.buttons: list = [
            Button(pygame.display.Info().current_w - 40, 10, 30, 30, text="||", on_click=self.pause),
        ]
        self.music: Music = static_music
        self.music.play(self.settings.getAssetsPath() + "audio/music/Terraria Music - Day.mp3")

        self.score = Text(None, 40, "Score:")
        self.player = Player(30000, 0, 32, 32)
        self.camera = Camera(self.screen.get_width(), self.screen.get_height())

        self.background = [
            pygame.image.load(self.settings.getAssetsPath() + "sprites/terrain/bg.png")
            for _ in range(200)  # Increased from 10 to 20 for wider coverage
        ]

        self.blocks = []
        block_width = 28 * 2
        block_height = 9 * 2

        for i in range(1, 1000):
            # Grass layer (top)
            grass_block = GrassBlock(28 * i * 2, pygame.display.Info().current_h - block_height * 6, block_width, block_height)
            self.blocks.append(grass_block)
            
            # Dirt layer (middle)
            dirt_block = DirtBlock(28 * i * 2, pygame.display.Info().current_h - block_height * 4, block_width, block_height)
            self.blocks.append(dirt_block)

            # Stone layer (bottom)
            stone_block = StoneBlock(28 * i * 2, pygame.display.Info().current_h - block_height * 2, block_width, block_height)
            self.blocks.append(stone_block)
        self.bullets = []
        self.shoot_cooldown_timer = 0

        # In __init__ (after initializing bullets):
        self.enemies = []
        self.current_wave = 1

        self.wave_text = Text(None, 40, "Wave: " + str(self.current_wave))
        self.spawn_wave()


    def spawn_wave(self):
        """
            Spawns enemies based on the current wave number.
            Waves 1-4 spawn regular enemies with shifting probabilities.
            Wave 5 spawns a Boss.
            After wave 5, waves continue infinitely with increased difficulty.
        """
        self.enemies = []

        if self.current_wave < 5:
            num_enemies = self.current_wave * 5  # Increase enemy count each wave
            for _ in range(num_enemies):
                # Spawn enemy a bit ahead of the player
                spawn_x = self.player.pos[0] + 400 + random.randint(0, 200)
                spawn_y = self.screen.get_height() - 105  # ground level
                r = random.random()
                if self.current_wave == 1:
                    # Wave 1: Mostly Orcs
                    if r < 0.8:
                        enemy = Orc(spawn_x, spawn_y)
                    else:
                        enemy = Zombie(spawn_x, spawn_y)
                elif self.current_wave == 2:
                    if r < 0.6:
                        enemy = Orc(spawn_x, spawn_y)
                    elif r < 0.9:
                        enemy = Zombie(spawn_x, spawn_y)
                    else:
                        enemy = Skeleton(spawn_x, spawn_y)
                elif self.current_wave == 3:
                    if r < 0.4:
                        enemy = Orc(spawn_x, spawn_y)
                    elif r < 0.8:
                        enemy = Zombie(spawn_x, spawn_y)
                    else:
                        enemy = Skeleton(spawn_x, spawn_y)
                elif self.current_wave == 4:
                    if r < 0.2:
                        enemy = Orc(spawn_x, spawn_y)
                    elif r < 0.6:
                        enemy = Zombie(spawn_x, spawn_y)
                    else:
                        enemy = Skeleton(spawn_x, spawn_y)
                self.enemies.append(enemy)
        elif self.current_wave % 5 == 0:
            # Wave 5: Boss wave
            spawn_x = self.player.pos[0] + 400 + random.randint(0, 200)
            spawn_y = self.screen.get_height() - 200
            boss = Boss(spawn_x, spawn_y)
            self.enemies.append(boss)
        else:
            # Infinite waves after wave 5: Increase enemy count/difficulty gradually.
            num_enemies = (self.current_wave - 4) * 5
            for _ in range(num_enemies):
                spawn_x = self.player.pos[0] + 400 + random.randint(0, 200)
                spawn_y = self.screen.get_height() - 105
                r = random.random()
                if r < 0.3:
                    enemy = Orc(spawn_x, spawn_y)
                elif r < 0.7:
                    enemy = Zombie(spawn_x, spawn_y)
                else:
                    enemy = Skeleton(spawn_x, spawn_y)
                self.enemies.append(enemy)

    
    def updateHeight(self):
        self.blocks = []
        block_width = 28 * 2
        block_height = 9 * 2
        for i in range(1, 1000):
            # Grass layer (top)
            grass_block = GrassBlock(28 * i * 2, pygame.display.Info().current_h - block_height * 6, block_width, block_height)
            self.blocks.append(grass_block)
            
            # Dirt layer (middle)
            dirt_block = DirtBlock(28 * i * 2, pygame.display.Info().current_h - block_height * 4, block_width, block_height)
            self.blocks.append(dirt_block)

            # Stone layer (bottom)
            stone_block = StoneBlock(28 * i * 2, pygame.display.Info().current_h - block_height * 2, block_width, block_height)
            self.blocks.append(stone_block)

        self.player.pos[0] = self.screen.get_width() // 2
        self.player.pos[1] = self.screen.get_height() - 100


    def update(self, draw_delta_time: float):
        if self.settings.updated == False:
            self.updateHeight()
            self.settings.updated = True

        self.screen.fill(self.settings.getColor("SKY_BLUE"))

        if "Pause" not in self.scene_manager.getCurrentScenes() and "Options" not in self.scene_manager.getCurrentScenes():
            for index, bg in enumerate(self.background):
                bg_x = index * 576 - self.camera.offset_x
                self.screen.blit(bg, (bg_x, self.screen.get_height() - 324 - 105))

            self.screen.blit(self.score.getText(), (10, 10))
                
            self.screen.blit(self.wave_text.getText(), (self.screen.get_width() // 2 - self.wave_text.getText().get_width() // 2, 10))
            # Update player
            player_draw_x = self.screen.get_width() // 2 - self.player.boundary.width // 2
            player_draw_y = self.player.pos[1]
            self.player.update(self.screen, draw_delta_time, player_draw_x, player_draw_y)

            # Update camera
            self.camera.update(self.player)

            # Render buttons
            for button in self.buttons:
                pos = [self.screen.get_width() - button.getSize()[0] - 10, 10]
                button.updatePos(pos)
                button.onClick()
                button.draw(self.screen)

            # Render blocks relative to the camera
            for block in self.blocks:
                render_x = block.boundary.x - self.camera.offset_x
                render_y = block.boundary.y
                if render_x + block.boundary.width >= 0 and render_x <= self.screen.get_width():
                    self.screen.blit(block.sprite, (render_x, render_y))

            # Handle shooting
            self.handle_shooting(draw_delta_time)

            # Update and draw bullets
            for bullet in self.bullets:
                bullet.update(draw_delta_time, self.blocks)
            self.bullets = [bullet for bullet in self.bullets if not bullet.is_expired()]
            for bullet in self.bullets:
                bullet.draw(self.screen, self.camera.offset_x)

            self.checkCollision()

            # --------------------------------------
            # Enemy Handling - ADDED CODE BELOW
            # --------------------------------------

            # Check if all enemies are defeated to start the next wave
            if len(self.enemies) == 0:
                self.current_wave += 1
                self.wave_text.setText(f"Wave {self.current_wave}")
                self.spawn_wave()


            # Bullet-Enemy Collision
            for bullet in self.bullets:
                for enemy in self.enemies:
                    if bullet.rect.colliderect(enemy.rect):
                        enemy.take_damage(bullet.damage)
                        bullet.age = bullet.lifespan  # Expire bullet on hit

            # Update and Draw Enemies
            for enemy in self.enemies:
                enemy.update(draw_delta_time, self.player)
                enemy.draw(self.screen, self.camera.offset_x)

                # If enemy collides with player, reduce player's health and remove enemy
                if enemy.rect.colliderect(self.player.boundary):
                    self.player.setHealth(enemy.damage)
                    self.enemies.remove(enemy)

                # Remove enemy if dead and add score
                if enemy.is_dead():
                    self.settings.score += enemy.score_value
                    self.score.setText(str(self.settings.score))
                    self.enemies.remove(enemy)

            if self.player.dead:
                with open(self.settings.getRunPath() + "setting.txt", "w") as file:
                    if self.settings.best_score < self.settings.score:
                        self.settings.best_score = self.settings.score
                    array = [str(self.settings.getMusicVolume()) + "\n", 
                             str(self.settings.getSoundVolume()) + "\n", 
                             "0\n", 
                             str(self.settings.best_score) + "\n"
                            ]
                    file.writelines(array)
                self.scene_manager.addScene("GameOver", GameOver(self.screen))
                self.scene_manager.addCurrentScene("GameOver")
                self.scene_manager.removeCurrentScene("GameScene")

            
    def handle_shooting(self, dt):
        """Handles shooting bullets with a cooldown timer."""
        self.shoot_cooldown_timer -= dt  # Reduce cooldown over time

        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] and self.shoot_cooldown_timer <= 0:
            self.shoot_cooldown_timer = 0.1
            self.player.shoot()

            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Convert screen position to world position (consider camera offset)
            world_mouse_x = mouse_x + self.camera.offset_x
            world_mouse_y = mouse_y

            # Bullet starts exactly at the player's center
            if self.settings.isFullscreen():
                bullet_start = (
                    self.player.boundary.x - self.player.boundary.width // 2 + self.settings.fullscreenSize()[0] // 2,
                    self.player.boundary.y + self.player.boundary.height // 2
                )
            else:
                bullet_start = (
                    self.player.pos[0],
                    # self.player.boundary.x - self.player.boundary.width // 2 + self.settings.getSceenSize()[0] // 2,
                    self.player.boundary.y + self.player.boundary.height // 2
                )

            # Create and add a new bullet
            new_bullet = Bullet(bullet_start, (world_mouse_x, world_mouse_y))
            self.bullets.append(new_bullet)


    def checkCollision(self):
        for block in self.blocks:
            if self.player.boundary.colliderect(block.boundary):
                # Calculate overlaps on both axes
                overlap_x = (self.player.boundary.width + block.boundary.width) / 2 - abs(self.player.boundary.centerx - block.boundary.centerx)
                overlap_y = (self.player.boundary.height + block.boundary.height) / 2 - abs(self.player.boundary.centery - block.boundary.centery)

                if overlap_x < overlap_y:
                    # Horizontal collision
                    if self.player.boundary.centerx < block.boundary.centerx:
                        self.player.boundary.right = block.boundary.left
                    else:
                        self.player.boundary.left = block.boundary.right
                    self.player.velocity[0] = 0  # Stop horizontal movement
                else:
                    # Vertical collision
                    if self.player.boundary.centery < block.boundary.centery:
                        self.player.boundary.bottom = block.boundary.top
                        self.player.velocity[1] = 0  # Stop vertical movement
                    else:
                        self.player.boundary.top = block.boundary.bottom
                        self.player.velocity[1] = 0
            

    #--------------------------------------------------
    # Events

    def pause(self):
        if "Pause" not in self.scene_manager.getCurrentScenes():
            self.scene_manager.addCurrentScene("Pause")