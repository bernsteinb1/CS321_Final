import numpy as np
from typing import Union
import time
from copy import deepcopy
import random

INPUT_NODES = 6
HIDDEN_LAYER_NODES = [4]  # use empty list for no hidden layers
OUTPUT_NODES = 2

MUTATION_RATE = .05
REPLACEMENT_RATE = .005
STD = .01

class NeuralNetwork:
    def __init__(self):
        """
        Initializes neural network with parameters set to the static variables declared at the top of the file
        """
        previous_layer_nodes = INPUT_NODES
        self.weights = []
        self.biases = []
        # initialize weights and biases randomly between -1 and 1 with a uniform distribution
        for i in range(len(HIDDEN_LAYER_NODES)):
            self.weights.append(np.random.uniform(-1, 1, size=(previous_layer_nodes, HIDDEN_LAYER_NODES[i])))
            self.biases.append(np.random.uniform(-1, 1, size=HIDDEN_LAYER_NODES[i]))
            previous_layer_nodes = HIDDEN_LAYER_NODES[i]
        self.weights.append(np.random.uniform(-1, 1, size=(previous_layer_nodes, OUTPUT_NODES)))
        self.biases.append(np.random.uniform(-1, 1, size=OUTPUT_NODES))

    def run(self, data: list[float]) -> Union[float, list[float]]:
        """Runs data through the neural network and returns the value in the output node(s)

        Args:
            data (list[float]): single dimension array containing each input as its own cell

        Returns:
            Union[float, list[float]]: float or array of floats representing the output value for each cell.
        """
        # run data through each layer applying ReLU at all cells except for the final cell
        for i in range(len(self.weights)):
            data = np.matmul(data, self.weights[i]) + self.biases[i]
            if i != len(self.weights) - 1:
                data = 1/ (1 + np.exp(-data))
        return data[0] if len(data) == 1 else data
    
    def mutate(self):
        new_network = deepcopy(self)
        for i in range(len(new_network.weights)):
            adjustments = np.zeros_like(new_network.weights[i])
            for row in adjustments:
                for j in range(len(row)):
                    if random.random() < MUTATION_RATE:
                        row[j] = random.uniform(-1, 1) if random.random() < REPLACEMENT_RATE else row[j] + np.random.normal(0, STD)
            new_network.weights[i] += adjustments

            adjustments = np.zeros_like(new_network.biases[i])
            for j in range(len(adjustments)):
                if random.random() < MUTATION_RATE:
                    adjustments[j] = random.uniform(-1, 1) if random.random() < REPLACEMENT_RATE else adjustments[j] + np.random.normal(0, STD)
            new_network.biases[i] += adjustments
            
        return new_network

# TODO: actually use the parents chosen in this function
def crossover(games):
    # softmax
    fitness_scores = np.array([game.score for game in games])
    # networks = [game.left_ai for game in games]
    exp_fitness = np.exp(fitness_scores)
    probabilities = exp_fitness / np.sum(exp_fitness)

    # need to do this more than once?
    parent1 = np.random.choice(games, p=probabilities)
    parent2 = np.random.choice(games, p=probabilities)
    print("parent 1 score:", parent1.score, "parent 2 score:", parent2.score)

    # i think using len of HIDDEN_LAYER_NODES gives number of weights
    num_weights = len(HIDDEN_LAYER_NODES)
    pivot = random.randrange(0, num_weights)

    # need to use selected parents to create new child
    # try single/one point crossover for now



if __name__ == '__main__':
    networks = [NeuralNetwork() for _ in range(1000)]
    start = time.time()
    for i in range(1000):
        print(networks[i].run([5]))
    print()
    print(time.time() - start)