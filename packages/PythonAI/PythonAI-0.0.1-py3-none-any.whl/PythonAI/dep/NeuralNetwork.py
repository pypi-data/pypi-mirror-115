"""
PythonAI - dep
v 0.0.1
By: Spidey Zac

PythonAI NeuralNetwork file
"""

__version__ = "0.0.1"

import numpy as np

randmatrix = np.random.uniform

class NeuralNetwork:
    '''
    Base class for all Neural Networks
    '''

    def __init__(self, network: list[int]) -> None:
        if len(network) < 2:
            raise Exception("Network Must Have At Least Two Layers")

        for i in range(len(network)):
            if network[i] <= 0:
                raise Exception("Network Layer {} Cannot have a size of 0 or less".format(i))

        self.network = network

        self.weights = np.zeros(len(network) - 1).tolist()
        self.biases = np.zeros(len(network) - 1).tolist()

        for i in range(len(network) - 1):
            self.weights[i] = randmatrix(-1, 1, (network[i + 1], network[i]))

        for i in range(1, len(network)):
            self.biases[i - 1] = randmatrix(-1, 1, (network[i], 1))

    def activation_function(self, x):
        return 1 / (1 + np.math.exp(-x))

    def feedForward(self, inputs: list[float]) -> float:
        '''
        Uses the feed forward algorithm to get outputs from the neural network
        '''

        ins = np.zeros((len(inputs), 1))
        for i in range(len(inputs)):
            ins[i][0] = inputs[i]

        inputs = ins

        for i in range(len(self.weights)):
            inputs = np.matmul(self.weights[i], inputs)
            inputs = np.add(inputs, self.biases[i])

            for j in range(len(inputs)):
                for k in range(len(inputs[j])):
                    inputs[j][k] = self.activation_function(inputs[j][k])

        return inputs.flatten()