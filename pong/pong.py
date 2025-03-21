import pygame
import random
import math
import pickle

# changing any of these will change something about the game.
# any changes within reason will not cause an error (something like making the games width smaller than the paddle's width might cause a problem)
# all values should be integers.
BACKGROUND_COLOR = (0, 0, 0)
PADDLE_COLOR = (255, 255, 255)
BALL_COLOR = (0, 200, 255)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
BALL_RADIUS = 10
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 50
PADDLE_DIST_FROM_EDGE = 5

BALL_START_SPEED = 5
BALL_START_ANGLE = 20
BALL_MAX_ANGLE = 75

PADDLE_SPEED = 3

AI_PLAYER = True

left_score = 0
right_score = 0

class Paddle:
    def __init__(self, side: str):
        """Creates a paddle on one of the sides

        Args:
            side (str): 'l' for left and anything else (but probably should be 'r') for right
        """
        if side == 'l':
            self.x = PADDLE_DIST_FROM_EDGE
        else:
            self.x = SCREEN_WIDTH - PADDLE_DIST_FROM_EDGE - PADDLE_WIDTH
        self.y = SCREEN_HEIGHT / 2 - PADDLE_HEIGHT / 2
    
    def draw(self, window: pygame.Surface):
        """Draws paddle onto window

        Args:
            window (pygame.Surface): where paddle is drawn
        """
        pygame.draw.rect(window, PADDLE_COLOR, (self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT))

    def move_up(self):
        """Moves paddle up capping at top of screen
        """
        self.y = max(self.y - PADDLE_SPEED, 0)
    
    def move_down(self):
        """Moves paddle down capping at bottom of screen
            """
        self.y = min(self.y + PADDLE_SPEED, SCREEN_HEIGHT - PADDLE_HEIGHT)

