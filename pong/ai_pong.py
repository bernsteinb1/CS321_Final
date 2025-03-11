import pygame
import random
import math
import sys
import numpy as np
from nn import NeuralNetwork

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

NUM_AGENTS = 1000

GENERATIONS = 30
SELECT_NUM = 50
RANDOM_NETWORKS_PER_GEN = 50
GAMES_PER_GEN = 5

STILLNESS_PUNISHMENT_FACTOR = .5
DISTANCE_PUNISHMENT_FACTOR = 1

class Ball:
    def __init__(self):
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

    def move_up(self, target=None):
        self.y = max(self.y - PADDLE_SPEED, 0)
        if target is not None:
            self.y = max(self.y, target)
    
    def move_down(self, target=None):
        self.y = min(self.y + PADDLE_SPEED, SCREEN_HEIGHT - PADDLE_HEIGHT)
        if target is not None:
            self.y = min(self.y, target)


class AIPlayer:
    def __init__(self):
        self.target_y = SCREEN_HEIGHT / 2 - PADDLE_HEIGHT / 2
    
    def calculate_target(self, ball):
        x_coord = ball.x
        y_coord = ball.y
        x_step = 1
        y_step = ball.y_velocity / ball.x_velocity
        while x_coord + BALL_RADIUS < SCREEN_WIDTH - PADDLE_DIST_FROM_EDGE - PADDLE_WIDTH:
            x_coord += x_step
            y_coord += y_step
            if y_coord < BALL_RADIUS or y_coord > SCREEN_HEIGHT - BALL_RADIUS:
                y_adj = SCREEN_HEIGHT - BALL_RADIUS - y_coord if y_coord > SCREEN_HEIGHT - BALL_RADIUS else BALL_RADIUS - y_coord
                y_coord += 2 * y_adj
                y_step *= -1
        self.target_y = y_coord + random.randint(int(-PADDLE_HEIGHT / 2) - BALL_RADIUS + 1, int(PADDLE_HEIGHT / 2) + BALL_RADIUS - 1) - PADDLE_HEIGHT / 2 # can't be equal to ball radius so we add 1

    def reset_target(self):
        self.target_y = SCREEN_HEIGHT / 2 - PADDLE_HEIGHT / 2

    def get_move(self, paddle):
        if paddle.y < int(self.target_y):
            return -1
        if paddle.y > int(self.target_y):
            return 1
        return 0
    

class Game:
    def __init__(self, neural_net):
        self.ball = Ball()
        self.left_paddle = Paddle('l')
        self.right_paddle = Paddle('r')
        self.left_ai = neural_net
        self.right_ai = AIPlayer()
        self.right_ai.calculate_target(self.ball)
        self.running = True
        self.score = 0
        self.has_moved = False

    def draw(self, screen):
        self.left_paddle.draw(screen)
        self.right_paddle.draw(screen)
        self.ball.draw(screen)

    def update(self):
        moved_proportion = 0  # at the beginning the ball has not moved at all
        # this gets called if the ball could possibly collide with a paddle.
        if (self.ball.x + self.ball.x_velocity + BALL_RADIUS >= self.right_paddle.x or self.ball.x + self.ball.x_velocity - BALL_RADIUS <= self.left_paddle.x + PADDLE_WIDTH) \
            and self.ball.x + BALL_RADIUS <= self.right_paddle.x and self.ball.x - BALL_RADIUS >= self.left_paddle.x + PADDLE_WIDTH:
            # see if ball collided or was missed
            res = self.collision_right() if self.ball.x + self.ball.x_velocity + BALL_RADIUS >= self.right_paddle.x else self.collision_left()
            if res:
                return True
            # how much the ball will have moved when it hits a paddle
            moved_proportion (self.right_paddle.x - (self.ball.x + BALL_RADIUS)) / self.ball.x_velocity if self.ball.x + self.ball.x_velocity + BALL_RADIUS >= self.right_paddle.x else ((self.ball.x - BALL_RADIUS) - (self.left_paddle.x + PADDLE_WIDTH)) / self.ball.x_velocity

        # move remaining amount (which is all if the ball did not hit a paddle)
        self.ball.x += self.ball.x_velocity * (1 - moved_proportion)
        self.ball.y += self.ball.y_velocity * (1 - moved_proportion)
        new_y = max(BALL_RADIUS, min(SCREEN_HEIGHT - BALL_RADIUS, self.ball.y))
        # if it bounced off a wall, we need to correct for the rest of the motion
        if new_y != self.ball.y:
            self.ball.y -= 2 * (self.ball.y - new_y)
            self.ball.y_velocity *= -1
        else:
            self.ball.y = new_y
        return False
        
    def collision_right(self):
        ball_slope = self.ball.y_velocity / self.ball.x_velocity
        collision_y = self.ball.y + ball_slope * (self.right_paddle.x - (self.ball.x + BALL_RADIUS))
        if collision_y + BALL_RADIUS > self.right_paddle.y and collision_y - BALL_RADIUS < self.right_paddle.y + PADDLE_HEIGHT:
            
            # calculate how the ball hit the paddle
            paddle_center = self.right_paddle.y + PADDLE_HEIGHT / 2
            new_angle = math.pi + (paddle_center - collision_y) / (PADDLE_HEIGHT / 2 + BALL_RADIUS) * math.radians(BALL_MAX_ANGLE)
            self.ball.x_velocity = BALL_START_SPEED * math.cos(new_angle)
            self.ball.y_velocity = BALL_START_SPEED * math.sin(new_angle)

            # adjust location
            self.ball.x = self.right_paddle.x - BALL_RADIUS
            self.ball.y = collision_y
        
        # this is for if the ball was missed
        else:
            return True
    
        self.right_ai.reset_target()
        return False

    def collision_left(self):
        ball_slope = self.ball.y_velocity / self.ball.x_velocity
        collision_y = self.ball.y + ball_slope * (self.left_paddle.x + PADDLE_WIDTH - (self.ball.x - BALL_RADIUS))
        if collision_y + BALL_RADIUS > self.left_paddle.y and collision_y - BALL_RADIUS < self.left_paddle.y + PADDLE_HEIGHT:

            # calculate how ball hit paddle
            paddle_center = self.left_paddle.y + PADDLE_HEIGHT / 2
            new_angle = (collision_y - paddle_center) / (PADDLE_HEIGHT / 2 + BALL_RADIUS) * math.radians(BALL_MAX_ANGLE)
            self.ball.x_velocity = BALL_START_SPEED * math.cos(new_angle)
            self.ball.y_velocity = BALL_START_SPEED * math.sin(new_angle)

            # adjust location
            self.ball.x = self.left_paddle.x + PADDLE_WIDTH + BALL_RADIUS
            self.ball.y = collision_y
        
        # this is for if the ball was missed
        else:
            self.score -= abs(collision_y - (self.left_paddle.y + PADDLE_HEIGHT / 2)) / SCREEN_HEIGHT * DISTANCE_PUNISHMENT_FACTOR
            return True
        
        # inc score if ball hit
        self.score += 1
        if not self.has_moved:
            self.score -= 1 * STILLNESS_PUNISHMENT_FACTOR
        self.has_moved = False
        self.right_ai.calculate_target(self.ball)
        return False
    
