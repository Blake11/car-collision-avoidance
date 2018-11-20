import pygame
from numpy import exp, random, dot, array, append

from colors import *
from consts import SCREEN_HEIGHT, SCREEN_WIDTH
from player import Car


class NeuralNetwork():
    def __init__(self):
        # Seed the random number generator, so it generates the same numbers
        # every time the program runs.
        random.seed(1)

        # We model a single neuron, with 3 input connections and 1 output connection.
        # We assign random weights to a 3 x 1 matrix, with values in the range -1 to 1
        # and mean 0.
        self.synaptic_weights = 2 * random.random((2, 1)) - 1

    # The Sigmoid function, which describes an S shaped curve.
    # We pass the weighted sum of the inputs through this function to
    # normalise them between 0 and 1.
    def __sigmoid(self, x):
        return 1 / (1 + exp(-x))

    # The derivative of the Sigmoid function.
    # This is the gradient of the Sigmoid curve.
    # It indicates how confident we are about the existing weight.
    def __sigmoid_derivative(self, x):
        return x * (1 - x)

    # We train the neural network through a process of trial and error.
    # Adjusting the synaptic weights each time.
    def train(self, training_set_inputs, training_set_outputs, number_of_training_iterations):
        for iteration in range(number_of_training_iterations):
            # Pass the training set through our neural network (a single neuron).
            output = self.think(training_set_inputs)

            # Calculate the error (The difference between the desired output
            # and the predicted output).
            error = training_set_outputs - output

            # Multiply the error by the input and again by the gradient of the Sigmoid curve.
            # This means less confident weights are adjusted more.
            # This means inputs, which are zero, do not cause changes to the weights.
            adjustment = dot(training_set_inputs.T, error * self.__sigmoid_derivative(output))

            # Adjust the weights.
            self.synaptic_weights += adjustment

    # The neural network thinks.
    def think(self, inputs):
        # Pass inputs through our neural network (our single neuron).
        return self.__sigmoid(dot(inputs, self.synaptic_weights))


neural_network = NeuralNetwork()
"Training data: Distanta, same lane"
training_set_inputs = array([[100, 0], [100, 1], [100, 0], [100, 1]])

training_set_outputs = array([[0, -1, 0, -1]]).T

pygame.init()

screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
bg = pygame.image.load("bg.png")

pygame.display.set_caption('AI')
fps = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 15)

ai = Car(BLUE, 1, "buttom")
car = Car(RED, 1, "top")

result = [0]
while True:
    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    if pygame.key.get_pressed()[pygame.K_LEFT] or result[0] > 0.1:
        ai.move("left")
    elif pygame.key.get_pressed()[pygame.K_RIGHT] or result[0] <= 0.1:
        ai.move("right")

    # move handler
    car.move("down")

    same_lane = 1 if ai.is_same_lane(car) else 0

    distance = ai.distance(car)

    # clear the screen before drawing
    screen.blit(bg, (0, 0))  # start new frame
    # drawing goes below
    ai.draw(screen)

    car.draw(screen)

    pygame.display.update()
    fps.tick(60)

    inputs = array([distance, same_lane])

    neural_network.train(training_set_inputs, training_set_outputs, 1000)

    result = neural_network.think(array(inputs))

    print(result)
