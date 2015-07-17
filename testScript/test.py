# If the test works, you should see a blue circle moving around the screen.
import pygame

pygame.init()
screen = pygame.display.set_mode((480,360))

x = 0
y = 0
while True:
    x = (x + 10) % 480
    y = (y + 10) % 360
    
    pygame.event.get()
    screen.fill((0,0,0))
    pygame.draw.circle(screen, (0, 127, 255), (x, y), 25)
    pygame.display.flip()
    pygame.time.delay(20)