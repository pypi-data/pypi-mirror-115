"""
PythonAI - dep
v 0.0.1
By: Spidey Zac

PythonAI GeneticAlgorithm file
"""

__version__ = "0.0.1"

from typing import Callable
import numpy as np
from random import uniform as random

from NeuralNetwork import NeuralNetwork

randmatrix = np.random.uniform
floor = np.math.floor

class GeneticAlgorithm(NeuralNetwork):
    '''
    Genetic Algorithm Class
    '''

    def crossover(self, parent2: 'GeneticAlgorithm', crossover: Callable) -> 'GeneticAlgorithm':
        '''
        Creates an offspring using the specified crossover function
        '''

        return crossover(self, parent2)

    def mutate(self) -> None:
        '''
        Mutates this Genetic Algorithm
        '''

        for i in range(len(self.weights)):
            for j in range(len(self.weights[i])):
                for k in range(len(self.weights[i][j])):
                    self.weights[i][j][k] += random(-1, 1)

        for i in range(len(self.biases)):
            for j in range(len(self.biases[i])):
                for k in range(len(self.biases[i][j])):
                    self.biases[i][j][k] += random(-1, 1)

def RandomCrossover(parent1: GeneticAlgorithm, parent2: GeneticAlgorithm) -> GeneticAlgorithm:
    '''
    Crossover Function

    %50 Chance to inherit from either parent
    '''

    child = GeneticAlgorithm(parent1.network)
    child.weights = parent1.weights
    child.biases = parent1.biases

    for i in range(len(child.weights)):
        for j in range(len(child.weights[i])):
            for k in range(len(child.weights[i][j])):
                if random(0, 1) <= 0.5:
                    child.weights[i][j][k] = parent2.weights[i][j][k]

    for i in range(len(child.biases)):
        for j in range(len(child.biases[i])):
            for k in range(len(child.biases[i][j])):
                if random(0, 1) <= 0.5:
                    child.weights[i][j][k] = parent2.biases[i][j][k]

    return child

def HalfCrossover(parent1: GeneticAlgorithm, parent2: GeneticAlgorithm) -> GeneticAlgorithm:
    '''
    Crossover Function

    Takes half the genes from each parent
    '''

    child = GeneticAlgorithm(parent1.network)
    child.weights = parent1.weights
    child.biases = parent1.biases

    for i in range(len(child.weights)):
        for j in range(len(child.weights[i])):
            for k in range(len(child.weights[i][j])):
                if k > len(child.weights[i][j]) // 2:
                    child.weights[i][j][k] = parent2.weights[i][j][k]

    for i in range(len(child.biases)):
        for j in range(len(child.biases[i])):
            for k in range(len(child.biases[i][j])):
                if k > len(child.weights[i][j]) // 2:
                    child.weights[i][j][k] = parent2.biases[i][j][k]

    return child

def SliceCrossover(parent1: GeneticAlgorithm, parent2: GeneticAlgorithm) -> GeneticAlgorithm:
    '''
    Crossover Function

    Picks a random area from parent2 to inherit from
    '''

    child = GeneticAlgorithm(parent1.network)
    child.weights = parent1.weights
    child.biases = parent1.biases

    for i in range(len(child.weights)):
        for j in range(len(child.weights[i])):
            k_low = floor(random(0, len(child.weights[i][j])))
            k_max = floor(random(k_low, len(child.weights[i][j])))
            for k in range(len(child.weights[i][j])):
                if k >= k_low and k < k_max:
                    child.weights[i][j][k] = parent2.weights[i][j][k]

    for i in range(len(child.biases)):
        for j in range(len(child.biases[i])):
            for k in range(len(child.biases[i][j])):
                if k >= k_low and k < k_max:
                    child.weights[i][j][k] = parent2.biases[i][j][k]

    return child