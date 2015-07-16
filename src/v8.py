import sys, pygame

pygame.init()
width = 480
height = 360
screen = pygame.display.set_mode((width, height))

class Bullet(object):
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.active = True
        self.color = (0,255,255)
        self.radius = 5

    def update(self):
        if not self.active: return

        global width, height
        self.x += self.vx
        self.y += self.vy

        if self.x > width or self.x < 0 or \
            self.y > height or self.y < 0:
            self.remove()

    def remove(self):
        self.active = False

    def draw(self):
        if not self.active: return
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


class KeyController(object):
    def __init__(self):
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.z_click = False

    def keyDown(self, key):
        if key == pygame.K_UP:
            self.up = True
        elif key == pygame.K_DOWN:
            self.down = True
        elif key == pygame.K_LEFT:
            self.left = True
        elif key == pygame.K_RIGHT:
            self.right = True
        elif key == pygame.K_z:
            self.z_click = True

    def keyUp(self, key):
        if key == pygame.K_UP:
            self.up = False
        elif key == pygame.K_DOWN:
            self.down = False
        elif key == pygame.K_LEFT:
            self.left = False
        elif key == pygame.K_RIGHT:
            self.right = False

    def update(self):
        self.z_click = False


class Player(object):
    def __init__(self):
        self.x = 50
        self.y = 50
        self.vx = 0
        self.vy = 0
        self.speed = 5
        self.color = (255, 0, 0)
        self.radius = 15

    def update(self):
        global keyController
        self.move(keyController)
        self.shoot(keyController)

    def move(self, keyController):
        self.vx = 0
        self.vy = 0
        if keyController.up:
            self.vy -= self.speed
        if keyController.down:
            self.vy += self.speed
        if keyController.left:
            self.vx -= self.speed
        if keyController.right:
            self.vx += self.speed

        self.x += self.vx
        self.y += self.vy

        if self.x > width:
            self.x = width
        if self.x < 0:
            self.x = 0
        if self.y > height:
            self.y = height
        if self.y < 0:
            self.y = 0

    def shoot(self, keyController):
        if keyController.z_click:
            spawnBullet(self.x, self.y, 10, 0)

    def draw(self):
        global screen
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

player = Player()
keyController = KeyController()
bullets = []


def spawnBullet(x, y, vx, vy):
    global bullets
    bullet = Bullet(x, y, vx, vy)
    bullets.append(bullet)


""" START REGION - CORE FUNCTIONS """

# Update function
# ALL game logic should go here.
def update():
    global player, bullets, keyController
    player.update()
    for bullet in bullets:
        bullet.update()

    keyController.update()

# Event read function
# Keyboard / Mouse input is read here.
# Minimal game logic should be here..
def eventRead():
    global keyController

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            keyController.keyDown(event.key)
        elif event.type == pygame.KEYUP:
            keyController.keyUp(event.key)

# Draw function
# All drawing functions should be placed here.
# NO game logic should be here.
def draw():
    global player
    screen.fill((0,0,0))
    
    player.draw()
    for bullet in bullets:
        bullet.draw()
    
    pygame.display.flip()

""" END REGION - CORE FUNCTIONS """

while True:
    #things to run every frame
    eventRead()
    update()
    draw()
    pygame.time.delay(20)
