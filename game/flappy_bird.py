import pygame
import random
import math

GRAVITY = 2
GAP_SIZE = 180
PIPE_SCROLL_SPEED = 2
FLAP_STRENGTH = 20
BIRD_RADIUS = 25
MAX_TERMINAL_VELOCITY = -8
DISTANCE_BETWEEN_PIPES = 250
PIPE_WIDTH = 85
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 640

# make bird class
class Bird:
    def __init__(self):
        self.velocity = 0
        self.x_coord = 0
        self.y_coord = 0
        # i dont use dist from pipe, bryce wants it for NN
        self.distance_from_pipe = 0
        self.color = (249, 220, 53)
        self.radius = BIRD_RADIUS
        # prob not great for bird to keep track of score, but it works
        self.score = 0

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x_coord, self.y_coord), self.radius)

    # each flap increase the bird's velocity, which is used to set y coordinate
    def flap(self):
        self.velocity = FLAP_STRENGTH

    # returns False if the bird hits the bottom of the screen, True otherwise
    def update(self):
        self.velocity -= GRAVITY
        self.velocity = max(self.velocity, MAX_TERMINAL_VELOCITY)

        self.y_coord -= self.velocity

        if self.y_coord < 0 + self.radius:
            self.y_coord = self.radius

        if self.y_coord >= WINDOW_HEIGHT - self.radius:
            return False
        
        return True

class Pipe:
    def __init__(self, x_coord):
        # a pipe is 2 rectangles split to create a gap, but treated as 1 pair
        self.gap = random.randrange(5, WINDOW_HEIGHT - GAP_SIZE - 5) # 5 px buffer to ensure that gaps are not right at edges of screen
        self.color = (75, 174, 78)
        # Rect class parameters
        self.x_coord = x_coord
        self.top_rect_top = 0
        self.bot_rect_top = self.gap + GAP_SIZE
        self.width = PIPE_WIDTH
        self.top_rect_height = self.gap
        self.bot_rect_height = WINDOW_HEIGHT - self.gap + GAP_SIZE   
        self.cleared = False

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x_coord, self.top_rect_top, self.width, self.top_rect_height))
        pygame.draw.rect(window, self.color, (self.x_coord, self.bot_rect_top, self.width, self.bot_rect_height))

    def update(self):
        self.x_coord -= PIPE_SCROLL_SPEED

# returns true if the bird collides with the given pipe
def check_collision(bird, pipe):
    # create a rectangle from the bird's circle
    bird_rect = pygame.Rect(bird.x_coord - bird.radius, bird.y_coord - bird.radius, bird.radius * 2, bird.radius * 2)

    # check if bird collides with the pipe 
    if bird_rect.colliderect(pygame.Rect(pipe.x_coord, pipe.top_rect_top, pipe.width, pipe.top_rect_height)):
        return True
    
    if bird_rect.colliderect(pygame.Rect(pipe.x_coord, pipe.bot_rect_top, pipe.width, pipe.bot_rect_height)):
        return True
    
    return False

# checks to see if the bird is at the end of a pipe. if it is, increases score by 1
def check_pipe_clear(bird, pipe):
    if bird.x_coord > pipe.x_coord + pipe.width:
        if pipe.cleared == False:
            pipe.cleared = True
            bird.score += 1
            print("Score:", bird.score)

# ------------- game code -------------
# setup window and basic game items
background_color = (5, 213, 250) 
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) 
pygame.display.set_caption('Bryce & Ruben: Flappy Bird') 
clock = pygame.time.Clock()
running = True

# setup bird object
bird = Bird()

# set initial screen position of bird
bird.x_coord = WINDOW_WIDTH / 2 - 50
bird.y_coord = WINDOW_HEIGHT / 2

# spawn initial pipes
num_pipes = math.ceil(WINDOW_WIDTH / (DISTANCE_BETWEEN_PIPES + PIPE_WIDTH)) + 1
offset = DISTANCE_BETWEEN_PIPES + PIPE_WIDTH
pipes = [Pipe(i * offset + WINDOW_WIDTH) for i in range(num_pipes)]

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
    
    closest_pipe = pipes[0] # first pipe in array is the pipe closest to bird
    if closest_pipe.x_coord < -closest_pipe.width:
        pipes.remove(closest_pipe)
        pipes.append(Pipe(pipes[-1].x_coord + offset)) # replace any deleted pipe
        closest_pipe = pipes[0]

    check_pipe_clear(bird, closest_pipe)

    if check_collision(bird, closest_pipe):
        print("Game over: hit pipe")
        running = False

    window.fill(background_color)
    for pipe in pipes:
        pipe.draw(window)
    bird.draw(window)
    pygame.display.update()

print("Final score:", bird.score)