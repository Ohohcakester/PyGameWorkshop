import sys, pygame

pygame.init()
screen = pygame.display.set_mode((480, 360))

class Player(object):
    def __init__(self):
        self.x = 50
        self.y = 50
        self.vx = 2
        self.vy = 1
        self.color = (255, 0, 0)
        self.radius = 15

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def turnLeft(self):
        self.vx = -2

    def turnRight(self):
        self.vx = 2

    def draw(self):
        global screen
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

player = Player()

# Update function
# ALL game logic should go here.
def update():
    global player
    player.update()

# Event read function
# Keyboard / Mouse input is read here.
# Minimal game logic should be here..
def eventRead():
    global player

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.turnLeft()
            elif event.key == pygame.K_RIGHT:
                player.turnRight()

# Draw function
# All drawing functions should be placed here.
# NO game logic should be here.
def draw():
    global player
    screen.fill((0,0,0))
    
    player.draw()
    
    pygame.display.flip()


while True:
    #things to run every frame
    eventRead()
    update()
    draw()
    pygame.time.delay(20)