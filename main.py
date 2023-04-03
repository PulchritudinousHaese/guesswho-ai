"""CSC111 Winter 2023 Project: Guess Who Artifical Intelligence
This module contains the classes and necessary functions to execute
the frontend with the backend of the classic game "Guess Who".

The files interface.py and guess_who.py are combined in this file to work together.
artifical_intelligence is provided to play against as an opponent and the player
may choose which opponent to play against.

This file also contins the main function to run games and test performaces between AIs.
"""
from __future__ import annotations

import csv
from tkinter import *

import guess_who as GW
from guess_who import Player

import artificial_intelligence as AI
from artificial_intelligence import RandomPlayer, GreedyPlayer, PoorPlayer

import interface as IF

GAME_SETTINGS = {'question': ''}


###########################################################
# main function to run games and test performances between the GuessWho AIs that we've defined.
###########################################################
def run_games(num: int, players: list[Player], num_cha: int, file: csv, plot: bool = False, p: bool = False) -> dict:
    """ Run GuessWho num times between player1 and player2 with characters in file and num_cha of characters .
     The function returns the results of each game.

        Optional Parameter:
        - plot: determines if the user wants to plot the game results in graph
        - p: determines if the user wants to print out the winning probability of each player
        Preconditions:
        - file is a non-empty file with questions and answers related to characteristics of each character
        at each line
    """
    default = [0] * num
    default1 = default.copy()
    player1 = players[0]
    player2 = players[1]
    pl1_name = players[0].name
    pl2_name = players[1].name
    results = {'num_games': [n for n in range(1, num + 1)], pl1_name: default, pl2_name: default1}
    game_sta = {players[0].name: 0, players[1].name: 0}
    for i in range(0, num):
        can = GW.create_candidates(file, num_cha)
        question = GW.generate_all_possible_questions(file)
        player1.candidates = can
        player2.candidates = can.copy()
        player1.questions = question
        player2.questions = question.copy()
        player1.select_spy()
        player2.select_spy()
        winner = AI.run_game([player1, player2], can.copy())
        if winner == player1.name or winner == player2.name:
            game_sta[winner] += 1
            results[winner][i] = 1
    if p:
        pl1_wins = game_sta[pl1_name]
        pl2_wins = game_sta[pl2_name]
        print(f'[winning_probability:{pl1_name}: {(pl1_wins / num) * 100}%, {pl2_name}: {(pl2_wins / num) * 100}%]')
    if plot:
        AI.plot_game_statistics(results, player1.name, player2.name)

    return results


if __name__ == "__main__":
    IF.initiate()

if __name__ == '__main__':
    pass
    # candidates = guess_who.create_candidates('data/questions.csv', 12)  # Define data to initialize two players
    # candidates1 = candidates.copy()
    # questions = guess_who.generate_all_possible_questions('data/questions.csv')

    # Sample call to run GuessWho 100 times between GreedyPlayer and PoorPlayer.
    # You may change the first parameter in run_games to determine how many games you would like to run.
    # You may change the last two parameters False, to not print out the winning probability of
    # each player(last parameter), or to not plot the game results(second last parameter).
    # player1 = GreedyPlayer(candidates, questions)
    # player2 = PoorPlayer(candidates1, questions)
    # run_games(100, [player1, player2], 12, 'data/questions.csv', True, True)
    # You can see GreedyPlayer has obviously better performance.

    # Below is a Sample call to run GuessWho 100 times with same setting, but between GreedyPlayer
    # and RandomPlayer.
    # player1 = GreedyPlayer(candidates, questions)
    # player2 = RandomPlayer(candidates1, questions)
    # run_games(100, [player1, player2], 12, 'data/questions.csv', True, True)

    # You should notice a more nuanced difference between the performance of RandomPlayer and GreedyPlayer
    # and the performance of PoorPlayer and GreedyPlayer. Sometimes GreedyPlayer and RandoPlayer may even have the same
    # winning probability!

    # import python_ta
    #
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'extra-imports': ['tkinter', 'guess_who', 'features', 'artificial_intelligence', 'csv', 'interface'],
    #     'disable': ['forbidden-top-level-code',
    #                 'wildcard-import',
    #                 'too-many-branches',
    #                 'forbidden-global-variables',
    #                 'unused-argument',
    #                 'too-many-arguments',
    #                 'too-many-locals',
    #                 'unused-import'
    #                 ],
    #     'allowed-io': []
    # })
