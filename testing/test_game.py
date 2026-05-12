import pygame
from player import Player
from enemy import Enemy
from spritesheet import Spritesheet
import random
import os



pygame.init()

DISPLAY_W, DISPLAY_H = pygame.display.Info().current_w, pygame.display.Info().current_h
canvas = pygame.Surface((DISPLAY_W,DISPLAY_H))
screen = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))

running = True
game_over = False
clock = pygame.time.Clock()

# Load health bar images
health_bar_path = '../Healthbar_resized/'
health_bars = {}
for i in range(1, 5):
    health_bars[i] = pygame.image.load(os.path.join(health_bar_path, f'{i:02d}.png')).convert_alpha()


backgrounds = [
    pygame.image.load('start_screen.png').convert(),
    pygame.image.load('start_level.png').convert()
]
new_backgrounds = [
    pygame.transform.scale(backgrounds[0], (DISPLAY_W, DISPLAY_H)),
    pygame.transform.scale(backgrounds[1], (DISPLAY_W, DISPLAY_H))
]
current_background = 0
check_edge = False

# Enemy management
enemies = pygame.sprite.Group()
enemy_spawn_timer = 0
enemy_spawn_interval = 120  # Frames between enemy spawns (2 seconds at 60 FPS)
max_enemies = 5  # Maximum number of enemies on screen

player = Player()

while running:
    clock.tick(140)
    
    # Game start transition
    if check_edge == False and player.rect.right > DISPLAY_W:
        current_background = (current_background + 1) % len(new_backgrounds)
        player.rect.left = 0
        check_edge = True
    
    # Spawn enemies when game has started
    if check_edge == True and not game_over:
        enemy_spawn_timer += 1
        if enemy_spawn_timer >= enemy_spawn_interval and len(enemies) < max_enemies:
            # Spawn enemy at random position on screen
            spawn_x = random.randint(0, DISPLAY_W - 50)
            spawn_y = random.randint(0, DISPLAY_H - 50)
            new_enemy = Enemy(player, spawn_x, spawn_y, DISPLAY_W, DISPLAY_H)
            enemies.add(new_enemy)
            enemy_spawn_timer = 0
    
    # Handle events and input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                    player.KEY_a, player.FACING_LEFT = True, True
            elif keys[pygame.K_d]:
                    player.KEY_d, player.FACING_LEFT = True, False
            elif keys[pygame.K_w]:
                    player.KEY_w = True
            elif keys[pygame.K_s]:
                    player.KEY_s = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player.KEY_a = False
                elif event.key == pygame.K_d:
                    player.KEY_d = False
                elif event.key == pygame.K_w:
                    player.KEY_w = False
                elif event.key == pygame.K_s:
                    player.KEY_s = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.attack()
    
    # Update player
    player.update()
    
    # Update enemies
    enemies.update()
    
    # Check if player attack hits enemies
    if player.is_attacking:
        for enemy in list(enemies):
            if player.attack_rect.colliderect(enemy.rect):
                enemy.take_damage(player.attack_damage)
    
    # Check collision between enemies and player (enemy damages player)
    if check_edge == True:
        for enemy in list(enemies):
            if enemy.rect.colliderect(player.rect):
                player.take_damage(enemy.damage)
                enemy.take_damage(2)  # Kill the enemy on collision
    
    # Check if player is dead
    if player.health <= 0 and not game_over:
        game_over = True
        player.state = 'dead'
    
    # Draw everything
    canvas.blit(new_backgrounds[current_background], (0,0))
    screen.blit(new_backgrounds[current_background], (0,0))
    
    # Draw health bar at top (only after entering the game level)
    if check_edge == True:
        health_bar_num = max(1, 4 - player.health)
        if health_bar_num in health_bars:
            screen.blit(health_bars[health_bar_num], (10, 10))
    
    player.draw(screen)
    
    # Draw remaining enemies
    enemies.draw(screen)
    
    pygame.display.flip()


