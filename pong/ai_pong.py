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
        # randomize starting position until paddle would be at a legal position
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
            if res is not None:
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


if __name__ == '__main__':
    # from PyGame website
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Bryce Ruben: Final Pong")
    clock = pygame.time.Clock()
    graphics_on = True

    best_nn = None
    best_score = -math.inf
    
    # game tuple takes form (network, paddle_y, score)
    games = [[NeuralNetwork(), 0, 0] for _ in range(NUM_AGENTS)]
    
    for gen in range(GENERATIONS):
        for _ in range(TRIALS_PER_GEN):
            ball = Ball()
            angle = math.degrees(math.atan(ball.y_velocity / ball.x_velocity))
            paddle_y = ball.y - angle / BALL_MAX_ANGLE * (PADDLE_HEIGHT / 2 + BALL_RADIUS) - PADDLE_HEIGHT / 2
            for game in games:
                game[1] = paddle_y

            while True:
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
                    inp = [ball.x, ball.y, ball.x_velocity, ball.y_velocity, game[1] + PADDLE_HEIGHT / 2] 
                    up, down = game[0].run(inp)
                    if up > 0 and not down > 0:
                        game[1] = max(game[1] - PADDLE_SPEED, 0)
                    if down > 0 and not up > 0:
                        game[1] = min(game[1] + PADDLE_SPEED, SCREEN_HEIGHT - PADDLE_HEIGHT)
                    if graphics_on:
                        pygame.draw.rect(screen, PADDLE_COLOR, (PADDLE_DIST_FROM_EDGE, game[1], PADDLE_WIDTH, PADDLE_HEIGHT))
                ball_update = ball.update()
                if ball_update is not None:
                    for game in games:
                        if ball_update > game[1] - BALL_RADIUS and ball_update < game[1] + BALL_RADIUS:
                            game[2] += 1
                    break
                if graphics_on:
                    pygame.display.flip()
                    clock.tick(60)
        games.sort(key=lambda game: game[2], reverse=True)
        if games[0][2] > best_score:
            best_score = games[0][2]
            best_nn = games[0][0]
        new_games = []

        print(f'Generation {gen + 1} results')
        for i in range(SELECT_NUM):
            print(games[i][2])
            new_games.append([games[i][0], 0, 0])
        print('============================')
        sys.stdout.flush()
        
        # create next generation using tournament selection
        while len(new_games) < NUM_AGENTS - RANDOM_NETWORKS_PER_GEN:
            parent_1_options = random.sample(games, TOURNAMENT_SIZE)
            parent_2_options = random.sample(games, TOURNAMENT_SIZE)

            parent1 = max(parent_1_options, key=lambda x: x[2])
            parent2 = max(parent_2_options, key=lambda x: x[2])
            if parent1 == parent2:
                continue
            crossover_child = crossover(parent1[0], parent2[0])
            new_games.append([crossover_child, 0, 0])

        for i in range(RANDOM_NETWORKS_PER_GEN):
            new_games.append([NeuralNetwork(), 0, 0])
        games = new_games

    with open('champion.pickle', 'wb') as f:
        pickle.dump(best_nn, f)
    pygame.quit()