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
game_started = False
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
        game_started = True
    
    # Spawn enemies when the level is active
    if game_started and not game_over:
        enemy_spawn_timer += 1
        if enemy_spawn_timer >= enemy_spawn_interval and len(enemies) < max_enemies:
            temp_enemy = Enemy(player, 0, 0, DISPLAY_W, DISPLAY_H)
            enemy_full_w, enemy_full_h = temp_enemy.rect.size
            enemy_collision = temp_enemy.get_collision_rect()
            enemy_collision_w, enemy_collision_h = enemy_collision.size
            enemy_collision_offset_x = (enemy_full_w - enemy_collision_w) // 2
            enemy_collision_offset_y = (enemy_full_h - enemy_collision_h) // 2
            del temp_enemy
            player_collision = player.get_collision_rect()
            min_distance = 300
            spawn_x = None
            spawn_y = None
            for _ in range(100):
                candidate_x = random.randint(0, DISPLAY_W - enemy_full_w)
                candidate_y = random.randint(0, DISPLAY_H - enemy_full_h)
                candidate_collision = pygame.Rect(
                    candidate_x + enemy_collision_offset_x,
                    candidate_y + enemy_collision_offset_y,
                    enemy_collision_w,
                    enemy_collision_h
                )
                dist = ((candidate_collision.centerx - player_collision.centerx) ** 2 + (candidate_collision.centery - player_collision.centery) ** 2) ** 0.5
                if dist >= min_distance and not candidate_collision.colliderect(player_collision):
                    spawn_x = candidate_x
                    spawn_y = candidate_y
                    break
            if spawn_x is None:
                # fallback to any position that doesn't overlap the player's collision box
                for _ in range(50):
                    candidate_x = random.randint(0, DISPLAY_W - enemy_full_w)
                    candidate_y = random.randint(0, DISPLAY_H - enemy_full_h)
                    candidate_collision = pygame.Rect(
                        candidate_x + enemy_collision_offset_x,
                        candidate_y + enemy_collision_offset_y,
                        enemy_collision_w,
                        enemy_collision_h
                    )
                    if not candidate_collision.colliderect(player_collision):
                        spawn_x = candidate_x
                        spawn_y = candidate_y
                        break
            if spawn_x is None:
                spawn_x = random.randint(0, DISPLAY_W - enemy_full_w)
                spawn_y = random.randint(0, DISPLAY_H - enemy_full_h)
            new_enemy = Enemy(player, spawn_x, spawn_y, DISPLAY_W, DISPLAY_H)
            enemies.add(new_enemy)
            enemy_spawn_timer = 0
    
    # Handle events and input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_r:
                game_over = False
                game_started = True
                current_background = 1
                check_edge = True
                enemy_spawn_timer = 0
                enemies.empty()
                player.health = 3
                player.state = 'idle'
                player.current_frame = 0
                player.last_updated = pygame.time.get_ticks()
                player.is_attacking = False
                player.click = False
                player.attack_rect = pygame.Rect(0, 0, 0, 0)
                player.KEY_a = player.KEY_w = player.KEY_s = player.KEY_d = False
                player.FACING_LEFT = False
                player.current_image = player.idle_frames_right[0]
                player.rect.left = 0

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
            if player.attack_rect.colliderect(enemy.get_collision_rect()):
                enemy_offset = enemy.rect.centerx - player.rect.centerx
                enemy_same_side = (enemy_offset > 0 and not player.FACING_LEFT) or (enemy_offset < 0 and player.FACING_LEFT)
                vertical_overlap = abs(enemy.rect.centery - player.rect.centery) < 30
                if enemy_same_side and vertical_overlap:
                    enemy.take_damage(player.attack_damage)
    
    # Check collision between enemies and player (enemy damages player)
    if game_started:
        for enemy in list(enemies):
            if enemy.get_collision_rect().colliderect(player.get_collision_rect()):
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
    if game_started:
        health_bar_num = max(1, 4 - player.health)
        if health_bar_num in health_bars:
            screen.blit(health_bars[health_bar_num], (10, 10))
    
    player.draw(screen)
    
    # Draw remaining enemies
    enemies.draw(screen)
    
    pygame.display.flip()


