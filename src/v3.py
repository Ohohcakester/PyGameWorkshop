import sys, pygame

pygame.init()
screen = pygame.display.set_mode((480, 360))

playerX = 50
playerY = 50

# Update function
# ALL game logic should go here.
def update():
    global playerX, playerY
    playerX += 2
    playerY += 1

# Event read function
# Keyboard / Mouse input is read here.
# Minimal game logic should be here..
def eventRead():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()

# Draw function
# All drawing functions should be placed here.
# NO game logic should be here.
def draw():
    global playerX, playerY
    screen.fill((0,0,0))
    
    pygame.draw.circle(screen, (255, 0, 0), (playerX, playerY), 15)
    
    pygame.display.flip()


while True:
    #things to run every frame
    eventRead()
    update()
    draw()
    pygame.time.delay(20)