import numpy as np
from typing import Union

INPUT_NODES = 4
HIDDEN_LAYER_NODES = [4]  # use empty list for no hidden layers
OUTPUT_NODES = 1

class NeuralNetwork:
    def __init__(self):
        """
        Initializes neural network with parameters set to the static variables declared at the top of the file
        """
        previous_layer_nodes = INPUT_NODES
        self.weights = []
        self.biases = []
        for i in range(len(HIDDEN_LAYER_NODES)):
            self.weights.append(np.random.uniform(-1, 1, size=(previous_layer_nodes, HIDDEN_LAYER_NODES[i])))
            self.biases.append(np.random.uniform(-1, 1, size=HIDDEN_LAYER_NODES[i]))
            previous_layer_nodes = HIDDEN_LAYER_NODES[i]
        self.weights.append(np.random.uniform(-1, 1, size=(previous_layer_nodes, OUTPUT_NODES)))
        self.biases.append(np.random.uniform(-1, 1, size=OUTPUT_NODES))

    def run(self, data: list[int]) -> Union[int, list[int]]:
        """Runs data through the neural network and returns the value in the output node(s)

        Args:
            data (list[int]): single dimension array containing each input as its own cell

        Returns:
            Union[int, list[int]]: int or array of ints representing the output value for each cell.
        """
        for i in range(len(self.weights)):
            data = np.matmul(data, self.weights[i]) + self.biases[i]
            if i != len(self.weights) - 1:
                data = np.maximum(data, np.zeros_like(data))
        return data[0] if len(data) == 1 else data


if __name__ == '__main__':
    for i in range(1000):
        nn = NeuralNetwork()
        print(nn.run([0, 0, 0, 0]))