import pygame
from spritesheet import Spritesheet




pygame.init()
DISPLAY_W, DISPLAY_H = 480, 300
canvas = pygame.Surface((DISPLAY_W,DISPLAY_H))
screen = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
running = True

my_spritesheet = Spritesheet('Funtimefoxy_sheet.png')
idle = [my_spritesheet.parse_sprite('01.png'),my_spritesheet.parse_sprite('02.png'),my_spritesheet.parse_sprite('03.png'),my_spritesheet.parse_sprite('04.png'),
        my_spritesheet.parse_sprite('05.png'),my_spritesheet.parse_sprite('06.png'),my_spritesheet.parse_sprite('07.png'),my_spritesheet.parse_sprite('08.png')]

index = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                index = (index + 1) % len(idle)

    canvas.fill((155,255,255))
    canvas.blit(idle[index], (0, DISPLAY_H - 200))
    screen.blit(canvas, (0,0))
    pygame.display.update()
