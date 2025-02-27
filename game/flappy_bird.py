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
        # need to track total distance bird has travelled

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x_coord, self.y_coord), self.radius)

    def flap(self):
        bird.velocity += 35

# # make obstacle class constructor 
class Pipe:
    def __init__(self, left, height):
        # a pipe is 2 rectangles split to create a gap, but treated as 1 pair
        self.gap = random.randrange(0, height - GAP_SIZE)
        self.color = (75, 174, 78)
        # Rect class parameters
        self.left = left
        self.top_rect_top = 0
        self.bot_rect_top = self.gap + GAP_SIZE
        self.width = 85
        self.top_rect_height = self.gap
        self.bot_rect_height = height - self.gap + GAP_SIZE   

    def randomize_gap(self, height):
        self.gap = random.randrange(0, height - GAP_SIZE)
        self.bot_rect_top = self.gap + GAP_SIZE
        self.top_rect_height = self.gap
        self.bot_rect_height = height - self.gap + GAP_SIZE

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.left, self.top_rect_top, self.width, self.top_rect_height))
        pygame.draw.rect(window, self.color, (self.left, self.bot_rect_top, self.width, self.bot_rect_height))

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

# initialize 2 pipe objects, these will respawn as they reach end of screen
pipe1 = Pipe(w, h)
pipe2 = Pipe(w * 2, h)

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
    # pipes are always 1 screen width apart
    pipe1.left -= PIPE_SCROLL_SPEED
    if pipe1.left < -pipe1.width:
        pipe1.randomize_gap(h)
        pipe1.left = pipe2.left + w

    pipe2.left -= PIPE_SCROLL_SPEED
    if pipe2.left < -pipe2.width:
        pipe2.randomize_gap(h)
        pipe2.left = pipe1.left + w

    window.fill(background_color)
    pipe1.draw(window)
    pipe2.draw(window)
    bird.draw(window)
    pygame.display.update()