import pygame

# 1. Setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
# Load your images using pygame.image.load()
backgrounds = [
    pygame.image.load("start_screen.png").convert(), 
    pygame.image.load("start_level.png").convert()
]
current_bg = 0
player = pygame.Rect(400, 300, 50, 50)

running = True
while running:
    # 2. Check for edge collision
    if player.right > 800:       # Reached Right Edge
        current_bg = (current_bg + 1) % len(backgrounds)
        player.left = 0          # Warp to left side
    elif player.left < 0:        # Reached Left Edge
        current_bg = (current_bg - 1) % len(backgrounds)
        player.right = 800       # Warp to right side

    # 3. Draw the current background
    screen.blit(backgrounds[current_bg], (0, 0))
    pygame.draw.rect(screen, (255, 0, 0), player)
    pygame.display.flip() # Update display