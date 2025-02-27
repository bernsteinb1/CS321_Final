import pygame
import random

GRAVITY = 5
GAP_SIZE = 140
PIPE_SCROLL_SPEED = 2
FLAP_STRENGTH = 35

# make bird class
class Bird:
    def __init__(self):
        self.velocity = 0
        self.x_coord = 0
        self.y_coord = 0
        self.distance_from_pipe = 0
        self.color = (249, 220, 53)
        self.radius = 25
        # prob not great for bird to keep track of score, but it works
        self.score = 0
        # need to track total distance bird has travelled

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x_coord, self.y_coord), self.radius)

    def flap(self):
        bird.velocity += FLAP_STRENGTH

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
        self.cleared = False

    def randomize_gap(self, height):
        self.gap = random.randrange(0, height - GAP_SIZE)
        self.bot_rect_top = self.gap + GAP_SIZE
        self.top_rect_height = self.gap
        self.bot_rect_height = height - self.gap + GAP_SIZE

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.left, self.top_rect_top, self.width, self.top_rect_height))
        pygame.draw.rect(window, self.color, (self.left, self.bot_rect_top, self.width, self.bot_rect_height))

# returns False if the bird hits the bottom of the screen, True otherwise
def update_bird(bird):
    bird.velocity -= GRAVITY
    if bird.velocity <= 0:
        bird.velocity = 0

    bird.y_coord += GRAVITY - bird.velocity

    if bird.y_coord < 0 + bird.radius:
        bird.y_coord = bird.radius

    if bird.y_coord >= h - bird.radius:
        return False
    
    return True

def update_pipes(pipe1, pipe2, height, width):
    # pipes are always 1 screen width apart
    pipe1.left -= PIPE_SCROLL_SPEED
    if pipe1.left < -pipe1.width:
        pipe1.randomize_gap(height)
        pipe1.left = pipe2.left + width
        pipe1.cleared = False

    pipe2.left -= PIPE_SCROLL_SPEED
    if pipe2.left < -pipe2.width:
        pipe2.randomize_gap(height)
        pipe2.left = pipe1.left + width
        pipe2.cleared = False

# returns true if the bird collides with either of the pipes
def check_collision(bird, pipe1, pipe2):
    # create a rectangle from the bird's circle
    bird_rect = pygame.Rect(bird.x_coord - bird.radius, bird.y_coord - bird.radius, bird.radius * 2, bird.radius * 2)

    # check if bird collides with pipe 1
    if bird_rect.colliderect(pygame.Rect(pipe1.left, pipe1.top_rect_top, pipe1.width, pipe1.top_rect_height)):
        return True
    
    if bird_rect.colliderect(pygame.Rect(pipe1.left, pipe1.bot_rect_top, pipe1.width, pipe1.bot_rect_height)):
        return True
    
    # check if bird collides with pipe2
    if bird_rect.colliderect(pygame.Rect(pipe2.left, pipe2.top_rect_top, pipe2.width, pipe2.top_rect_height)):
        return True
    
    if bird_rect.colliderect(pygame.Rect(pipe2.left, pipe2.bot_rect_top, pipe2.width, pipe2.bot_rect_height)):
        return True
    
    return False

# checks to see if the bird is halfway through a pipe. if it is, increases score by 1
def check_pipe_clear(bird, pipe1, pipe2):
    if bird.x_coord > pipe1.left + pipe1.width / 2:
        if pipe1.cleared == False:
            pipe1.cleared = True
            bird.score += 1
            print("Score:", bird.score)

    if bird.x_coord > pipe2.left + pipe2.width / 2:
        if pipe2.cleared == False:
            pipe2.cleared = True
            bird.score += 1
            print("Score:", bird.score)

# ------------- game code -------------
# setup window and basic game items
background_color = (5, 213, 250) 
window = pygame.display.set_mode((480, 640)) 
w, h = pygame.display.get_surface().get_size()
pygame.display.set_caption('Bryce & Ruben: Flappy Bird') 
clock = pygame.time.Clock()
running = True

# setup bird object
bird = Bird()

# set initial screen position of bird
bird.x_coord = w / 2 - 50
bird.y_coord = h / 2

# initialize 2 pipe objects, these will respawn as they reach end of screen
pipe1 = Pipe(w, h)
pipe2 = Pipe(w * 2, h)

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

    if not update_bird(bird):
        print("Game over: hit bottom")
        running = update_bird(bird)

    update_pipes(pipe1, pipe2, h, w)

    check_pipe_clear(bird, pipe1, pipe2)

    if check_collision(bird, pipe1, pipe2):
        print("Game over: hit pipe")
        running = False

    window.fill(background_color)
    pipe1.draw(window)
    pipe2.draw(window)
    bird.draw(window)
    pygame.display.update()