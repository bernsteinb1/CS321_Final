import pygame
import random
import math

BACKGROUND_COLOR = (0, 0, 0)
PADDLE_COLOR = (255, 255, 255)
BALL_COLOR = (0, 0, 255)
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
BALL_RADIUS = 10
PADDLE_DIST_FROM_EDGE = 5
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 50
BALL_START_SPEED = 1
PADDLE_SPEED = .5

class Ball:
    def __init__(self):
        self.x = SCREEN_WIDTH / 2 - BALL_RADIUS / 2
        self.y = SCREEN_HEIGHT / 2 - BALL_RADIUS / 2
        self.randomize_start_vel()

    def randomize_start_vel(self):
        angle = random.randint(-75, 75)
        if random.random() < .5:
            angle += 180
        angle = math.radians(angle)
        self.x_velocity = BALL_START_SPEED * math.cos(angle)
        self.y_velocity = BALL_START_SPEED * math.sin(angle)

    def update(self):
        self.x += self.x_velocity
        self.y += self.y_velocity
        self.y = max(BALL_RADIUS, min(SCREEN_HEIGHT - BALL_RADIUS, self.y))
        if self.y == BALL_RADIUS or self.y == SCREEN_HEIGHT - BALL_RADIUS:
            self.y_velocity *= -1
    
    def draw(self, window):
        pygame.draw.circle(window, BALL_COLOR, (self.x, self.y), BALL_RADIUS)


class Paddle:
    def __init__(self, side):
        if side == 'l':
            self.x = PADDLE_DIST_FROM_EDGE
        else:
            self.x = SCREEN_WIDTH - PADDLE_DIST_FROM_EDGE - PADDLE_WIDTH
        self.y = SCREEN_HEIGHT / 2 - PADDLE_HEIGHT / 2
    
    def draw(self, window):
        pygame.draw.rect(window, PADDLE_COLOR, (self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT))

    def move_up(self):
        self.y = max(self.y - PADDLE_SPEED, 0)
    
    def move_down(self):
        self.y = min(self.y + PADDLE_SPEED, SCREEN_HEIGHT - PADDLE_HEIGHT)
        

if __name__ == '__main__':
    # from PyGame website
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True

    # set up game
    ball = Ball()
    left_paddle = Paddle('l')
    right_paddle = Paddle('r')

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN]:
            right_paddle.move_down()
        if keys[pygame.K_UP]:
            right_paddle.move_up()
        if keys[pygame.K_w]:
            left_paddle.move_up()
        if keys[pygame.K_s]:
            left_paddle.move_down()
        screen.fill(BACKGROUND_COLOR)

        # draw game components
        ball.draw(screen)
        left_paddle.draw(screen)
        right_paddle.draw(screen)

        ball.update()

        pygame.display.flip()
        clock.tick(500)
    pygame.quit()