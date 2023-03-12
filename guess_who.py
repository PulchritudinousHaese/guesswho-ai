"""CSC111 Winter 2023 Project: Guess Who Artifical Intelligence

This module contains the classes and necessary functions to execute
the backend of the classic game "Guess Who".

Some features:
https://chalkdustmagazine.com/blog/cracking-guess-board-game/

All characters:
https://www.joe.co.uk/life/ranking-guess-who-least-most-horny-193991
"""

import csv
import random
import copy

from typing import Optional, Any

import plotly
import tkinter as tk

########################################################################

def load_person(person_string: str) -> Person:
  """Returns a Person from the defined string of characteristics.
  """
  
  # TODO
  
  return person


def load_persons(file_name: tuple[str | bool]) -> list[Person]:
  """Function to load all features into a list of Person classes 
  as determined in the file file_name.
  
  Precondition:
  - file_name != ''
  """
  persons_so_far = []
  
  with open(games_file) as csv_file:
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
  - 
  
  >>> p = Person(
  
  """

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
    spies: list[Person]

    def __init__(self, spy1: Person, spy2: Person) -> None:
        """ Initialize a GuessWho game with the two players"""
        self.guesses = []
        self.spies = [spy1, spy2]


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

    def __init__(self, n, spy) -> None:
        """ create a new player for the game. n represets if this is the first/second player and spy
        represents the chraracter this player has chosen.
         """
        self.question = []
        self.n = n
        self.spy = spy
