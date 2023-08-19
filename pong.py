import pygame

screen = pygame.display.set_mode((1200, 800))

keep_running = True
while keep_running:
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                print("Game quit")
                keep_running = False
    screen.fill((0, 0, 0))
    pygame.display.flip()
