import pygame
import random
import math

BACKGROUND_COLOR = (0, 0, 0)
PADDLE_COLOR = (255, 255, 255)
BALL_COLOR = (0, 200, 255)
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
BALL_RADIUS = 10
PADDLE_DIST_FROM_EDGE = 5
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 50
BALL_START_SPEED = 3
PADDLE_SPEED = 2

class Ball:
    def __init__(self):
        self.x = SCREEN_WIDTH / 2 - BALL_RADIUS / 2
        self.y = SCREEN_HEIGHT / 2 - BALL_RADIUS / 2
        self.randomize_start_vel()

    def randomize_start_vel(self):
        angle = random.randint(-10, 10)
        if random.random() < .5:
            angle += 180
        angle = math.radians(angle)
        self.x_velocity = BALL_START_SPEED * math.cos(angle)
        self.y_velocity = BALL_START_SPEED * math.sin(angle)

    def update(self, left_paddle, right_paddle):
        moved_proportion = 0
        # this gets called if the ball could possibly collide with a paddle.
        if (self.x + self.x_velocity > right_paddle.x or self.x + self.x_velocity < left_paddle.x + PADDLE_WIDTH) \
            and self.x <= right_paddle.x and self.x >= left_paddle.x + PADDLE_WIDTH:
            ball_slope = self.y_velocity / self.x_velocity
            # right paddle
            if self.x + self.x_velocity > right_paddle.x:
                collision_y = self.y + ball_slope * (right_paddle.x - self.x)
                if collision_y + BALL_RADIUS > right_paddle.y and collision_y - BALL_RADIUS < right_paddle.y + PADDLE_HEIGHT:
                    paddle_center = right_paddle.y + PADDLE_HEIGHT / 2
                    moved_proportion = (right_paddle.x - self.x) / self.x_velocity
                    new_angle = math.pi + (paddle_center - collision_y) / (PADDLE_HEIGHT / 2 + BALL_RADIUS) * 15/36 * math.pi
                    self.x_velocity = BALL_START_SPEED * math.cos(new_angle)
                    self.y_velocity = BALL_START_SPEED * math.sin(new_angle)

                    self.x = right_paddle.x
                    self.y = collision_y
            # left paddle
            else:
                collision_y = self.y + ball_slope * (left_paddle.x + PADDLE_WIDTH - self.x)
                if collision_y + BALL_RADIUS > left_paddle.y and collision_y - BALL_RADIUS < left_paddle.y + PADDLE_HEIGHT:
                    paddle_center = left_paddle.y + PADDLE_HEIGHT / 2
                    moved_proportion = (self.x - (left_paddle.x + PADDLE_WIDTH)) / self.x_velocity
                    new_angle = (collision_y - paddle_center) / (PADDLE_HEIGHT / 2 + BALL_RADIUS) * 15/36 * math.pi
                    self.x_velocity = BALL_START_SPEED * math.cos(new_angle)
                    self.y_velocity = BALL_START_SPEED * math.sin(new_angle)

                    self.x = left_paddle.x + PADDLE_WIDTH
                    self.y = collision_y
        # no collision
        self.x += self.x_velocity * (1 - moved_proportion)
        self.y += self.y_velocity * (1 - moved_proportion)
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
    pygame.display.set_caption("Bryce Ruben: Final Pong")
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

        ball.update(left_paddle, right_paddle)

        # draw game components
        screen.fill(BACKGROUND_COLOR)
        ball.draw(screen)
        left_paddle.draw(screen)
        right_paddle.draw(screen)

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

def main():
    pass

if __name__ == '__main__':
    main()