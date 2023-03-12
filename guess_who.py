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
  - hair_style: The person's hairstyle. 
  - hair_length: The person's hair length.
  - hair_colour: The person's hair colour. None if none.
  - nose_size: The person's nose size.
  - facial_hair: The person's facial_hair. None if none.
  - accessory: The person's accesory. None if none.
  - mouth_size: The person's mouth size.
  - guessed: Boolean whether the person has been guessed or not.
  
  Representation Invariants:
  - 
  
  >>> p = Person(
  
  """

# TODO: Attributes, initializer, determine functions necessary
class GuessWho:
  """The main class to run the game of GuessWho and represent its game_state.
  
  Instance Attributes:
  - guesses: A list representing the moves made by both players in order.
  # - player_one_guesses: A list representing the guesses done by player one.
  # - player_two_guesses: A list representing the guesses done by player two.
  - spies: A list representing the spies of each player (index 0 for player one, index 1 for player two)
  
  Representation Invariants:
  # - (player_one_guesses and guesses) or not (player_one_guesses or guesses)
  # - (player_two_guesses and guesses) or not (player_two_guesses or guesses)
  """
