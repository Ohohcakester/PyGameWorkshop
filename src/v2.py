import sys, pygame

pygame.init()
screen = pygame.display.set_mode((480, 360))

def eventRead():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()

def draw():
    screen.fill((0,0,0))
    
    pygame.draw.circle(screen, (255, 0, 0), (50, 50), 15)
    
    pygame.display.flip()


while True:
    #things to run every frame
    eventRead()
    draw()
    pygame.time.delay(20)