import pygame
import random

GRAVITY = 5
GAP_SIZE = 120
PIPE_SCROLL_SPEED = 1.5

# make bird class
class Bird:
    def __init__(self):
        self.velocity = 0
        self.x_coord = 0
        self.y_coord = 0
        self.distance_from_pipe = 0
        self.color = (249, 220, 53)
        self.radius = 25
        # i forgot one of the variables we talked about

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x_coord, self.y_coord), self.radius)

    def flap(self):
        bird.velocity += 35

# # make obstacle class constructor 
class Pipe:
    def __init__(self, left, height):
        # self.gap = some random choice for gap location
        self.color = (75, 174, 78)
        # Rect class parameters
        self.left = left
        self.top = 0
        self.width = 85
        self.height = height

    def draw(self, window, window_height):
        pygame.draw.rect(window, self.color, (self.left, self.top, self.width, window_height))
        # still need to cut out the gap

# ------------- game code -------------
# setup window and basic game items
background_color = (5, 213, 250) 
window = pygame.display.set_mode((480, 640)) 

pygame.display.set_caption('Bryce & Ruben: Flappy Bird') 

clock = pygame.time.Clock()
  
running = True

# setup bird object
bird = Bird()

# set initial screen position of bird
w, h = pygame.display.get_surface().get_size()
bird.x_coord = w / 2 - 50
bird.y_coord = h / 2

# initialize a single pipe object, will need to create more within while loop
pipe = Pipe(w, h)

# game loop 
while running: 
    # set FPS to 60
    clock.tick(60)  
    # https://stackoverflow.com/questions/35617246/setting-a-fixed-fps-in-pygame-python-3
    # might want to look at this ^ later
    
# for loop through the event queue   
    for event in pygame.event.get(): 
      
        if event.type == pygame.QUIT: 
            running = False

        # flap with space, quit with q
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.flap()
            elif event.key == pygame.K_q:
                running = False

    # update bird position
    bird.velocity -= GRAVITY
    if bird.velocity <= 0:
        bird.velocity = 0

    bird.y_coord += GRAVITY - bird.velocity

    if bird.y_coord < 0 + bird.radius:
        bird.y_coord = bird.radius

    if bird.y_coord >= h - bird.radius:
        running = False

    # update pipe position
    pipe.left -= PIPE_SCROLL_SPEED

    window.fill(background_color)
    bird.draw(window)
    pipe.draw(window, h)
    pygame.display.update()