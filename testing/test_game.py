import pygame
from player import Player
from spritesheet import Spritesheet




pygame.init()
DISPLAY_W, DISPLAY_H = pygame.display.Info().current_w, pygame.display.Info().current_h
canvas = pygame.Surface((DISPLAY_W,DISPLAY_H))
screen = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
running = True
clock = pygame.time.Clock()
enemies = []
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

fox = Player()

while running:
    clock.tick(140)
    if check_edge == True:
         pass
    elif fox.rect.right > DISPLAY_W and check_edge == False:
        current_background = (current_background + 1) % len(new_backgrounds)
        fox.rect.left = 0
        check_edge = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
                fox.KEY_a, fox.FACING_LEFT = True, True
        elif keys[pygame.K_d]:
                fox.KEY_d, fox.FACING_LEFT = True, False
        elif keys[pygame.K_w]:
                fox.KEY_w = True
        elif keys[pygame.K_s]:
                fox.KEY_s = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                fox.KEY_a = False
            elif event.key == pygame.K_d:
                fox.KEY_d = False
            elif event.key == pygame.K_w:
                fox.KEY_w = False
            elif event.key == pygame.K_s:
                fox.KEY_s = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            fox.attack()
    screen.fill((0,0,0))


    canvas.blit(new_backgrounds[current_background], (0,0))
    screen.blit(new_backgrounds[current_background], (0,0))
    fox.update()
    fox.draw(screen)
    pygame.display.flip()

