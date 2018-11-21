from math import inf
from random import randint

import pygame

from consts import *


class Car:
    lane = None

    def __init__(self, color, lane, position):
        self.speed = CAR_SPEED
        self.color = color
        self.lane = lanes[lane]

        if position == "buttom":
            self.height = SCREEN_HEIGHT * 0.75
        if position == "top":
            self.height = SCREEN_HEIGHT * - 0.1

        self.shape = pygame.Rect(self.lane, self.height, CAR_WIDTH, CAR_HEIGHT)

    @staticmethod
    def random_lane():
        return lanes[randint(0, 2)]

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.shape)

    def reset(self):
        self.lane = Car.random_lane()
        self.height = SCREEN_HEIGHT * -0.1
        self.shape = pygame.Rect(self.lane, self.height, CAR_WIDTH, CAR_HEIGHT)

    def move(self, direction):
        """
        Move the player in a given direction
        :param direction: "left", "right", "up", "down"
        :return: None
        """

        if direction == "left":
            if self.shape.left > 0:
                self.shape = self.shape.move(-self.speed, 0)
        elif direction == "right":
            if self.shape.right < SCREEN_WIDTH:
                self.shape = self.shape.move(self.speed, 0)
        elif direction == "down":
            if self.shape.bottom < SCREEN_HEIGHT * 1.2 + CAR_HEIGHT:
                self.shape = self.shape.move(0, self.speed)
            else:
                self.reset()
        elif direction == "up":
            if self.shape.top > 0:
                self.shape = self.shape.move(0, -self.speed)

    def distance(self, other_car):
        distance = inf
        distance = self.shape.top - other_car.shape.bottom

        if distance < 0:
            distance = inf

        return distance

    def get_lane(self):
        return (self.shape.centerx-10)/SCREEN_WIDTH*10//3 + 1

    def is_same_lane(self, other_car):
        if self.shape.centerx > other_car.shape.centerx + CAR_WIDTH or self.shape.centerx < other_car.shape.centerx - CAR_WIDTH:
            return False
        else:
            return True
