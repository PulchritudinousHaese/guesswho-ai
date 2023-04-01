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
import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import dataclass

from typing import Optional
from features import *

import tkinter as tk


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
    candidates: dict[str, dict[str, str]]

    def __init__(self, players: list[Player], candidates: dict[str, dict[str, str]]) -> None:
        """ Initialize a GuessWho game with the two players"""
        self.candidates = candidates
        self.players = {1: players[0], 2: players[1]}

    def get_winner(self, guess1, guess2) -> Optional[str]:
        """ return if there is a winner in the game and which player is the winner, with the guess1 by player1
        and guess2 by player2. Guess1 is the guess made by player1 and guess2 is the guess by player2.
        One of the player wins if :
            - The player successfully guesses the spy of the opponent.
            - The opponent has run out of the questions first。
        There is a tie under two circumstances:
            - Both guessers have guessed the spy of the opponent.
            - Both players have run out of questions to ask.
        """
        if not self.players[1].questions and not self.players[2].questions
            return 'tie'
        elif not self.players[1].questions:
            return self.players[2].name
        elif not self.players[2].questions:
            return self.players[1].name
        elif (guess1 == self.players[1].spy) and (guess2 == self.players[2].spy):
            return 'tie'
        elif guess2 == self.players[1].spy:
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
        verify_with = self.players[player_num]
        return self.candidates[verify_with.spy][question]


def create_candidates(file: str, num_cha: int) -> dict[str, dict[str, str]]:
    """Function to load all questions and answers for all candidates into a dictionary
       as determined in the file. Create the candidates dictionary with num_cha characters.

       Precondition:
       - file != ''
    """
    candidate_so_far = {}
    limited_candidates = {}
    b = 0

    with open(file) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)

        for row in reader:
            d = {}
            for i in range(0, (len(row) - 1) // 2):
                d[row[2 * i + 1]] = row[2 * i + 2]
            candidate_so_far[row[0]] = d

        while b != num_cha:
            added_pair = random.choice(list(candidate_so_far.items()))
            if added_pair[0] not in limited_candidates:
                limited_candidates[added_pair[0]] = added_pair[1]
                b += 1
        return limited_candidates


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
    - the name of the player.
    - questions : A list representing the questions the player has asked.
    - n : an integer determining if the player is the player 0 or player 1 in the game.
    - spy : The spy this player has chosen.
    Representation Invariants:
        - spy is a valid person from the given file
    """
    name: str
    questions: list[str]
    candidates: dict[str, dict[str, str]]
    spy: str

    def __init__(self, candidates: dict[str, dict[str, str]], questions: list[str], name: str) -> None:
        """ create a new player for the game. n represets if this is the first/second player and characters represent
        the list of characters that this player can potentially choose to be the spy.
         """
        self.candidates = candidates
        self.questions = questions
        self.name = name

    def select_spy(self):
        """ The player selects the docstring"""
        self.spy = random.choice([name for name in self.candidates.keys()])

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
        # print(f'{self.name} candidates {len(self.candidates)}')
        # print(f'to delete{to_delete}')
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
        can = create_candidates(file, num_cha)
        question = generate_all_possible_questions(file)
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
    candidates = create_candidates('data/questions.csv', 12)
    candidates1 = candidates.copy()
    candidates2 = candidates.copy()
    questions = generate_all_possible_questions('data/questions.csv')
    player1 = GreedyPlayer(candidates, questions)
    player2 = RandomPlayer(candidates1, questions)
    run_games(100, [player1, player2], 12, 'data/questions.csv', True, True)