def get_softmax_probabilities(games):
    fitness_scores = np.array([game.score for game in games])
    exp_fitness = np.exp(fitness_scores)
    probabilities = exp_fitness / np.sum(exp_fitness)

    return probabilities
        

if __name__ == '__main__':
    # from PyGame website
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Bryce Ruben: Final Pong")
    clock = pygame.time.Clock()
    graphics_on = True

    games = [Game(NeuralNetwork()) for _ in range(NUM_AGENTS)]
    
    for _ in range(GENERATIONS):
        for _ in range(GAMES_PER_GEN):
            living_game = True
            while living_game:
                living_game = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            if graphics_on:
                                graphics_on = False
                                print("Graphics turned OFF")
                            else:
                                graphics_on = True
                                print("Graphics turned ON")

                if graphics_on:
                    screen.fill(BACKGROUND_COLOR)

                # 1 tick for each agent and its associated enemy ai
                for game in games:
                    if game.running:
                        living_game = True
                        inp = [game.ball.x, game.ball.y, game.ball.x_velocity, game.ball.y_velocity, game.left_paddle.y + PADDLE_HEIGHT / 2, game.right_paddle.y + PADDLE_HEIGHT / 2] 
                        up, down = game.left_ai.run(inp)
                        if up > 0 and not down > 0:
                            before_y = game.left_paddle.y
                            game.left_paddle.move_up()
                            after_y = game.left_paddle.y
                            if before_y != after_y:
                                game.has_moved = True
                        if down > 0 and not up > 0:
                            before_y = game.left_paddle.y
                            game.left_paddle.move_down()
                            after_y = game.left_paddle.y
                            if before_y != after_y:
                                game.has_moved = True

                        # move pong ai
                        mv = game.right_ai.get_move(game.right_paddle)
                        if mv == 1:
                            game.right_paddle.move_up(target=game.right_ai.target_y)
                        elif mv == -1:
                            game.right_paddle.move_down(target=game.right_ai.target_y)

                        if game.update():
                            # remove finished game
                            game.running = False
                        if graphics_on:
                            game.draw(screen)
                if graphics_on:
                    pygame.display.flip()
            for i in range(len(games)):
                score = games[i].score
                games[i] = Game(games[i].left_ai)
                games[i].score = score
        games.sort(key=lambda game: game.score, reverse=True)
        new_games = games[:SELECT_NUM]

        for i in range(len(new_games)):
            print(new_games[i].score)
            new_games[i] = Game(games[i].left_ai)
        print('============================')
        
        # create next generation
        while len(new_games) < NUM_AGENTS - RANDOM_NETWORKS_PER_GEN:
            for i in range(SELECT_NUM):
                probabilities = get_softmax_probabilities(new_games)
                parent1 = np.random.choice(new_games, p=probabilities)
                parent2 = np.random.choice(new_games, p=probabilities)
                # print("parent 1 score:", parent1.score, "parent 2 score:", parent2.score)

                # does this work to crossover then mutate?
                crossover_child = Game(new_games[i].left_ai.crossover(parent1, parent2)) 
                new_games.append(Game(crossover_child.left_ai.mutate()))

                # new_games.append(Game(new_games[i].left_ai.mutate()))
        while len(new_games) > NUM_AGENTS - RANDOM_NETWORKS_PER_GEN:
            new_games.remove(random.choice(new_games))
        for i in range(RANDOM_NETWORKS_PER_GEN):
            new_games.append(Game(NeuralNetwork()))
        games = new_games
    pygame.quit()