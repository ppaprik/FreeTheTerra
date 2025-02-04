import pygame

from scripts.Settings import static_settings



class Enemy:
    def __init__(self, x, y, health, damage, score_value, speed, image_path):
        self.x = x
        self.y = y
        self.health = health
        self.damage = damage
        self.score_value = score_value
        self.speed = speed
        self.image = image_path
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.x = float(self.rect.x)


    def update(self, dt, player):
        # Simple AI: move left toward the player
        direction = pygame.math.Vector2(player.boundary.centerx - self.rect.centerx, 0)
        if direction.length() != 0:
            direction.normalize_ip()
        self.x += direction.x * self.speed * dt
        self.rect.x = int(self.x)


    def draw(self, screen, camera_offset_x):
        screen.blit(self.image, (self.rect.x - camera_offset_x, self.rect.y))


    def take_damage(self, damage):
        self.health -= damage


    def is_dead(self):
        return self.health <= 0



class Orc(Enemy):
    def __init__(self, x, y):
        image_path = pygame.image.load(static_settings.getAssetsPath() + "sprites/enemies/orc.png")
        image_path = pygame.transform.scale(image_path, (int(image_path.get_width() * 3), int(image_path.get_height() * 3)))
        super().__init__(x, y,
            health = 20,
            damage = 5,
            score_value = 5,
            speed = 100,
            image_path = image_path
        )



class Zombie(Enemy):
    def __init__(self, x, y):
        image_path = pygame.image.load(static_settings.getAssetsPath() + "sprites/enemies/zombie.gif")
        image_path = pygame.transform.scale(image_path, (int(image_path.get_width() * 0.5), int(image_path.get_height() * 0.5)))
        super().__init__(x, y,
            health = 40,
            damage = 10,
            score_value = 10,
            speed = 150,
            image_path = image_path
        )



class Skeleton(Enemy):
    def __init__(self, x, y):
        image_path = pygame.image.load(static_settings.getAssetsPath() + "sprites/enemies/skeleton.png")
        image_path = pygame.transform.scale(image_path, (int(image_path.get_width() * 3), int(image_path.get_height() * 3)))
        super().__init__(x, y,
            health = 60,
            damage = 15,
            score_value = 15,
            speed = 80,
            image_path = image_path
            )
        



class Boss(Enemy):
    def __init__(self, x, y):
        image_path = pygame.image.load(static_settings.getAssetsPath() + "sprites/enemies/boss.png")
        image_path = pygame.transform.scale(image_path, (int(image_path.get_width() * 3), int(image_path.get_height() * 3)))
        super().__init__(x, y,
            health = 200,
            damage = 100,
            score_value = 50,
            speed = 90,
            image_path = image_path
            )
