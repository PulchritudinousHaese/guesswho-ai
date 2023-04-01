"""CSC111 Winter 2023 Project: Guess Who Artificial Intelligence
This module contains the subclassess AI from parent class AI (Player) in guess_who.py and the
necessary functions to backend of the classic game "Guess Who".
This file is Copyright (c) 2023 Annie Wang, Mikhail Skazhenyuk, Xinyuan Gu, Ximei Lin.
"""
from guess_who import Player, GuessWho
import guess_who
import csv
import random
import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import dataclass

from typing import Optional
from features import *

import tkinter as tk

########################################################################

class GreedyPlayer(Player):
    """ A player who has the higher winning probability in the game.
    Instance Attributes:
        - name: name of the type of player in the game.
        - spy: the spy that the player has chosen.
    """
    def __init__(self, candidates: dict[str, dict[str, str]], questions: list[str]):
        Player.__init__(self, candidates, questions, 'GreedyPlayer')

    def make_guesses(self, game: GuessWho) -> str:
        """ The player makes a guess of the name of the opponent's spy at the end of the game."""

        for name in self.candidates:
            return name

    def ask_questions(self, game: GuessWho) -> str:
        """ The player asks question about the characterstics of the spy based on the current state of the game. The
        method mutates questions and candidates by removing the question and candodate that the player
        has already chosen.
         Preconditions:
            - game._whose_turn() == self.n
        """
        scores = []
        for q in self.questions:
            count_y = 0
            count_n = 0
            for v in self.candidates.values():
                if v[q] == "Y":
                    count_y += 1
                else:
                    count_n += 1
            scores.append(abs(count_y - count_n))
        min_score = min(scores)
        min_index = scores.index(min_score)
        question = self.questions[min_index]
        self.eliminate_question(question)
        return question


#@check_contract
class RandomPlayer(Player):
    """ A player who randomly asks question without using a strategy.
    """
    def __init__(self, candidates: dict[str, dict[str, str]], questions: list[str]):
        Player. __init__(self, candidates, questions, 'RandomPlayer')

    def make_guesses(self, game: GuessWho) -> str:
        """ The player makes a guess of the name of the opponent's spy at the last round of the game.
        Precondition:
            - len(self.candidates) == 1
        """
        for name in self.candidates:
            return name

    def ask_questions(self, game: GuessWho) -> str:
        """ A player randomly asks questions based on the current state of game.
         Preconditions:
            - game._whose_turn() == self.n
        """
        question = random.choice(self.questions)
        self.eliminate_question(question)
        return question


class PoorPlayer(Player):
    """ A player who deliberately chooses the worst qurestion.
    """
    def __init__(self, candidates: dict[str, dict[str, str]], questions: list[str]):
        Player.__init__(self, candidates, questions, 'PoorPlayer')

    def make_guesses(self, game: GuessWho) -> str:
        """ The player makes a guess of the name of the opponent's spy at the last round of the game.
        Precondition:
            - len(self.candidates) == 1
        """
        for name in self.candidates:
            return name

    def ask_questions(self, game: GuessWho) -> str:
        """ A player randomly asks questions based on the current state of game.
         Preconditions:
            - game._whose_turn() == self.n
        """
        scores = []
        for q in self.questions:
            count_y = 0
            count_n = 0
            for v in self.candidates.values():
                if v[q] == "Y":
                    count_y += 1
                else:
                    count_n += 1
            scores.append(abs(count_y - count_n))

        max_score = max(scores)
        max_index = scores.index(max_score)
        question = self.questions[max_index]
        self.eliminate_question(question)
        return question


def plot_game_statistics(result: dict[str, list[int]], player1: str, player2: str) -> None:
    """ Plot the game results from the given list of games and players results. x-axis represents the num_games.
    y-axis shows the winning state of each pleyer (0=lost, 1=won)
     Results is a dictionary contaiting the number of games recorded and the results from each game. Each keys
     represent what values are recorded in the corresponding values in terms of list.
     Values of results[num_games] shows which games are recoded. Values of results[player1] and results[player2] show
     if each player won in each game.
     For example if index 0 at results[num_games] is 1, results[player1][0] and results[player2][0] are the
     results of the first game: player 1 lost(if results[player1][0] = 0) and player2 won (if results[player2][0] =1).
     Names of player1 and player 2 are determined by who is playing.
    Preconditions:
     - len(results[num_games]) >= 1
     - len(results[num_games]) == len(results[player1]) == len(results[player2])
     - all(isinstance(key,str) for key in results)
     """
    df = pd.DataFrame(result)
    ax1 = df.plot(kind='scatter', x='num_games', y=player1, color='r', label=player1)
    df.plot(kind='scatter', x='num_games', y=player2, color='g', label=player2, ax=ax1)
    ax1.set_xlabel('number_of_games')
    ax1.set_ylabel('results (0 = lost) (1 = won)')
    plt.show()


def run_game(players: list[Player], candidates: dict[str, dict[str, str]]) -> str:
    """Run a GuessWho game between the two given players and returns the winner at the end of the game.
       Use candidates as the candidates_questions dictionary in the game.
       Preconditions:
        - candidates is not an empty dictionary.
    """

    player1 = players[0]
    player2 = players[1]
    game = GuessWho(players, candidates)
    p1_question = game.players[1].questions
    p2_question = game.players[2].questions
    while len(player1.candidates) != 1 and len(player2.candidates) != 1 and p1_question != [] and p2_question != []:
        question1 = player1.ask_questions(game)
        answer1 = game.return_answer(question1, 2)
        player1.eliminate_candidates(question1, answer1)
        question2 = player2.ask_questions(game)
        answer2 = game.return_answer(question2, 1)
        player2.eliminate_candidates(question2, answer2)

    guess1 = player1.make_guesses(game)
    guess2 = player2.make_guesses(game)

    return game.get_winner(guess1, guess2)


def run_games(num: int,  players: list[Player], num_cha: int, file: csv, plot: bool = False, p: bool = False) -> dict:
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
        can = Guess_who.create_candidates(file, num_cha)
        question = Guess_who.generate_all_possible_questions(file)
        player1.candidates = can
        player2.candidates = can.copy()
        player1.questions = question
        player2.questions = question.copy()
        player1.select_spy()
        player2.select_spy()
        winner = run_game([player1, player2], can.copy())
        if winner == player1.name or winner == player2.name:
            game_sta[winner] += 1
            results[winner][i] = 1
    if p:
        pl1_wins = game_sta[pl1_name]
        pl2_wins = game_sta[pl2_name]
        print(f'[winning_probability:{pl1_name}: {(pl1_wins/num) * 100}%, {pl2_name}: {(pl2_wins/num) * 100}%]')
    if plot:
        plot_game_statistics(results, player1.name, player2.name)

    return results



if __name__ == '__main__':
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'max-nested-blocks': 4,
    #     'extra-imports': ['random', 'a2_adversarial_wordle', 'a2_game_tree'],
    #     'allowed-io': ['run_learning_algorithm']
    # })
    candidates = guess_who.create_candidates('data/questions.csv', 12)
    candidates1 = candidates.copy()
    candidates2 = candidates.copy()
    questions = guess_who.generate_all_possible_questions('data/questions.csv')
    player1 = GreedyPlayer(candidates, questions)
    player2 = RandomPlayer(candidates1, questions)
    run_games(100, [player1, player2], 12, 'data/questions.csv', True, True)

    
   
