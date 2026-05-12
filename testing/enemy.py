import pygame
import math

class Enemy(pygame.sprite.Sprite):
    """
    Enemy sprite that:
    - Spawns randomly on screen
    - Moves towards the player
    - Takes damage from player attacks
    - Damages player on collision
    - Dies when health reaches 0
    """
    def __init__(self, player, x, y, display_w, display_h):
        super().__init__()
        self.player = player
        self.display_w = display_w
        self.display_h = display_h
        
        # Load and set up image
        self.image = pygame.image.load('Enemies_resized/01.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = pygame.math.Vector2(self.rect.topleft)
        
        # Enemy stats
        self.health = 2
        self.max_health = 2
        self.speed = 2
        self.damage = 1
        self.damage_cooldown = 0
        self.damage_cooldown_max = 60  # Frames between damage hits to player
        
        # For visual feedback
        self.hit_timer = 0
        self.hit_flash_duration = 10
        self.original_image = self.image
        self.is_alive = True
        
    def get_collision_rect(self):
        collision_rect = self.rect.inflate(-int(self.rect.width * 0.5), -int(self.rect.height * 0.5))
        collision_rect.center = self.rect.center
        return collision_rect

    def update(self):
        """Update enemy movement and collision detection"""
        # Move towards player
        if self.player:
            direction = pygame.math.Vector2(
                self.player.rect.centerx - self.rect.centerx,
                self.player.rect.centery - self.rect.centery
            )
            if direction.length() > 0:
                direction = direction.normalize()
                self.pos += direction * self.speed
                self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        # Keep enemy on screen
        self.rect.x = max(0, min(self.rect.x, self.display_w - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, self.display_h - self.rect.height))
        self.pos.x = self.rect.x
        self.pos.y = self.rect.y
        
        # Update hit flash
        if self.hit_timer > 0:
            self.hit_timer -= 1
            # Flash effect - alternate transparency
            if self.hit_timer % 4 < 2:
                self.image = self.original_image.copy()
                self.image.set_alpha(150)
            else:
                self.image = self.original_image
    
    def take_damage(self, damage):
        """Take damage from player attack"""
        self.health -= damage
        self.hit_timer = self.hit_flash_duration
        
        if self.health <= 0:
            self.is_alive = False
            self.kill()
    
    def draw(self, surface):
        """Draw the enemy to the surface"""
        surface.blit(self.image, self.rect)
    
    def get_attack_rect(self):
        """Return the rectangle for collision detection"""
        return self.rect
