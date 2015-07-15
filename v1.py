import sys, pygame

pygame.init()
screen = pygame.display.set_mode((480, 360))

def eventRead():
    events = pygame.event.get()

            
while True:
    #things to run every frame
    eventRead()
    pygame.time.delay(20)