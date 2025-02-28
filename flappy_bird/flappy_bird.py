import pygame
import random
import math

GRAVITY = .8  # how fast bird accelerates downward
GAP_SIZE = 180  # distance between the top and the bottom of a pipe
PIPE_SCROLL_SPEED = 2  # how fast pipes move towards bird
FLAP_STRENGTH = 13  # how much vertical velocity a flap adds
BIRD_RADIUS = 25  # bird radius
TERMINAL_VELOCITY = -10  # top downward velocity
DISTANCE_BETWEEN_PIPES = 250  # distance between pipes
PIPE_WIDTH = 85  # width of pipes
PIPE_BUFFER = 20  # minimum distance to pipe from top or bottom of screen
WINDOW_WIDTH = 480  # width of window
WINDOW_HEIGHT = 640  # height of window

BIRD_COLOR = (249, 220, 53)
PIPE_COLOR = (75, 174, 78)
BACKGROUND_COLOR = (5, 213, 250) 

# make bird class
class Bird:
    def __init__(self):
        self.velocity = 0
        self.x_coord = WINDOW_WIDTH / 2 - 50
        self.y_coord = WINDOW_HEIGHT / 2

    def draw(self, window):
        pygame.draw.circle(window, BIRD_COLOR, (self.x_coord, self.y_coord), BIRD_RADIUS)

    # each flap increase the bird's velocity, which is used to set y coordinate
    def flap(self):
        self.velocity = FLAP_STRENGTH

    # returns False if the bird hits the bottom of the screen, True otherwise
    def update(self):
        self.velocity = max(self.velocity - GRAVITY, TERMINAL_VELOCITY)  # don't let bird exceed terminal velocity
        self.y_coord = max(self.y_coord - self.velocity, BIRD_RADIUS)  # don't let bird hit top of screen
        return self.y_coord < WINDOW_HEIGHT - BIRD_RADIUS  # evaluates true if bird not touching bottom.

class Pipe:
    def __init__(self, x_coord):
        # a pipe is 2 rectangles split to create a gap, but treated as 1 pair
        self.gap = random.randrange(PIPE_BUFFER, WINDOW_HEIGHT - GAP_SIZE - PIPE_BUFFER) # PIPE_BUFFER ensures that gaps are not right at edges of screen
        # Rect class parameters
        self.x_coord = x_coord
        self.top_rect_top = 0
        self.bot_rect_top = self.gap + GAP_SIZE
        self.top_rect_height = self.gap
        self.bot_rect_height = WINDOW_HEIGHT - self.gap + GAP_SIZE   

    def draw(self, window):
        pygame.draw.rect(window, PIPE_COLOR, (self.x_coord, self.top_rect_top, PIPE_WIDTH, self.top_rect_height))
        pygame.draw.rect(window, PIPE_COLOR, (self.x_coord, self.bot_rect_top, PIPE_WIDTH, self.bot_rect_height))

    def update(self):
        self.x_coord -= PIPE_SCROLL_SPEED

# returns true if the bird collides with the given pipe
def check_collision(bird, pipe):
    # create a rectangle from the bird's circle
    bird_rect = pygame.Rect(bird.x_coord - BIRD_RADIUS, bird.y_coord - BIRD_RADIUS, BIRD_RADIUS * 2, BIRD_RADIUS * 2)

    # check if bird collides with the pipe 
    if bird_rect.colliderect(pygame.Rect(pipe.x_coord, pipe.top_rect_top, PIPE_WIDTH, pipe.top_rect_height)):
        return True
    if bird_rect.colliderect(pygame.Rect(pipe.x_coord, pipe.bot_rect_top, PIPE_WIDTH, pipe.bot_rect_height)):
        return True
    return False

# checks to see if the bird is at the end of a pipe. if it is, increases score by 1
def check_pipe_clear(bird, pipe):
    return bird.x_coord > pipe.x_coord + PIPE_WIDTH

# ------------- game code -------------
# setup window and basic game items
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) 
pygame.display.set_caption('Bryce & Ruben: Flappy Bird') 
clock = pygame.time.Clock()
running = True
score = 0

# setup bird object
bird = Bird()

# spawn initial pipes
num_pipes = math.ceil(WINDOW_WIDTH / (DISTANCE_BETWEEN_PIPES + PIPE_WIDTH)) + 1
offset = DISTANCE_BETWEEN_PIPES + PIPE_WIDTH
pipes = [Pipe(i * offset + WINDOW_WIDTH) for i in range(num_pipes)]

next_pipe = pipes[0]

# game loop 
while running: 
    # set FPS to 60
    clock.tick(60)  
    
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False

        # flap with space, quit with q
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.flap()
            elif event.key == pygame.K_q:
                print("Player quit game")
                running = False

    if not bird.update():
        print("Game over: hit bottom")
        running = False

    for pipe in pipes:
        pipe.update()
    
    if pipes[0].x_coord < -PIPE_WIDTH:
        pipes.pop(0)
        pipes.append(Pipe(pipes[-1].x_coord + offset)) # replace any deleted pipe

    if check_pipe_clear(bird, next_pipe):
        print("Score:", score)
        next_pipe = pipes[pipes.index(next_pipe) + 1]
        score += 1

    if check_collision(bird, next_pipe):
        print("Game over: hit pipe")
        running = False

    window.fill(BACKGROUND_COLOR)
    for pipe in pipes:
        pipe.draw(window)
    bird.draw(window)
    pygame.display.update()
    
print("Final score:", score)
