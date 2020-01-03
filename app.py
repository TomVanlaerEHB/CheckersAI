from checkers.game import Game
from ast import literal_eval
from data import *
from keras.models import Sequential
from keras.layers import Dense

import json
import matplotlib.pyplot as plt

game = Game()

print_board(game.board)

import config

model = Sequential([
    Dense(units=64, activation='relu', input_dim=30),
    Dense(units=10, activation='relu'),
    Dense(units=2, activation='softmax')
])

print(game.is_over())

while not game.is_over():
    print("Player {} is at play".format(game.whose_turn()))
    game.get_possible_moves()
    action = input('Enter your chosen action: ')