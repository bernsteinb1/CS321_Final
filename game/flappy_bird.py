import pygame

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

    def flap(self):
        bird.velocity += 35

# make obstacle class constructor 

# ------------- game code -------------
# setup window and basic game items
background_color = (5, 213, 250) 
window = pygame.display.set_mode((480, 640)) 

pygame.display.set_caption('Bryce & Ruben: Flappy Bird') 
  
window.fill(background_color) 
  
pygame.display.update() 

clock = pygame.time.Clock()

gravity = 5
  
running = True

# setup bird object
bird = Bird()

# set screen position of bird
w, h = pygame.display.get_surface().get_size()
bird.x_coord = w / 2 - 50
bird.y_coord = h / 2

# game loop 
while running: 
    
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

    bird.velocity -= gravity
    if bird.velocity <= 0:
        bird.velocity = 0

    bird.y_coord += gravity - bird.velocity

    if bird.y_coord < 0 + bird.radius:
        bird.y_coord = bird.radius
    print(bird.y_coord)

    if bird.y_coord >= h - bird.radius:
        running = False

    window.fill(background_color)
    pygame.draw.circle(window, bird.color, (bird.x_coord, bird.y_coord), bird.radius)
    pygame.display.update()

    # set FPS to 60
    clock.tick(60)  
    # https://stackoverflow.com/questions/35617246/setting-a-fixed-fps-in-pygame-python-3
    # might want to look at this later