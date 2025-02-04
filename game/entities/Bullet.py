import pygame

from scripts.Settings import static_settings


class Bullet:
    def __init__(self, start_pos, target_pos, damage=10):
        self.damage = damage  # Set bullet damage (adjust as needed)
        self.settings = static_settings
        self.sprite = pygame.image.load(self.settings.getAssetsPath() + "sprites//player/bullet/bullet1.png")
        self.sprite = pygame.transform.scale(self.sprite, (10, 10))
        
        self.pos = list(start_pos)
        self.speed = 500  # pixels per second
        self.lifespan = 5.0  # seconds
        self.age = 0.0

        # Calculate normalized direction vector from start_pos to target_pos
        direction = pygame.math.Vector2(target_pos[0] - start_pos[0], target_pos[1] - start_pos[1])
        if direction.length() != 0:
            direction = direction.normalize()
        self.velocity = direction * self.speed

        # Create a rect for collision detection
        self.rect = self.sprite.get_rect(center=self.pos)

    def update(self, delta_time, blocks):
        self.age += delta_time
        self.pos[0] += self.velocity.x * delta_time
        self.pos[1] += self.velocity.y * delta_time
        self.rect.center = (self.pos[0], self.pos[1])
        
        # Check collision with blocks if needed
        for block in blocks:
            if self.rect.colliderect(block.boundary):
                self.age = self.lifespan  # Expire the bullet if collision occurs

    def is_expired(self):
        return self.age >= self.lifespan

    def draw(self, screen, camera_offset_x):
        screen.blit(self.sprite, (self.pos[0] - camera_offset_x, self.pos[1]))