class Ball:
    def __init__(self):
        """Creates centered Ball object with random starting velocity.
        """
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2
        self.randomize_start_vel()

    def randomize_start_vel(self):
        """Randomizes start velocity for ball up to BALL_START_ANGLE
        """
        angle = random.randint(-BALL_START_ANGLE, BALL_START_ANGLE)
        if random.random() < .5:
            angle += 180
        angle = math.radians(angle)
        self.x_velocity = BALL_START_SPEED * math.cos(angle)
        self.y_velocity = BALL_START_SPEED * math.sin(angle)

    def update(self, left_paddle, right_paddle):
        """Calculates all updates for the game, including ball motion, wall collision, and paddle collision. Results
        give info about whether a player scored.

        Args:
            left_paddle (Paddle): the left paddle object
            right_paddle (Paddle): the right paddle object.

        Returns:
            bool: True if someone scored
        """
        moved_proportion = 0  # at the beginning the ball has not moved at all
        # this gets called if the ball could possibly collide with a paddle.
        if (self.x + self.x_velocity + BALL_RADIUS >= right_paddle.x or self.x + self.x_velocity - BALL_RADIUS <= left_paddle.x + PADDLE_WIDTH) \
            and self.x + BALL_RADIUS <= right_paddle.x and self.x - BALL_RADIUS >= left_paddle.x + PADDLE_WIDTH:
            # see if ball collided or was missed
            res = self.collision_right(right_paddle) if self.x + self.x_velocity + BALL_RADIUS >= right_paddle.x else self.collision_left(left_paddle)
            if res:
                return True
            # how much the ball will have moved when it hits a paddle
            moved_proportion (right_paddle.x - (self.x + BALL_RADIUS)) / self.x_velocity if self.x + self.x_velocity + BALL_RADIUS >= right_paddle.x else ((self.x - BALL_RADIUS) - (left_paddle.x + PADDLE_WIDTH)) / self.x_velocity

        # move remaining amount (which is all if the ball did not hit a paddle)
        self.x += self.x_velocity * (1 - moved_proportion)
        self.y += self.y_velocity * (1 - moved_proportion)
        new_y = max(BALL_RADIUS, min(SCREEN_HEIGHT - BALL_RADIUS, self.y))
        # if it bounced off a wall, we need to correct for the rest of the motion
        if new_y != self.y:
            self.y -= 2 * (self.y - new_y)
            self.y_velocity *= -1
        else:
            self.y = new_y
        return False
        
    def collision_right(self, right_paddle):
        """Handles collision on right side

        Args:
            right_paddle (Paddle): the right paddle

        Returns:
            bool: True if left scored.
        """
        ball_slope = self.y_velocity / self.x_velocity
        collision_y = self.y + ball_slope * (right_paddle.x - (self.x + BALL_RADIUS))
        if collision_y + BALL_RADIUS > right_paddle.y and collision_y - BALL_RADIUS < right_paddle.y + PADDLE_HEIGHT:
            
            # calculate how the ball hit the paddle
            paddle_center = right_paddle.y + PADDLE_HEIGHT / 2
            new_angle = math.pi + (paddle_center - collision_y) / (PADDLE_HEIGHT / 2 + BALL_RADIUS) * math.radians(BALL_MAX_ANGLE)
            self.x_velocity = BALL_START_SPEED * math.cos(new_angle)
            self.y_velocity = BALL_START_SPEED * math.sin(new_angle)

            # adjust location
            self.x = right_paddle.x - BALL_RADIUS
            self.y = collision_y
        
        # this is for if the ball was missed
        else:
            global left_score
            left_score += 1
            print("Left scored!")
            return True
    
        return False

    def collision_left(self, left_paddle):
        """Handles collision on left side

        Args:
            left_paddle (Paddle): the left paddle

        Returns:
            bool: True if right scored.
        """
        ball_slope = self.y_velocity / self.x_velocity
        collision_y = self.y + ball_slope * (left_paddle.x + PADDLE_WIDTH - (self.x - BALL_RADIUS))
        if collision_y + BALL_RADIUS > left_paddle.y and collision_y - BALL_RADIUS < left_paddle.y + PADDLE_HEIGHT:

            # calculate how ball hit paddle
            paddle_center = left_paddle.y + PADDLE_HEIGHT / 2
            new_angle = (collision_y - paddle_center) / (PADDLE_HEIGHT / 2 + BALL_RADIUS) * math.radians(BALL_MAX_ANGLE)
            self.x_velocity = BALL_START_SPEED * math.cos(new_angle)
            self.y_velocity = BALL_START_SPEED * math.sin(new_angle)

            # adjust location
            self.x = left_paddle.x + PADDLE_WIDTH + BALL_RADIUS
            self.y = collision_y
        
        # this is for if the ball was missed
        else:
            global right_score
            right_score += 1
            print("Right scored!")
            return True
        
        return False
    
    def draw(self, window):
        pygame.draw.circle(window, BALL_COLOR, (self.x, self.y), BALL_RADIUS)


if __name__ == '__main__':
    # from PyGame website
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Bryce Ruben: Final Pong")
    clock = pygame.time.Clock()
    # to use champion.pickle or last_gen.pickle, set their filepath below.
    with open('last_gen.pickle', 'rb') as champ:
        ai = pickle.load(champ)

    # set up game
    ball = Ball()
    left_paddle = Paddle('l')
    right_paddle = Paddle('r')

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        keys = pygame.key.get_pressed()
        if not AI_PLAYER:
            if keys[pygame.K_w]:
                left_paddle.move_up()
            if keys[pygame.K_s]:
                left_paddle.move_down()
        else:
            # run inputs through neural network to get action
            inp = [ball.x, ball.y, ball.x_velocity, ball.y_velocity, left_paddle.y + PADDLE_HEIGHT / 2] 
            up, down = ai.run(inp)
            if up > 0 and not down > 0:
                left_paddle.move_up()
            if down > 0 and not up > 0:
                left_paddle.move_down()
        if keys[pygame.K_UP]:
            right_paddle.move_up()
        if keys[pygame.K_DOWN]:
            right_paddle.move_down()

        if ball.update(left_paddle, right_paddle):
            print(f"Right: {right_score}\nLeft: {left_score}")
            ball = Ball()
            left_paddle = Paddle('l')
            right_paddle = Paddle('r')

        # draw game components
        screen.fill(BACKGROUND_COLOR)
        ball.draw(screen)
        left_paddle.draw(screen)
        right_paddle.draw(screen)

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()