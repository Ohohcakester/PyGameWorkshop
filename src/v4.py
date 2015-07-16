import sys, pygame

pygame.init()
screen = pygame.display.set_mode((480, 360))

playerX = 50
playerY = 50
velocityX = 2
velocityY = 1

# Update function
# ALL game logic should go here.
def update():
    global playerX, playerY, velocityX, velocityY
    playerX += velocityX
    playerY += velocityY

# Event read function
# Keyboard / Mouse input is read here.
# Minimal game logic should be here..
def eventRead():
    global velocityX

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                velocityX = -2
            elif event.key == pygame.K_RIGHT:
                velocityX = 2

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