"""CSC111 Winter 2023 Project: Guess Who Artifical Intelligence
This module contains the classes and necessary functions to execute
the backend of the classic game "Guess Who".
Some features:
https://chalkdustmagazine.com/blog/cracking-guess-board-game/
All characters:
https://www.joe.co.uk/life/ranking-guess-who-least-most-horny-193991

This file is Copyright (c) 2023 Annie Wang, Mikhail Skazhenyuk, Xinyuan Gu, Ximei Lin.
"""
from __future__ import annotations

import csv
import random
import copy
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from typing import Optional, Any

import plotly
import tkinter as tk
from game_tree import GameTree

from features import *
from dataclasses import dataclass

########################################################################

def load_person(person_tuple: tuple[str]) -> Person:
    """Returns a Person from the defined string of characteristics.
    Preconditions:
    - len(person_tuple) == 9
    """
    p = person_tuple
    features_so_far = set()
    for p in person_tuple[1:]:
        features_so_far.add(p)
    person = Person(p[0], features_so_far)
    return person


def load_persons(file_name: str) -> list[Person]:
    """Function to load all features into a list of Person classes
    as determined in the file file_name.
    Precondition:
    - file_name != ''
    """
    persons_so_far = []

    with open(file_name) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            row = tuple(row)
            person = load_person(row)
            persons_so_far.append(person)

    return persons_so_far


########################################################################

# TODO: Finish attributes, initializer, determine functions necessary
@dataclass
class Person:
    """The main class to represent each person in the game of GuessWho.
  Instance Attributes:
  - name: The person's name (for the final guess)
  - features: A set of all the person's features
  - up: Boolean whether the person has been guessed/eliminated or not.
  Representation Invariants:
  - self.features != set()
  """
    name: str
    features: set[str]
    up: bool

    def __init__(self, name: str, features: set[str], up: bool = True) -> None:
        """Initialize Person with given Instance Attributes. """

        self.name = name
        self.features = features
        self.up = up
        
        
# TODO: Attributes, initializer, determine functions necessary
class GuessWho:
    """The main class to run the game of GuessWho and represent its game_state.
    Instance Attributes:
    - guesses: A list representing the moves made by both players in order.
    - spies: A list representing the spies of each player (index 0 for player one, index 1 for player two)
    - players: A list of the players in the game
    Representation Invariants:
    - len(spies) == 2
    - spy is a valid person from the given file
     """
    players: dict[int, Player]
    process: list[str]
    characters: dict[str, dict[str,str]]

    def __init__(self, players: list[Player], characters_questions_file: str) -> None:
        """ Initialize a GuessWho game with the two players"""
        self.characters = create_candidates(characters_questions_file)
        self.players = {1: players[0], 2: players[1]}

    def get_winner(self, guess1, guess2) -> Optional[str]:
        """ return if there is a winner in the game and which player is the winner, with the guess1 by player1
        and guess2 by player2. Guess1 is the guess made by player1 and guess2 is the guess by player2. There is a tie if both guessers have guessed
        the spy of the opponent.
        """
        if (guess1 == self.players[1].spy) and (guess2 == self.players[2].spy):
           return 'tie'
        if guess2 == self.players[1].spy:
           return self.players[2].name
        elif guess1 == self.players[2].spy:
           return self.players[1].name

    def whose_turn(self) -> int:
        """ return it's which player's turn to make a guess in this round of game"""
        if len(self.process) % 2 == 0:
            return 2
        else:
            return 1
    def return_answer(self, question: str, player_num: int) -> str:
        """ Answer yes or no to the questiont that one player has asked, regarding the spy that player_num has chosen"""
        veridy_with = self.players[player_num]
        return self.candidates[veridy_with.spy][question]


# dict_categories_to_features = {ear_size:, [BIGEARS, SMALLEARS], \
#     hair_style: [STRAIGHT, CURLY, WAVY], \
#     hair_length: [LONGHAIR, MEDIUMHAIR, SHORTHAIR, BALD] \
#     hair_colour: [BLONDE, BLACK, BROWN, RED, GRAY], \
#     nose_size: [BIGNOSE, SMALLNOSE], \
#     facial_hair: [BEARD, MOUSTACHE, FULLBEARD], \
#     accessory: [HAT, REDCHEEKS], \
#     mouth_size: [BIGMOUTH, MEDIUMMOUTH, SMALLMOUTH]}  # imported from features constants

