import pygame
from spritesheet import Spritesheet

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.KEY_a ,self.KEY_w, self.KEY_s, self.KEY_d, self.FACING_LEFT ,self.click =False, False, False, False, False, False
        self.load_frames()
        self.rect = self.idle_frames_left[0].get_rect()
        self.rect.midbottom = (240, 300)
        self.current_frame = 0
        self.last_updated = 0
        self.velocity = 0
        self.state = 'idle'
        self.current_image = self.idle_frames_left[0]

    def attack(self):
        self.click = True
        if self.click:
            self.state = 'attacking'
        if self.state == 'attacking':
            now = pygame.time.get_ticks()
            if now - self.last_updated > 10:
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.attack_frames_left)
                if self.FACING_LEFT:
                    self.current_image = self.attack_frames_left[self.current_frame]
                elif not self.FACING_LEFT:
                    self.current_image = self.attack_frames_right[self.current_frame]
            if self.current_frame == len(self.attack_frames_left) - 1:
                self.click = False
                self.state = 'idle'
                self.current_frame = 0


    def update(self):
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
        self.set_state()
        self.animate()


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

