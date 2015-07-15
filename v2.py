import sys, pygame

pygame.init()
screen = pygame.display.set_mode((480, 360))

def eventRead():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


def update():
    pass

def draw():
    screen.fill((0,0,0))
    
    pygame.draw.circle(screen, (255, 0, 0), (50, 50), 15)
    
    pygame.display.flip()
            
            
while True:
    eventRead()
    update()
    draw()

    pygame.time.delay(20)