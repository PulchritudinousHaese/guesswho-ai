"""CSC111 Winter 2023 Project: Guess Who Artifical Intelligence
This module contains the GameTree class and all necessary methods to
add respective player moves and change probabilities.
This file is Copyright (c) 2023 Annie Wang, Mikhail Skazhenyuk, Xinyuan Gu, Ximei Lin.
"""
from __future__ import annotations

from typing import Optional

STARTING_MOVE = '*'


class GameTree:
    """A tree to compile different move sequences of the game Guess Who.

    THIS DOES NOT STORE ALTERNATING MOVES, RATHER IT STORES INDIVIDUAL PLAYER MOVE SEQUENCES.

    Each node in the tree stores a Guess Who question/guess.

    Instance Attributes:
        - move: '*' if it is the start of the game, or a question/guess
        - win_probability: the probability the player will win if they follow this path.

    Representation Invariants:
        - self.move == STARTING_MOVE or self.move is a valid Guess Who question/guess
        - all(key == self._subtrees[key].move for key in self._subtrees)
        - STARTING_MOVE not in self._subtrees  # since it can only appear at the very top of a game tree
    """
    move: str
    win_probability: Optional[float] = 0.0

    # Private Instance Attributes:
    #  - _subtrees:
    #      Following step along the path (question/guess)
    _subtrees: dict[str, GameTree]

    def __init__(self, move: str = STARTING_MOVE,
                 win_probability: Optional[float] = 0.0) -> None:
        """Initialize a new game tree.

        >>> game = GameTree()
        >>> game.move == STARTING_MOVE
        True
        """
        self.move = move
        self._subtrees = {}
        self.win_probability = win_probability

    def get_subtrees(self) -> list[GameTree]:
        """Return the game trees (out of the _subtrees dict)."""
        return list(self._subtrees.values())

    def find_subtree_by_move(self, move: str) -> Optional[GameTree]:
        """Returns the GameTree corresponding the question (move) made.
        Returns None if no such subtree exists.
        """
        if move in self._subtrees:
            return self._subtrees[move]
        else:
            return None

    def __str__(self) -> str:
        """Return a string version of this tree.
        """
        return self._printable(0)

    def _printable(self, depth: int) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.

        You MAY change the implementation of this method (e.g. to display different instance attributes)
        as you work on this assignment.

        Preconditions:
            - depth >= 0
        """
        move_desc = f'{self.move}\n'
        str_so_far = '  ' * depth + move_desc
        for subtree in self._subtrees.values():
            str_so_far += subtree._printable(depth + 1)
        return str_so_far

    def add_subtree(self, subtree: GameTree) -> None:
        """Add a subtree to this game tree.
        Update probability following this addition.
        """
        self._subtrees[subtree.move] = subtree
        self._update_win_probability()

    def insert_move_sequence(self, moves: list[str], probability: Optional[float] = 0.0) -> None:
        """Insert the given sequence of moves (questions/guesses) into this tree.
        """
        moves_copy = moves.copy()
        if self.sequence_in_tree(moves) or not moves:
            return
        elif moves[0] in self._subtrees:
            move = moves_copy.pop(0)
            tree = self.find_subtree_by_move(move)
            tree.insert_move_sequence(moves_copy, probability)
        else:
            self.next_moves(moves_copy, probability)

        self._update_win_probability()

    def sequence_in_tree(self, moves: list[str | tuple[str, ...]]) -> bool:
        """Return wheter the move sequence is already in the tree."""
        moves_copy = moves.copy()
        if not moves:
            return True
        elif moves[0] not in self._subtrees:
            return False
        else:
            move = moves_copy.pop(0)
            subtree = self.find_subtree_by_move(move)
            return subtree.sequence_in_tree(moves_copy)

    def next_moves(self, moves: list[str | tuple[str, ...]], probability: Optional[float] = 0.0) -> None:
        """Helper Function.
        Recursively adds next moves to the GameTree assuming this version of events never occured before.
        """
        if len(moves) == 1:  # Last move in sequence
            new_leaf = GameTree(moves[0])
            new_leaf.win_probability = probability
            self.add_subtree(new_leaf)
        else:
            moves_copy = moves.copy()
            move = moves_copy.pop(0)
            game_tree = GameTree(move)
            game_tree.next_moves(moves_copy, probability)
            self.add_subtree(game_tree)
        self._update_win_probability()

    def _update_win_probability(self) -> None:
        """Recalculate the guesser win probability of this tree.

        Probability is updated based on these metrics:
        -
        """
        if not self.get_subtrees():
            return
        elif self.get_subtrees():
            probability_sum = sum(tree.win_probability for tree in self.get_subtrees())
            self.win_probability = probability_sum / len(self.get_subtrees())

    def update_tree_probabilities(self) -> None:
        """Updates the entire tree's probabilities recursively."""
        if self._subtrees:
            for subtree in self.get_subtrees():
                subtree.update_tree_probabilities()
            self._update_win_probability()


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