def create_candidates(file: str) -> dict[str, dict[str, str]]:
    """Function to load all questions and answers for all candidates into a dictionary
       as determined in the file.
       Precondition:
       - file != ''
    """
    candidate_so_far = {}

    with open(file) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)

        for row in reader:
            d = {}
            for i in range(0, len(row) // 2):
                d[row[2 * i + 1]] = row[2 * i + 2]
            candidate_so_far[row[0]] = d

    return candidate_so_far


def generate_all_possible_questions(file: str) -> list[str]:
    """ A function to generate all questions from the file. """
    all_questions = []

    with open(file) as csv_file:
        row = csv_file.readlines()[0]
        for i in range(1, len(row) // 2):
            all_questions.append(row[2 * i + 1] + '?')

    return all_questions[1:]


class Player:
    """ One of the player in the game
    Instance Attributes:
    - questions : A list representing the questions the player has asked.
    - n : an integer determining if the player is the player 0 or player 1 in the game.
    - spy : The spy this player has chosen.
    Representation Invariants:
        - n == 1 or n == 2
        - spy is a valid person from the given file
    """
    name: str
    questions: list[str]
    candidates: dict[str, dict[str, str]]
    spy: str

    def __init__(self, candidates: dict[str, dict[str, str]], questions: list[str], name:str) -> None:
        """ create a new player for the game. n represets if this is the first/second player and characters represent
        the list of characters that this player can potentially choose to be the spy.
         """
        self.spy = random.choice([name for name in candidates.keys()])
        self.candidates = candidates
        self.questions = questions
        self.name = name

    def make_guesses(self, game: GuessWho) -> str:
        """ The player makes a guess of the opponent's spy based on the current state of the game. An abstract class
            that would be nimplemented differently based on different players we define.

         Preconditions:
             - game._whose_turn() == self.n
        """
        raise NotImplementedError


    def ask_questions(self, game: GuessWho) -> str:
        """ The player asks question about the characterstics of the spy based on the current state of the game.
         Preconditions:
            - game._whose_turn() == self.n
        """
        raise NotImplementedError

    def eliminate_candidates(self, generated_question: str, answer: str):
        """ Eliminating the candidates based on the answers to the question. """
        to_delete = []
        for k, v in self.candidates.items():
            if v[generated_question] != answer:
                to_delete.append(k)

        for key in to_delete:
            del self.candidates[key]


    def eliminate_question(self, generated_question: str):
        """Eliminating the questions that has been asked."""
        self.questions.remove(generated_question)


class GreedyPlayer(Player):
    """ A player who has the higher winning probability in the game.
    Instance Attributes:
        - name: name of the type of player in the game.
        - spy: the spy that the player has chosen.

    """
    def __init__(self, candidates: dict[str, dict[str, str]], questions: list[str]):
        Player. __init__(self, candidates, questions, 'GreedyPlayer')

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
        count_y = 0
        count_n = 0

        for name in self.candidates:
            for question in self.questions:
                if self.candidates[name][question] == 'Y':
                    count_y += 1
                else:
                    count_n += 1
            scores.append(abs(count_y - count_n))

        min_score = min(scores)
        min_index = scores.index(min_score)
        # self.eliminate_candidates(self.questions[min_index], 'Y')
        self.eliminate_question(self.questions[min_index])

        return self.questions[min_index]


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
        # self.eliminate_candidates(question, 'Y')
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

    #specify x-axis and y-axis labels
    ax1.set_xlabel('num_games')
    ax1.set_ylabel('results (0 = lost) (1 = won)')


def run_game(player1: Player, player2: Player, characters_questions_file: str) -> str:
    """Run a GuessWho game between the two given players and returns the winner at the end of the game
    Use the words in word_set_file, and use max_guesses as the maximum number of guesses.
    Return the AdversarialWordle instance after the game is complete.

    Preconditions:
    - word_set_file is a non-empty with one word per line
    """
    players = [player1, player2]
    game = GuessWho(players, characters_questions_file)

    while (len(player1.candidates) != 1) or (len(player2.candidates) != 1):
        question1 = player1.ask_questions(game)
        answer1 = game.return_answer(question1, 2)
        print(f'question1: {question1} answer1: {answer1}')
        player1.eliminate_candidates(question1, answer1)
        question2 = player2.ask_questions(game)
        answer2 = game.return_answer(question2, 1)
        player2.eliminate_candidates(question2, answer2)
        print(f'question2: {question2} answer2: {answer2}')

    assert len(player1.candidates) == 1 or len(player2.candidates) == 1

    guess1 = player1.make_guesses(game)
    guess2 = player2.make_guesses(game)

    return game.get_winner(guess1, guess2)


def run_games(player1: Player, player2: Player, num_games: int, file: str, plot: bool = False, p: bool = False) -> dict:
    """ Run GuessWho num times between player1 and player2, and record the results of each game.

        Optional Parameter:
        - plot: determines if the user wants to plot the game results in graph
        - p: determines if the user wants to print out the winner at the end of each game
        Preconditions:
        - file is a non-empty file with questions and answers related to characteristics of each character
        at each line
    """
    default = [0] * num_games
    results = {'num_games': [i for i in range(1, num_games + 1)], player1.name: default, player2.name: default}
    for i in range(0, num_games):
        winner = run_game(player1, player2, file)
        results[winner][i] = 1
        if p:
            print(f'game {i + 1} winner: {winner}')
    if plot:
        plot_game_statistics(results, player1.name, player2.name)

    return results


