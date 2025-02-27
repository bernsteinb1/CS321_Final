import pygame
import random

GRAVITY = 2
GAP_SIZE = 180
PIPE_SCROLL_SPEED = 2
FLAP_STRENGTH = 20
MAX_TERMINAL_VELOCITY = -8
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
        self.radius = 25
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
        self.gap = random.randrange(0, WINDOW_HEIGHT - GAP_SIZE)
        self.color = (75, 174, 78)
        # Rect class parameters
        self.x_coord = x_coord
        self.top_rect_top = 0
        self.bot_rect_top = self.gap + GAP_SIZE
        self.width = 85
        self.top_rect_height = self.gap
        self.bot_rect_height = WINDOW_HEIGHT - self.gap + GAP_SIZE   
        self.cleared = False

    def randomize_gap(self, height):
        self.gap = random.randrange(0, height - GAP_SIZE)
        self.bot_rect_top = self.gap + GAP_SIZE
        self.top_rect_height = self.gap
        self.bot_rect_height = height - self.gap + GAP_SIZE

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x_coord, self.top_rect_top, self.width, self.top_rect_height))
        pygame.draw.rect(window, self.color, (self.x_coord, self.bot_rect_top, self.width, self.bot_rect_height))

def update_pipes(pipe1, pipe2):
    # pipes are always 1 screen width apart
    pipe1.x_coord -= PIPE_SCROLL_SPEED
    if pipe1.x_coord < -pipe1.width:
        pipe1.randomize_gap(WINDOW_HEIGHT)
        pipe1.x_coord = pipe2.x_coord + WINDOW_WIDTH
        pipe1.cleared = False

    pipe2.x_coord -= PIPE_SCROLL_SPEED
    if pipe2.x_coord < -pipe2.width:
        pipe2.randomize_gap(WINDOW_HEIGHT)
        pipe2.x_coord = pipe1.x_coord + WINDOW_WIDTH
        pipe2.cleared = False

# returns true if the bird collides with either of the pipes
def check_collision(bird, pipe1, pipe2):
    # create a rectangle from the bird's circle
    bird_rect = pygame.Rect(bird.x_coord - bird.radius, bird.y_coord - bird.radius, bird.radius * 2, bird.radius * 2)

    # check if bird collides with pipe 1
    if bird_rect.colliderect(pygame.Rect(pipe1.x_coord, pipe1.top_rect_top, pipe1.width, pipe1.top_rect_height)):
        return True
    
    if bird_rect.colliderect(pygame.Rect(pipe1.x_coord, pipe1.bot_rect_top, pipe1.width, pipe1.bot_rect_height)):
        return True
    
    # check if bird collides with pipe2
    if bird_rect.colliderect(pygame.Rect(pipe2.x_coord, pipe2.top_rect_top, pipe2.width, pipe2.top_rect_height)):
        return True
    
    if bird_rect.colliderect(pygame.Rect(pipe2.x_coord, pipe2.bot_rect_top, pipe2.width, pipe2.bot_rect_height)):
        return True
    
    return False

# checks to see if the bird is halfway through a pipe. if it is, increases score by 1
def check_pipe_clear(bird, pipe1, pipe2):
    if bird.x_coord > pipe1.x_coord + pipe1.width:
        if pipe1.cleared == False:
            pipe1.cleared = True
            bird.score += 1
            print("Score:", bird.score)

    if bird.x_coord > pipe2.x_coord + pipe2.width:
        if pipe2.cleared == False:
            pipe2.cleared = True
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

# initialize 2 pipe objects, these will respawn as they reach end of screen
pipe1 = Pipe(WINDOW_WIDTH)
pipe2 = Pipe(WINDOW_WIDTH * 2)

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
                # not sure if quit is appropriate to use, cant use running bc update_bird also modifies it
                print("Player quit game")
                pygame.quit()

    if not bird.update():
        print("Game over: hit bottom")
        running = False

    update_pipes(pipe1, pipe2)

    check_pipe_clear(bird, pipe1, pipe2)

    if check_collision(bird, pipe1, pipe2):
        print("Game over: hit pipe")
        running = False

    window.fill(background_color)
    pipe1.draw(window)
    pipe2.draw(window)
    bird.draw(window)
    pygame.display.update()

print("Final score:", bird.score)