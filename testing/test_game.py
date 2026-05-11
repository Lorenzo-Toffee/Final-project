import pygame
from player import Player




pygame.init()
DISPLAY_W, DISPLAY_H = 500, 400
canvas = pygame.Surface((DISPLAY_W,DISPLAY_H))
screen = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
running = True
clock = pygame.time.Clock()
menu = pygame.image.load('start_screen.png').convert()
scaled_menu = pygame.transform.scale(menu, (DISPLAY_W, DISPLAY_H))

fox = Player()

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                fox.KEY_a, fox.FACING_LEFT = True, True
            elif event.key == pygame.K_d:
                fox.KEY_d, fox.FACING_LEFT = True, False
            elif event.key == pygame.K_w:
                fox.KEY_w = True
            elif event.key == pygame.K_s:
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


    fox.update()

    canvas.blit(scaled_menu, (0,0))
    fox.draw(canvas)
    screen.blit(canvas, (0,0))
    pygame.display.update()
