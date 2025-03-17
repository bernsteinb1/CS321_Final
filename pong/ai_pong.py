import math
import random
import sys
from nn import NeuralNetwork, crossover
import pickle
import multiprocessing
from functools import partial

# changing any of these will change something about the game.
# any changes within reason will not cause an error (something like making the games width smaller than the paddle's width might cause a problem)
# all values should be integers. These values should match those in pong.py if you expect good AI performance.

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
BALL_RADIUS = 10
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 50
PADDLE_DIST_FROM_EDGE = 5

BALL_START_SPEED = 5
BALL_MAX_ANGLE = 75
PADDLE_SPEED = 3

NUM_AGENTS = 1000  # how many agents to introduce each generation
GENERATIONS = 50
SELECT_NUM = 10  # how many agents automatically advance to the next generation without modification. Also impacts number of results printed.
RANDOM_NETWORKS_PER_GEN = 0  # introduce a number of random networks each generation, this can prevent stagnation
TRIALS_PER_GEN = 1000  # how many trials to run each generation 
TOURNAMENT_SIZE = 10  # in tournament selection (https://en.wikipedia.org/wiki/Tournament_selection) the tournament size.

class Ball:
    def __init__(self):
        """Create ball object such that it has been hit in a possible way
        """
        paddle_y = -1
        # randomize starting position until paddle would be at a legal position
        while paddle_y < 0 or paddle_y + PADDLE_HEIGHT > SCREEN_HEIGHT:
            self.x = PADDLE_DIST_FROM_EDGE + PADDLE_WIDTH + BALL_RADIUS
            self.y = random.randint(BALL_RADIUS, SCREEN_HEIGHT - BALL_RADIUS)
            self.randomize_start_vel()

            angle = math.degrees(math.atan(self.y_velocity / self.x_velocity))
            paddle_y = self.y - angle / BALL_MAX_ANGLE * (PADDLE_HEIGHT / 2 + BALL_RADIUS) - PADDLE_HEIGHT / 2

    def randomize_start_vel(self):
        """Randomizes start velocity for ball up to BALL_MAX_ANGLE
        """
        angle = random.randint(-BALL_MAX_ANGLE, BALL_MAX_ANGLE)
        angle = math.radians(angle)
        self.x_velocity = BALL_START_SPEED * math.cos(angle)
        self.y_velocity = BALL_START_SPEED * math.sin(angle)

    def collision_right(self):
        """In each trial, right collisions are certain. When it happens it will randomly set the velocity to somewhere
        between -BALL_MAX_ANGLE and BALL_MAX_ANGLE. On even generations, it will always choose either -BALL_MAX_ANGLE or
        BALL_MAX_ANGLE with no intermediate values.

        Args:
            gen_num (int): the generation number
        """
        ball_slope = self.y_velocity / self.x_velocity
        collision_y = self.y + ball_slope * (SCREEN_WIDTH - PADDLE_DIST_FROM_EDGE - PADDLE_WIDTH - (self.x + BALL_RADIUS))
        self.x = SCREEN_WIDTH - PADDLE_DIST_FROM_EDGE - PADDLE_WIDTH - BALL_RADIUS
        self.y = collision_y

        angle = random.randrange(-BALL_MAX_ANGLE, BALL_MAX_ANGLE) + 180
        self.x_velocity = math.cos(math.radians(angle)) * BALL_START_SPEED
        self.y_velocity = math.sin(math.radians(angle)) * BALL_START_SPEED

    def collision_left(self):
        """If the ball were to collide with the left side, returns the ball's collision location.

        Returns:
            float: where the ball hit the wall.
        """
        ball_slope = self.y_velocity / self.x_velocity
        collision_y = self.y + ball_slope * (PADDLE_DIST_FROM_EDGE + PADDLE_WIDTH + BALL_RADIUS - (self.x - BALL_RADIUS))
        return collision_y

    def update(self):
        """Moves ball and calls appropriate collision functions. Returns center of ball collision if trial is over.

        Args:
            gen_num (int): the generation number

        Returns:
            float: where the ball collides with the left wall.
        """
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


def do_trial(neural_nets, _):
    """_summary_

    Args:
        neural_nets (list[NeuralNetwork]): list of neural networks to play the game
        gen_num (int): generation number
        _ : dummy variable given by multiprocessing.map

    Returns:
        list[float]: A list of reward values for each neural network determined by the distance to the ball's collision
        location.
    """
    ball = Ball()
    angle = math.degrees(math.atan(ball.y_velocity / ball.x_velocity))
    paddle_y = ball.y - angle / BALL_MAX_ANGLE * (PADDLE_HEIGHT / 2 + BALL_RADIUS) - PADDLE_HEIGHT / 2

    paddles = [paddle_y for _ in range(len(neural_nets))]
    # do frames until the ball gets back to the wall
    while True:
        for i in range(len(neural_nets)):
            inp = [ball.x, ball.y, ball.x_velocity, ball.y_velocity, paddles[i] + PADDLE_HEIGHT / 2] 
            up, down = neural_nets[i].run(inp)
            if up > 0 and not down > 0:
                paddles[i] = max(paddles[i] - PADDLE_SPEED, 0)
            if down > 0 and not up > 0:
                paddles[i] = min(paddles[i] + PADDLE_SPEED, SCREEN_HEIGHT - PADDLE_HEIGHT)
        ball_update = ball.update()
        if ball_update is not None:
            # reward closer paddles more heavily
            rewards = [1 - abs(paddle + PADDLE_HEIGHT / 2 - ball_update) / SCREEN_HEIGHT for paddle in paddles]
            return rewards


if __name__ == '__main__':
    best_nn = None
    best_score = -math.inf

    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    
    # starting networks
    games = [NeuralNetwork() for _ in range(NUM_AGENTS)]
    
    for gen in range(GENERATIONS):
        # get rewards for each network. This will use ALL of your CPU for the duration of the runtime.
        rewards = pool.map(partial(do_trial, games), range(TRIALS_PER_GEN))
        # create game_score objects to sort and rank by.
        game_scores = [[game, 0] for game in games]
        for reward in rewards:
            for i in range(len(reward)):
                game_scores[i][1] += reward[i]
            
        game_scores.sort(key=lambda game: game[1], reverse=True)
        if game_scores[0][1] > best_score:
            best_score = game_scores[0][1]
            best_nn = game_scores[0][0]
            # save champion
            with open('champion.pickle', 'wb') as f:
                pickle.dump(best_nn, f)
        
        new_games = []

        print(f'Generation {gen + 1} results')
        for i in range(SELECT_NUM):
            print(game_scores[i][1])
            new_games.append(game_scores[i][0])
        print('============================')
        sys.stdout.flush()
        
        # create next generation using tournament selection
        while len(new_games) < NUM_AGENTS - RANDOM_NETWORKS_PER_GEN:
            parent_1_options = random.sample(game_scores, TOURNAMENT_SIZE)
            parent_2_options = random.sample(game_scores, TOURNAMENT_SIZE)

            parent1 = max(parent_1_options, key=lambda x: x[1])
            parent2 = max(parent_2_options, key=lambda x: x[1])
            if parent1 == parent2:
                continue
            crossover_child = crossover(parent1[0], parent2[0])
            new_games.append(crossover_child)

        for i in range(RANDOM_NETWORKS_PER_GEN):
            new_games.append(NeuralNetwork())
        games = new_games
        # save winner from last generation
        with open('last_gen.pickle', 'wb') as f:
            pickle.dump(games[0], f)

    pool.close()
    
