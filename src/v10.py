import sys, pygame
import random
import math

pygame.init()
width = 480
height = 360
screen = pygame.display.set_mode((width, height))

class KeyController(object):
    def __init__(self):
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.z = False
        self.z_click = False
        self.r_click = False
        self.esc_click = False

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
            self.z = True
        elif key == pygame.K_r:
            self.r_click = True
        elif key == pygame.K_ESCAPE:
            self.esc_click = True

    def keyUp(self, key):
        if key == pygame.K_UP:
            self.up = False
        elif key == pygame.K_DOWN:
            self.down = False
        elif key == pygame.K_LEFT:
            self.left = False
        elif key == pygame.K_RIGHT:
            self.right = False
        elif key == pygame.K_z:
            self.z = False

    def update(self):
        self.z_click = False
        self.r_click = False
        self.esc_click = False


""" START REGION - GAME OBJECT CLASSES """

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
        x = int(self.x)
        y = int(self.y)
        pygame.draw.circle(screen, self.color, (x, y), self.radius)


class Enemy(object):
    def __init__(self, y):
        global width, frame
        self.x = width
        self.y = y
        self.vx = -2
        self.vy = 0
        self.active = True
        self.color = (0,96,191)
        self.radius = 15
        self.hp = 30
        self.bulletSpeed = 2
        self.cannonAngle = random.random()*2*math.pi
        self.cannonTurnRate = 0.07
        self.cannonFireInterval = 14
        self.spawnFrame = frame % self.cannonFireInterval

    def update(self):
        if not self.active: return

        self.randomlyChangeCourse()

        global width, height
        self.x += self.vx
        self.y += self.vy

        self.shoot()

        if self.x+self.radius < 0:
            self.remove()

        self.checkCollision()

    def randomlyChangeCourse(self):
        global width, height
        if random.random() < 0.005:
            if self.y > height*0.75:
                self.vy = -random.random()
            elif self.y < height*0.25:
                self.vy = random.random()
            else:
                self.vy = random.random()*2-1

    def shoot(self):
        global frame
        self.cannonAngle += self.cannonTurnRate
        if frame % self.cannonFireInterval == self.spawnFrame:
            self.fireAt(self.cannonAngle)


    def fireAt(self, angle):
        vx = self.bulletSpeed*math.cos(angle) + 0.5*self.vx
        vy = self.bulletSpeed*math.sin(angle) + 0.5*self.vy

        spawnEnemyBullet(self.x, self.y, vx, vy)


    def checkCollision(self):
        global bullets
        for bullet in bullets:
            if bullet.active and self.collideWith(bullet):
                bullet.remove()
                self.takeDamage(2)
                return

    def takeDamage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.killed()

    def collideWith(self, bullet):
        dx = self.x - bullet.x
        dy = self.y - bullet.y
        dist = self.radius + bullet.radius
        return dx*dx + dy*dy <= dist*dist

    def killed(self):
        global score
        score += 1
        self.remove()
        print('Score: ' + str(score))

    def remove(self):
        self.active = False

    def draw(self):
        if not self.active: return
        pygame.draw.rect(screen, self.color,
                            (self.x-self.radius, self.y-self.radius,
                            2*self.radius, 2*self.radius))


class Player(object):
    def __init__(self):
        self.x = 50
        self.y = 50
        self.vx = 0
        self.vy = 0
        self.speed = 5
        self.color = (255, 224, 127)
        self.redcolor = (255, 0, 0)
        self.radius = 5
        self.drawRadius = 15
        self.active = True
        self.fireRate = 5
        self.startFireFrame = -1

    def update(self):
        if not self.active: return

        global keyController
        self.move(keyController)
        self.shoot(keyController)
        self.checkCollision()

    def checkCollision(self):
        global enemies, enemyBullets
        for enemy in enemies:
            if enemy.active and self.collideWith(enemy):
                enemy.remove()
                self.remove()
                return
        for bullet in enemyBullets:
            if bullet.active and self.collideWith(bullet):
                bullet.remove()
                self.remove()
                return

    def collideWith(self, obj):
        dx = self.x - obj.x
        dy = self.y - obj.y
        dist = self.radius + obj.radius
        return dx*dx + dy*dy <= dist*dist

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
        global frame
        if keyController.z_click:
            self.startFireFrame = frame % self.fireRate
        if keyController.z and frame % self.fireRate == self.startFireFrame:
            spawnBullet(self.x, self.y+5, 15, 1.5)
            spawnBullet(self.x, self.y, 15, 0)
            spawnBullet(self.x, self.y-5, 15, -1.5)

    def draw(self):
        if not self.active: return

        global screen
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.drawRadius)
        pygame.draw.circle(screen, self.redcolor, (self.x, self.y), self.radius)

    def remove(self):
        self.active = False

""" END REGION - GAME OBJECT CLASSES """

def initialise():
    global player, keyController, bullets, enemyBullets, enemies, frame, score
    frame = 0
    score = 0
    player = Player()
    keyController = KeyController()
    bullets = []
    enemies = []
    enemyBullets = []

# spawns a new bullet at the specified location with a specified velocity
def spawnBullet(x, y, vx, vy):
    global bullets
    bullet = Bullet(x, y, vx, vy)
    bullets.append(bullet)

# spawns an enemy bullet. Enemy bullets can kill the player.
def spawnEnemyBullet(x, y, vx, vy):
    global enemyBullets
    bullet = Bullet(x, y, vx, vy)
    enemyBullets.append(bullet)

# spawns a new enemey at the specified location.
def spawnEnemy(y):
    global enemies
    enemy = Enemy(y)
    enemies.append(enemy)

# Remove all inactive items from the array periodically.
def maybeCleanUpArrays():
    global bullets, enemies, enemyBullets
    if len(bullets) > 50:
        bullets = list(filter(lambda obj : obj.active, bullets))
    if len(enemies) > 30:
        enemies = list(filter(lambda obj : obj.active, enemies))
    if len(enemyBullets) > 80:
        enemyBullets = list(filter(lambda obj : obj.active, enemyBullets))


""" START REGION - CORE FUNCTIONS """

# Update function
# ALL game logic should go here.
def update():
    global player, bullets, enemyBullets, enemies, keyController, frame, height
    
    player.update()
    for bullet in bullets:
        bullet.update()
    for bullet in enemyBullets:
        bullet.update()
    for enemy in enemies:
        enemy.update()

    if frame % 50 == 0:
        spawnEnemy(random.randrange(30,height-30))

    maybeCleanUpArrays()
    frame += 1

    if keyController.r_click:
        initialise()
    if keyController.esc_click:
        sys.exit()

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
    global player, bullets, enemyBullets, enemies
    screen.fill((0,0,0))

    player.draw()
    for bullet in bullets:
        bullet.draw()
    for bullet in enemyBullets:
        bullet.draw()
    for enemy in enemies:
        enemy.draw()
    
    pygame.display.flip()

""" END REGION - CORE FUNCTIONS """

initialise()
while True:
    #things to run every frame
    eventRead()
    update()
    draw()
    pygame.time.delay(20)
