import pygame
import math

from scripts.Settings import Settings, static_settings
from scripts.SoundMusic import Sound, static_music
from scripts.Text import Text


class Player:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.settings = static_settings
        self.pos = [x, y]
        self.size = [width, height]

        self.scale_factor = 3

        self.player_idle = [
            pygame.image.load(self.settings.getAssetsPath() + "sprites/player/idle/Soldier_idle1.png"),
            pygame.image.load(self.settings.getAssetsPath() + "sprites/player/idle/Soldier_idle2.png"),
        ]
        self.player_idle = [pygame.transform.scale(image, (int(image.get_width() * self.scale_factor), int(image.get_height() * self.scale_factor))) for image in self.player_idle]

        self.player_running = [
            pygame.image.load(self.settings.getAssetsPath() + "sprites/player/run/Soldier_move1.png"),
            pygame.image.load(self.settings.getAssetsPath() + "sprites/player/run/Soldier_move2.png"),
            pygame.image.load(self.settings.getAssetsPath() + "sprites/player/run/Soldier_move3.png"),
            pygame.image.load(self.settings.getAssetsPath() + "sprites/player/run/Soldier_move4.png"),
            pygame.image.load(self.settings.getAssetsPath() + "sprites/player/run/Soldier_move5.png"),
            pygame.image.load(self.settings.getAssetsPath() + "sprites/player/run/Soldier_move6.png"),
            pygame.image.load(self.settings.getAssetsPath() + "sprites/player/run/Soldier_move7.png"),
            pygame.image.load(self.settings.getAssetsPath() + "sprites/player/run/Soldier_move8.png")
        ]
        self.player_running = [pygame.transform.scale(image, (int(image.get_width() * self.scale_factor), int(image.get_height() * self.scale_factor))) for image in self.player_running]

        self.player_dead = [
            pygame.image.load(self.settings.getAssetsPath() + "sprites/player/dead/Soldier_dead1.png"),
            pygame.image.load(self.settings.getAssetsPath() + "sprites/player/dead/Soldier_dead2.png"),
            pygame.image.load(self.settings.getAssetsPath() + "sprites/player/dead/Soldier_dead3.png"),
            pygame.image.load(self.settings.getAssetsPath() + "sprites/player/dead/Soldier_dead4.png")
        ]
        self.player_dead = [pygame.transform.scale(image, (int(image.get_width() * self.scale_factor), int(image.get_height() * self.scale_factor))) for image in self.player_dead]

        self.player_damage_taken = [
            pygame.image.load(self.settings.getAssetsPath() + "sprites/player/damage_taken/Soldier_damage1.png"),
            pygame.image.load(self.settings.getAssetsPath() + "sprites/player/damage_taken/Soldier_damage2.png"),
            pygame.image.load(self.settings.getAssetsPath() + "sprites/player/damage_taken/Soldier_damage3.png"),
            pygame.image.load(self.settings.getAssetsPath() + "sprites/player/damage_taken/Soldier_damage4.png")
        ]
        self.player_damage_taken = [pygame.transform.scale(image, (int(image.get_width() * self.scale_factor), int(image.get_height() * self.scale_factor))) for image in self.player_damage_taken]

        self.player_shoot = [
            pygame.image.load(self.settings.getAssetsPath() + "sprites/player/shoot/Soldier_shoot1.png"),
            pygame.image.load(self.settings.getAssetsPath() + "sprites/player/shoot/Soldier_shoot2.png"),
            pygame.image.load(self.settings.getAssetsPath() + "sprites/player/shoot/Soldier_shoot3.png"),
            pygame.image.load(self.settings.getAssetsPath() + "sprites/player/shoot/Soldier_shoot4.png"),
            pygame.image.load(self.settings.getAssetsPath() + "sprites/player/shoot/Soldier_shoot5.png"),
            pygame.image.load(self.settings.getAssetsPath() + "sprites/player/shoot/Soldier_shoot6.png"),
            pygame.image.load(self.settings.getAssetsPath() + "sprites/player/shoot/Soldier_shoot7.png"),
            pygame.image.load(self.settings.getAssetsPath() + "sprites/player/shoot/Soldier_shoot8.png"),
            pygame.image.load(self.settings.getAssetsPath() + "sprites/player/shoot/Soldier_shoot9.png")
        ]
        self.player_shoot = [pygame.transform.scale(image, (int(image.get_width() * self.scale_factor), int(image.get_height() * self.scale_factor))) for image in self.player_shoot]

        self.player_attack = [
            pygame.image.load(self.settings.getAssetsPath() + "sprites/player/attack/Soldier_attack1.png"),
            pygame.image.load(self.settings.getAssetsPath() + "sprites/player/attack/Soldier_attack2.png"),
            pygame.image.load(self.settings.getAssetsPath() + "sprites/player/attack/Soldier_attack3.png"),
            pygame.image.load(self.settings.getAssetsPath() + "sprites/player/attack/Soldier_attack4.png"),
            pygame.image.load(self.settings.getAssetsPath() + "sprites/player/attack/Soldier_attack5.png"),
            pygame.image.load(self.settings.getAssetsPath() + "sprites/player/attack/Soldier_attack6.png")
        ]
        self.player_attack = [pygame.transform.scale(image, (int(image.get_width() * self.scale_factor), int(image.get_height() * self.scale_factor))) for image in self.player_attack]

        self.player_animation_idle_time = 1
        self.player_animation_run_time = 0.1
        self.player_animation_delta = 0
        self.jump_delay = 0.8
        self.jump_delay_timer = 0
        self.sprite_index = 0
        self.velocity = [0.0, 0.0]
        self.max_velocity = 10
        self.speed = 80
        self.gravity = 1
        self.max_fall_velocity = 20
        self.shooting = False
        self.health = 100
        self.health_text = Text(None, 40, "Health: " + str(self.health))
        self.dead = False

        # In __init__ method of Player:
        self.boundary = pygame.Rect(
            self.pos[0], 
            self.pos[1], 
            self.player_idle[0].get_width(), 
            self.player_idle[0].get_height()
        )


    def setHealth(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.dead = True
        self.health_text.setText("Health: " + str(self.health))


    def physics_update(self, physics_delta_time: float):
        pass        


    def update(self, screen, draw_delta_time: float, draw_x=None, draw_y=None):
        # pygame.draw.rect(screen, (255, 0, 0), self.boundary)
        self.move(draw_delta_time)
        self.animation(screen, draw_delta_time, draw_x, draw_y)
        screen.blit(self.health_text.getText(), (10, 50))


    def move(self, physics_delta_time):
        keys = pygame.key.get_pressed()

        self.jump_delay_timer += physics_delta_time
        if self.jump_delay_timer > self.jump_delay:
            if keys[pygame.K_SPACE]:
                Sound(self.settings.getAssetsPath() + "audio/soundeffects/jump.mp3")
                self.velocity[1] = -20
                self.jump_delay_timer = 0

        self.velocity[1] += self.gravity
        if self.velocity[1] > self.max_fall_velocity:
            self.velocity[1] = self.max_fall_velocity

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if self.velocity[0] < -self.max_velocity:
                self.velocity[0] = -self.max_velocity
            else:
                self.velocity[0] += - self.speed * physics_delta_time
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if self.velocity[0] > self.max_velocity:
                self.velocity[0] = self.max_velocity
            else:
                self.velocity[0] += self.speed * physics_delta_time
        else:
            if self.velocity[0] > 0:
                self.velocity[0] -= 1
            else:
                self.velocity[0] = 0


        self.boundary[0] += self.velocity[0]
        self.boundary[1] += self.velocity[1]
        self.pos[0] = self.boundary[0]
        self.pos[1] = self.boundary[1]

        # print(self.pos)


    def shoot(self):
        Sound(self.settings.getAssetsPath() + "audio/soundeffects/shoot.mp3")
        self.shooting = True


    def animation(self, screen, draw_delta_time, draw_x=None, draw_y=None):
        self.player_animation_delta += draw_delta_time

        # If no drawing coordinates are provided, use the internal position.
        if draw_x is None:
            draw_x = self.boundary[0]
        if draw_y is None:
            draw_y = self.boundary[1]

        if self.shooting:
            if self.player_animation_delta >= self.player_animation_run_time:
                self.sprite_index += 1
                self.player_animation_delta = 0
                if self.sprite_index % len(self.player_shoot) == len(self.player_shoot) - 1:
                    self.shooting = False
                    self.sprite_index = 0
            if self.velocity[0] < 0:
                flipped_image = pygame.transform.flip(self.player_shoot[self.sprite_index % len(self.player_shoot)], True, False)
                screen.blit(flipped_image, (draw_x, draw_y))
            else:
                screen.blit(self.player_shoot[self.sprite_index % len(self.player_shoot)], (draw_x, draw_y))
        else:
            # (Choose the correct animation sequence based on velocity)
            if self.velocity[0] == 0 and self.velocity[1] == 0:
                if self.player_animation_delta >= self.player_animation_idle_time:
                    self.sprite_index += 1
                    self.player_animation_delta = 0
                screen.blit(self.player_idle[self.sprite_index % len(self.player_idle)], (draw_x, draw_y))
            elif self.velocity[0] > 0:
                if self.player_animation_delta >= self.player_animation_run_time:
                    self.sprite_index += 1
                    self.player_animation_delta = 0
                screen.blit(self.player_running[self.sprite_index % len(self.player_running)], (draw_x, draw_y))
            elif self.velocity[0] < 0:
                if self.player_animation_delta >= self.player_animation_run_time:
                    self.sprite_index += 1
                    self.player_animation_delta = 0
                flipped_image = pygame.transform.flip(self.player_running[self.sprite_index % len(self.player_running)], True, False)
                screen.blit(flipped_image, (draw_x, draw_y))
            elif self.velocity[0] == 0 and self.velocity[1] != 0:
                if self.player_animation_delta >= self.player_animation_run_time:
                    self.sprite_index += 1
                    self.player_animation_delta = 0
                screen.blit(self.player_running[self.sprite_index % len(self.player_running)], (draw_x, draw_y))
