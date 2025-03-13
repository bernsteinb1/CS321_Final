import pygame
import random
import math
import sys
import numpy as np
from nn import NeuralNetwork, crossover
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
BALL_MAX_ANGLE = 75

PADDLE_SPEED = 3

NUM_AGENTS = 1000

GENERATIONS = 30
SELECT_NUM = 10
RANDOM_NETWORKS_PER_GEN = 0  # introduce a number of random networks each generation, this can prevent stagnation
TRIALS_PER_GEN = 20
TOURNAMENT_SIZE = 10

STILLNESS_PUNISHMENT_FACTOR = 0
DISTANCE_PUNISHMENT_FACTOR = 0

class Ball:
    def __init__(self):
        paddle_y = -1
        while paddle_y < 0 or paddle_y + PADDLE_HEIGHT > SCREEN_HEIGHT:
            self.x = PADDLE_DIST_FROM_EDGE + PADDLE_WIDTH + BALL_RADIUS
            self.y = random.randint(BALL_RADIUS, SCREEN_HEIGHT - BALL_RADIUS)
            self.randomize_start_vel()

            angle = math.degrees(math.atan(self.y_velocity / self.x_velocity))
            paddle_y = self.y - angle / BALL_MAX_ANGLE * (PADDLE_HEIGHT / 2 + BALL_RADIUS) - PADDLE_HEIGHT / 2

    def randomize_start_vel(self):
        """Randomizes start velocity for ball up to BALL_START_ANGLE
        """
        angle = random.randint(-BALL_MAX_ANGLE, BALL_MAX_ANGLE)
        angle = math.radians(angle)
        self.x_velocity = BALL_START_SPEED * math.cos(angle)
        self.y_velocity = BALL_START_SPEED * math.sin(angle)

    def draw(self, window):
        pygame.draw.circle(window, BALL_COLOR, (self.x, self.y), BALL_RADIUS)

    def collision_right(self):
        ball_slope = self.y_velocity / self.x_velocity
        collision_y = self.y + ball_slope * (SCREEN_WIDTH - PADDLE_DIST_FROM_EDGE - PADDLE_WIDTH - (self.x + BALL_RADIUS))
        self.x = SCREEN_WIDTH - PADDLE_DIST_FROM_EDGE - PADDLE_WIDTH - BALL_RADIUS
        self.y = collision_y

        angle = random.randrange(-BALL_MAX_ANGLE, BALL_MAX_ANGLE) + 180
        self.x_velocity = math.cos(math.radians(angle)) * BALL_START_SPEED
        self.y_velocity = math.sin(math.radians(angle)) * BALL_START_SPEED

    def collision_left(self):
        ball_slope = self.y_velocity / self.x_velocity
        collision_y = self.y + ball_slope * (PADDLE_DIST_FROM_EDGE + PADDLE_WIDTH + BALL_RADIUS - (self.x - BALL_RADIUS))
        return collision_y

    def update(self):
        moved_proportion = 0  # at the beginning the ball has not moved at all
        # this gets called if the ball could possibly collide with a paddle.
        left_paddle = PADDLE_DIST_FROM_EDGE + PADDLE_WIDTH
        right_paddle = SCREEN_WIDTH - left_paddle
        if (self.x + self.x_velocity + BALL_RADIUS >= right_paddle or self.x + self.x_velocity - BALL_RADIUS <= left_paddle) \
            and self.x + BALL_RADIUS <= right_paddle and self.x - BALL_RADIUS >= left_paddle:
            # see if ball collided or was missed
            res = self.collision_right() if self.x + self.x_velocity + BALL_RADIUS >= right_paddle else self.collision_left()
            if res != None:
                return res
            # how much the ball will have moved when it hits a paddle
            moved_proportion = (right_paddle - (self.x + BALL_RADIUS)) / self.x_velocity

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

