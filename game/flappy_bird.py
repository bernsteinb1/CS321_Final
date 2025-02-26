import pygame

# make bird class
class Bird:
    def __init__(self):
        self.x_velocity = 0
        self.y_velocity = 0
        self.x_coord = 0
        self.y_coord = 0
        self.distance_from_pipe = 0
        self.color = (249, 220, 53)
        self.radius = 25
        # i forgot one of the variables we talked about

# make obstacle class constructor 

# ------------- game code -------------
# setup window and basic game items
background_colour = (5, 213, 250) 
window = pygame.display.set_mode((480, 640)) 

pygame.display.set_caption('Bryce & Ruben: Flappy Bird') 
  
window.fill(background_colour) 
  
pygame.display.update() 
  
# Variable to keep our game loop running 
running = True

# setup bird object
bird = Bird()

# set screen position 
w, h = pygame.display.get_surface().get_size()
bird.xcoord = w / 2 - 50
bird.ycoord = h / 2

# game loop 
while running: 
    
# for loop through the event queue   
    for event in pygame.event.get(): 
      
        if event.type == pygame.QUIT: 
            running = False

        if event.type == pygame.KEYDOWN:
            print("keypress!")

    # keys = pygame.key.get_pressed() 
    # if keys[pygame.K_SPACE]:
    #     print("space bar!")
    pygame.draw.circle(window, bird.color, (bird.xcoord, bird.ycoord), bird.radius)
    pygame.display.update()