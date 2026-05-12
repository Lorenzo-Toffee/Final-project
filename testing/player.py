import pygame
from spritesheet import Spritesheet

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.KEY_a ,self.KEY_w, self.KEY_s, self.KEY_d, self.FACING_LEFT ,self.click =False, False, False, False, False, False
        self.load_frames()
        self.rect = self.idle_frames_left[0].get_rect()
        self.rect.midbottom = (500, 600)
        self.current_frame = 0
        self.last_updated = 0
        self.velocity = 0
        self.state = 'idle'
        self.current_image = self.idle_frames_left[0]
        self.speed = 10
        self.health = 3
        self.attack_rect = pygame.Rect(0, 0, 0, 0)
        self.is_attacking = False
        self.attack_damage = 1
        self.attack_duration = 200
        self.attack_start_time = 0
        self.damage_cooldown = 0
        self.damage_cooldown_max = 60  # Frames between damage hits

    def take_damage(self, damage):
        if self.damage_cooldown <= 0:
            self.health -= damage
            self.damage_cooldown = self.damage_cooldown_max

    def attack(self):
        if not self.is_attacking:
            self.click = True
            self.state = 'attacking'
            self.is_attacking = True
            self.current_frame = 0
            self.last_updated = pygame.time.get_ticks()
            self.attack_start_time = self.last_updated
            if self.FACING_LEFT:
                self.current_image = self.attack_frames_left[self.current_frame]
            else:
                self.current_image = self.attack_frames_right[self.current_frame]
            self.update_attack_rect()


    def update(self):
        # Don't update if dead
        if self.state == 'dead':
            self.animate()
            return
        
        # Update damage cooldown
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1
        
        # Handle attack state management
        if self.state == 'attacking':
            now = pygame.time.get_ticks()
            if now - self.last_updated > 2:
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.attack_frames_left)
                if self.FACING_LEFT:
                    self.current_image = self.attack_frames_left[self.current_frame]
                else:
                    self.current_image = self.attack_frames_right[self.current_frame]
            if now - self.attack_start_time >= self.attack_duration:
                self.click = False
                self.state = 'idle'
                self.current_frame = 0
                self.is_attacking = False

        self.velocity = 0
        self.height = 0
        if self.KEY_a:
            self.velocity = -2
        elif self.KEY_d:
            self.velocity = 2
        elif self.KEY_w:
            self.height = -2
        elif self.KEY_s:
            self.height = 2
        self.rect.x += self.velocity
        self.rect.y += self.height
        if not self.is_attacking:
            self.set_state()
        self.animate()
        self.update_attack_rect()



    def set_state(self):
        self.state = 'idle'
        if self.velocity > 0:
            self.state = 'moving right'
        elif self.velocity < 0:
            self.state = 'moving left'
        elif self.height > 0:
            self.state = 'moving up'
        elif self.height < 0:
            self.state = 'moving down'

    def draw(self, display):
        display.blit(self.current_image, self.rect)



    def animate(self):
        if self.state == 'attacking':
            return
        
        if self.state == 'dead':
            if self.FACING_LEFT:
                self.current_image = self.death_frames_left[0]
            else:
                self.current_image = self.death_frames_right[0]
            return

        now = pygame.time.get_ticks()
        if self.state == 'idle':
            if now - self.last_updated > 200:
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames_left)
                if self.FACING_LEFT:
                    self.current_image = self.idle_frames_left[self.current_frame]
                elif not self.FACING_LEFT:
                    self.current_image = self.idle_frames_right[self.current_frame]
        else:
            if now - self.last_updated > 200:
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_left)
                if self.state == 'moving left':
                    self.current_image = self.walking_frames_left[self.current_frame]
                elif self.state == 'moving right':
                    self.current_image = self.walking_frames_right[self.current_frame]
                elif self.state == 'moving up':
                    if self.FACING_LEFT:
                        self.current_image = self.walking_frames_left[self.current_frame]
                    elif not self.FACING_LEFT:
                        self.current_image = self.walking_frames_right[self.current_frame]
                elif self.state == 'moving down':
                    if self.FACING_LEFT:
                        self.current_image = self.walking_frames_left[self.current_frame]
                    elif not self.FACING_LEFT:
                        self.current_image = self.walking_frames_right[self.current_frame]
    
    def update_attack_rect(self):
        """Update the attack hitbox based on player position and facing direction"""
        if self.is_attacking:
            # Create attack box extending from player
            attack_width = 100
            attack_height = 60
            if self.FACING_LEFT:
                # Attack to the left
                self.attack_rect = pygame.Rect(
                    self.rect.left - attack_width,
                    self.rect.centery - attack_height // 2,
                    attack_width,
                    attack_height
                )
            else:
                # Attack to the right
                self.attack_rect = pygame.Rect(
                    self.rect.right,
                    self.rect.centery - attack_height // 2,
                    attack_width,
                    attack_height
                )
        else:
            self.attack_rect = pygame.Rect(0, 0, 0, 0)

    def load_frames(self):
        my_spritesheet = Spritesheet('Funtimefoxy_sheet.png')
        self.idle_frames_left = [my_spritesheet.parse_sprite('01.png'), 
                                 my_spritesheet.parse_sprite('02.png')]
        self.walking_frames_left = [my_spritesheet.parse_sprite('03.png'), 
                                 my_spritesheet.parse_sprite('04.png')]
        self.attack_frames_left = [my_spritesheet.parse_sprite('06.png')]
        self.death_frames_left = [my_spritesheet.parse_sprite('08.png')]
        self.idle_frames_right = []
        self.walking_frames_right = []
        self.attack_frames_right = []
        self.death_frames_right = []

        for frame in self.idle_frames_left:
            self.idle_frames_right.append(pygame.transform.flip(frame, True, False))
        for frame in self.walking_frames_left:
            self.walking_frames_right.append(pygame.transform.flip(frame, True, False))
        for frame in self.attack_frames_left:
            self.attack_frames_right.append(pygame.transform.flip(frame, True, False))
        for frame in self.death_frames_left:
            self.death_frames_right.append(pygame.transform.flip(frame, True, False))