class Paddle:
    def __init__(self, side):
        if side == 'l':
            self.x = PADDLE_DIST_FROM_EDGE
        else:
            self.x = SCREEN_WIDTH - PADDLE_DIST_FROM_EDGE - PADDLE_WIDTH
    
    def draw(self, window):
        pygame.draw.rect(window, PADDLE_COLOR, (self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT))

    def move_up(self, target=None):
        self.y = max(self.y - PADDLE_SPEED, 0)
        if target is not None:
            self.y = max(self.y, target)
    
    def move_down(self, target=None):
        self.y = min(self.y + PADDLE_SPEED, SCREEN_HEIGHT - PADDLE_HEIGHT)
        if target is not None:
            self.y = min(self.y, target)

class Game:
    def __init__(self, neural_net):
        self.left_paddle = Paddle('l')
        self.left_ai = neural_net
        self.score = 0

    def draw(self, screen):
        self.left_paddle.draw(screen)

    def reward(self, ball_update):
        self.score += 1 - abs(self.left_paddle.y - ball_update) / SCREEN_HEIGHT


if __name__ == '__main__':
    # from PyGame website
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Bryce Ruben: Final Pong")
    clock = pygame.time.Clock()
    graphics_on = True

    best_nn = None
    best_score = -math.inf
    
    games = [Game(NeuralNetwork()) for _ in range(NUM_AGENTS)]
    
    for gen in range(GENERATIONS):
        for _ in range(TRIALS_PER_GEN):
            ball = Ball()
            angle = math.degrees(math.atan(ball.y_velocity / ball.x_velocity))
            paddle_y = ball.y - angle / BALL_MAX_ANGLE * (PADDLE_HEIGHT / 2 + BALL_RADIUS) - PADDLE_HEIGHT / 2
            for game in games:
                game.left_paddle.y = paddle_y

            living_game = True
            while living_game:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            if graphics_on:
                                graphics_on = False
                                print("Graphics turned OFF", file=sys.stderr)
                            else:
                                graphics_on = True
                                print("Graphics turned ON", file=sys.stderr)

                if graphics_on:
                    screen.fill(BACKGROUND_COLOR)
                    ball.draw(screen)

                # 1 tick for each agent
                for game in games:
                    inp = [ball.x, ball.y, ball.x_velocity, ball.y_velocity, game.left_paddle.y + PADDLE_HEIGHT / 2] 
                    up, down = game.left_ai.run(inp)
                    if up > 0 and not down > 0:
                        game.left_paddle.move_up()
                    if down > 0 and not up > 0:
                        game.left_paddle.move_down()                                                
                    if graphics_on:
                        game.draw(screen)
                ball_update = ball.update()
                if ball_update != None:
                    for game in games:
                        game.reward(ball_update)
                    break
                if graphics_on:
                    pygame.display.flip()
                    clock.tick(60)
            for i in range(len(games)):
                score = games[i].score
                games[i] = Game(games[i].left_ai)
                games[i].score = score
        games.sort(key=lambda game: game.score, reverse=True)
        if games[0].score > best_score:
            best_score = games[0].score
            best_nn = games[0].left_ai
        new_games = []

        print(f'Generation {gen + 1} results')
        for i in range(SELECT_NUM):
            print(games[i].score)
            new_games.append(Game(games[i].left_ai))
        print('============================')
        sys.stdout.flush()
        
        # create next generation using tournament selection
        while len(new_games) < NUM_AGENTS - RANDOM_NETWORKS_PER_GEN:
            parent_1_options = np.random.choice(games, TOURNAMENT_SIZE, False)
            parent_2_options = np.random.choice(games, TOURNAMENT_SIZE, False)

            parent1 = max(parent_1_options, key=lambda x: x.score)
            parent2 = max(parent_2_options, key=lambda x: x.score)
            if parent1 == parent2:
                continue
            crossover_child = crossover(parent1.left_ai, parent2.left_ai)
            new_games.append(Game(crossover_child.mutate()))

        for i in range(RANDOM_NETWORKS_PER_GEN):
            new_games.append(Game(NeuralNetwork()))
        games = new_games

    with open('champion.pickle', 'wb') as f:
        pickle.dump(best_nn, f)
    pygame.quit()