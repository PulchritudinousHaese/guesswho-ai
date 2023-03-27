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

from typing import Optional, Any

import plotly
import tkinter as tk
from game_tree import GameTree

from features import *


########################################################################

def load_person(person_tuple: tuple[str]) -> Person:
    """Returns a Person from the defined string of characteristics.

    Preconditions:
    - len(person_tuple) == 9
    """
    p = person_tuple
    person = Person(p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8])
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

        for row in reader:
            row = tuple(row)
            person = load_person(row)
            persons_so_far.append(person)

    return persons_so_far


########################################################################

# TODO: Finish attributes, initializer, determine functions necessary
class Person:
  """The main class to represent each person in the game of GuessWho.

  Instance Attributes:
  - name: The person's name (for the final guess)
  - ear_size: The size of the person's ears.
  - hair_style: The person's hairstyle. None if none.
  - hair_length: The person's hair length.
  - hair_colour: The person's hair colour. None if none.
  - nose_size: The person's nose size.
  - facial_hair: The person's facial_hair. None if none.
  - accessory: The person's accesory. None if none.
  - mouth_size: The person's mouth size.
  - up: Boolean whether the person has been guessed/eliminated or not.

  Representation Invariants:
  - self.name != ''
  - self.ear_size != ''
  - self.hair_style != '' or self.hair_style is None
  - self.hair_length != '' or self.hair_length is None
  - self.hair_colour != '' or self.hair_colour is None
  - self.nose_size != ''
  - self.facial_hair != '' or self.facial_hair is None
  - self.accessory != '' or self.accessory is None
  - self.mouth_size != ''
  - self.up is True or self.up is False

  >>> p = Person(
  """
  name: str
  ear_size: str
  hair_style: Optional[str]
  hair_length: Optional[str]
  hair_colour: Optional[str]
  nose_size: str
  facial_hair: Optional[str]
  accessory: Optional[str]
  mouth_size: str
  up: bool

  def __init__(self, name:str, ear_size: str, hair_style: Optional[str],
             hair_length: Optional[str], hair_colour: Optional[str],
             nose_size: str, facial_hair: Optional[str], accessory: Optional[str],
             mouth_size: str, up: bool = True) -> None:
    """Initialize Person with given Instance Attributes. """

    self.name = name
    self.ear_size = ear_size
    self.hair_style = hair_style
    self.hair_length = hair_length
    self.hair_colour = hair_colour
    self.nose_size = nose_size
    self.facial_hair = facial_hair
    self.accessory = accessory
    self.mouth_size = mouth_size
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
    guesses: list[str]
    players: dict[int, Player]
    characters = list[Person]

    def __init__(self, player1, player2, characters: list[Person]) -> None:
        """ Initialize a GuessWho game with the two players"""
        self.guesses = []
        self.players[1] = player1
        self.players[2] = player2
        self.characters = characters

    def _record_answers(self, guess: str) -> None:
        """ Record the guesses that have been made by each player in the game, and update the game's status"""
        self.guesses.append(guess)

    def get_winner(self, guess1, guess2) -> Optional[str]:
        """ return if there is a winner in the game and which player is the winner, with the guess1 by player1
        and guess2 by player2"""
        if guess1 == self.players[1].spy:
            return 'player1'
        elif guess2 == self.players[2].spy:
            return 'player2'

    def _whose_turn(self) -> int:
        """ return it's which player's turn to make a guess in this round of game"""
        if len(self.guesses) % 2 == 0:
            return 2
        else:
            return 1


list_of_categories = [HAIR_COLOUR, HAIR_STYLES, ...]  # imported from features constants

def get_list_of_category (characteristic): 
    for lst in list_of_categories:
        if characteristic in lst:
            return lst
            
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

    questions: list[str]
    n: int
    spy: Person
    possible_guesses: list[Person]
    visited: set[Person] = set()
    _game_tree: GameTree

    def __init__(self, n, spy) -> None:
        """ create a new player for the game. n represets if this is the first/second player and spy
        represents the chraracter this player has chosen.
         """
        self.question = []
        self.n = n
        self.spy = spy

    def _make_guesses(self, game: GuessWho) -> str:
        """ The player makes a guess of the opponent's spy based on the current state of the game. An abstract class that would be
        implemented differently based on different players we define.
        
         Preconditions: 
         - game._whose_turn() == self.n        
        """
        raise NotImplementedError
    
    def _choose_spy(self, characters: list[Person]) -> None:
        """ The player chooses the spy from the given set of characters at the start of the GuessWho game."""
        self.spy = random.choice(characters)
    
    def check_question_to_persons -> None: #check for each person
        for person in self.possible_guesses:

            if check_question_to_person:
                person.up = False
    
    def check_question_to_person -> bool: #checks 
        a1 = question.a1
        if question.connective:
            connective = question.connective
            a2 = question.a2

            if connective == 'OR':
                if a1[0] == '0':
                    a1 = a1[1]
                    match(a1):
                        case person.hair_colour == a1:
                else:
                    a1 = a1[1]
                    match(a1):
                        case a1 in HAIR_COLOUR and person.hair_colour != a1:

        
def run_game(player1: Player, player2: Player, characters_files: str) -> GuessWho:
    """Run a GuessWho game between the two given players.

    Use the words in word_set_file, and use max_guesses as the maximum number of guesses.

    Return the AdversarialWordle instance after the game is complete.

    Preconditions:
    - word_set_file is a non-empty with one word per line
    - all words in word_set_file have the same length
    - max_guesses >= 1
    """
    # with open(word_set_file) as f:
    #     word_set = {str.strip(line.lower()) for line in f}
    # 
    # game = AdversarialWordle(word_set, max_guesses)
    # 
    # while game.get_winner() is None:
    #     guess = guesser.make_move(game)
    #     game.record_guesser_move(guess)
    #     status = adversary.make_move(game)
    #     game.record_adversary_move(status)
    # 
    # return game
