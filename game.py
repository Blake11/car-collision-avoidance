from random import randint, uniform

import numpy as np
import pygame

from colors import *
from consts import SCREEN_HEIGHT, SCREEN_WIDTH
from network import NeuralNetwork
from player import Car

"""Add a neural network"""
neural_network = NeuralNetwork()

# print("Beginning Randomly Generated Weights: ")
# print(neural_network.synaptic_weights)

"""
    Training data consisting of 4 examples--3 input values and 1 output 
    input data format: distance, is same lane
    output: 1 if distance is bigger that 250.0 and is on the same lane
            of if they are on different lanes
            0 otherwise
"""
batch_size = 100
training_iterations = 1500
"""Make a random input with the format of [distance, is_same_lane]
ex D= Distance S=Same Lane  O=output
D   S   L   R
200 1   0   1
50  1   1   1
25  1   1
0   1   1
200 0   0
100 0   0
50  0   0
25  0   0

"""


def get_input():
    """
    Generate a random input with the following format

    :return: [distance,lane number, is same lane]
    """

    distance = uniform(0, SCREEN_HEIGHT * 2)
    lane_number = randint(1, 3)
    same_lane = randint(0, 1)

    return [distance, lane_number, same_lane]


def eval_input(in_layer):
    """
    Evaluate a given input and return the correct move

    :param in_layer: [distance,lane number, is same lane]
    :return: [L,R] where only L or R is 1 but not both (ex [0,1] or [1,0])

    list(map(lambda x: 1 if x[1] == 1 or (x[1] == 1 and x[0] != inf) else 0
    """

    distance = in_layer[0]
    lane_number = in_layer[1]
    is_same_lane = in_layer[2]
    print(is_same_lane)

    if distance < 350:
        if is_same_lane:
            if lane_number == 1:
                return [0, 1]
            if lane_number == 2:
                pos = randint(0, 1)
                arr = [0, 0]
                arr[pos] = 1
                return arr
            if lane_number == 3:
                return [1, 0]
        else:
            return [0, 0]
    else:
        return [0, 0]


random_input = [get_input() for _ in range(batch_size)]
correct_outputs = []

for inp in random_input:
    output = eval_input(inp)
    correct_outputs.append(output)

training_inputs = np.array(random_input)
training_outputs = np.array(correct_outputs)

print(training_inputs, training_outputs, sep="\n")

# training taking place
neural_network.train(training_inputs, training_outputs, training_iterations)

# print("Ending Weights After Training: ")
# print(neural_network.synaptic_weights)

"""Initiate pygame specific code"""
pygame.init()

screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
bg = pygame.image.load("bg.png")

pygame.display.set_caption('AI')
fps = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 15)

ai = Car(BLUE, 1, "buttom")
car = Car(RED, 1, "top")

"""Game loop"""
left, right = 0, 0
while True:
    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    if pygame.key.get_pressed()[pygame.K_LEFT]:
        ai.move("left")
    elif pygame.key.get_pressed()[pygame.K_RIGHT]:
        ai.move("right")

    if left > right:
        ai.move("left")
        lane_text = "left"
    elif left < right:
        ai.move("right")
        lane_text = "right"
    else:
        lane_text = "NU MISCA BA"
    # move handler
    car.move("down")

    lane = ai.get_lane()

    same_lane = 1 if ai.is_same_lane(car) else 0

    distance = ai.distance(car)

    # clear the screen before drawing
    screen.blit(bg, (0, 0))  # start new frame
    # drawing goes below
    ai.draw(screen)

    car.draw(screen)

    pygame.display.update()
    fps.tick(60)

    inputs = np.array([distance, lane, same_lane])

    prediction = neural_network.think(np.array(inputs))

    print(inputs, prediction, lane_text, sep=" ")
    left = prediction[0]
    right = prediction[1]

