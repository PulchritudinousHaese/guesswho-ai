This file is Copyright (c) 2023 Annie Wang, Mikhail Skazhenyuk, Xinyuan Gu, Ximei Lin.
"""
import random
from typing import Optional

import a2_game_tree
import a2_adversarial_wordle as aw


class ExploringGuesser(aw.Guesser):
    """A Guesser player that sometimes plays greedily and sometimes plays randomly.

    See assignment handout for details.

    Representation Invariants:
        - 0.0 <= self._exploration_probability <= 1.0
    """
    # Private Instance Attributes:
    #   - _game_tree:
    #       The GameTree that this player uses to make its moves. If None, then this
    #       player just makes random moves.
    #   - _exploration_probability:
    #       The probability that this player ignores its game tree and makes a random move.
    _game_tree: Optional[a2_game_tree.GameTree]
    _exploration_probability: float

    def __init__(self, game_tree: a2_game_tree.GameTree, exploration_probability: float) -> None:
        """Initialize this player."""
        self._game_tree = game_tree
        self._exploration_probability = exploration_probability

    def make_move(self, game: aw.AdversarialWordle) -> str:
        """Make a move given the current game.

        Preconditions:
            - game.is_guesser_turn()
        """
        possible_answers = game.get_possible_answers()
        # Update game tree to corresponding move - None if no subtree
        if len(game.statuses) > 0 and self._game_tree is not None:
            current_status = game.statuses[-1]
            if not self._game_tree.get_subtrees():  # If there are no subtrees
                self._game_tree = None
            else:
                self._game_tree = self._game_tree.find_subtree_by_move(current_status)

        if self._game_tree is not None and self._game_tree.get_subtrees():
            x = random.uniform(0, 1)
            if x < self._exploration_probability:
                move = random.choice(list(possible_answers))
                self._game_tree = self._game_tree.find_subtree_by_move(move)
                return move
            else:
                probability = self.probability_extreme()
                trees_so_far = []

                for subtree in self._game_tree.get_subtrees():

                    if probability == subtree.guesser_win_probability:
                        trees_so_far.append(subtree)

                tree = random.choice(trees_so_far)
                self._game_tree = tree

                return tree.move
        else:
            return random.choice(possible_answers)

    def probability_extreme(self) -> float:
        """Returns the min of probabilities in the current subtrees"""
        probabilities = {x.guesser_win_probability for x in self._game_tree.get_subtrees()}
        return max(probabilities)


def run_learning_algorithm(
        word_set_file: str,
        max_guesses: int,
        exploration_probabilities: list[float],
        show_stats: bool = True) -> a2_game_tree.GameTree:
    """Play a sequence of AdversarialWordle games using an ExploringGuesser and RandomAdversary.

    This algorithm first initializes an empty GameTree. All ExploringGuessers will use this
    SAME GameTree object, which will be mutated over the course of the algorithm!
    Return this object.

    There are len(exploration_probabilities) games played, where at game i (starting at 0):
        - The Guesser is an ExploringGuesser (using the game tree) whose exploration probability
            is equal to exploration_probabilities[i].
        - The Adversary is a RandomAdversary.
        - AFTER the game, the move sequence from the game is inserted into the game tree,
          with a guesser win probability of 1.0 if the Guesser won the game, and 0.0 otherwise.

    Preconditions:
        - word_set_file and max_guesses satisfy the preconditions of aw.run_game
        - all(0.0 <= p <= 1.0 for p in exploration_probabilities)
        - exploration_probabilities != []

    Implementation notes:
        - A NEW ExploringGuesser instance should be created for each loop iteration.
          However, each one should use the SAME GameTree object.
        - You should call aw.run_game, NOT aw.run_games. This is because you need more control
          over what happens after each game runs, which you can get by writing your own loop
          that calls run_game. However, you can base your loop on the implementation of run_games.
        - Note that aw.run_game returns the AdversarialWordle game instance. You may need to review
          the documentation for that class to figure out what methods are useful here.
        - You may call print in this function to report progress made in each game.
        - This function must return the final GameTree object. You can inspect the
          guesser_win_probability of its nodes, calculate its size, or use it in a
          RandomTreeGuesser or GreedyTreeGuesser to see how they do with it.
    """
    results = []
    game_tree = a2_game_tree.GameTree()
    for probability in exploration_probabilities:
        gsr = ExploringGuesser(game_tree, probability)
        adv = aw.RandomAdversary()
        game = aw.run_game(gsr, adv, word_set_file, max_guesses)
        winner = game.get_winner()
        if winner == 'Guesser':
            game_tree.insert_move_sequence(game.get_move_sequence(), 1.0)
        else:
            game_tree.insert_move_sequence(game.get_move_sequence())
        results.append(winner)
    if show_stats:
        aw.plot_game_statistics(results)
    # print(game_tree)
    return game_tree


def linear_function(n: int) -> list[float]:
    """Goes from 0.0 to 1.0 in n steps."""
    return [1.0 - 1 / n * point for point in range(0, n + 1)]


def piece_wise_function(n: int, m: int) -> list[float]:
    """Goes from 1.0 to 0.0 in n steps and then the next m steps are 0.0"""
    return [1.0 - 1 / n * point for point in range(0, n + 1)] + [0.0] * m


def part3_runner() -> a2_game_tree.GameTree:
    """Run example for Part 3.

    Please note that unlike part1_runner and part2_runner, this function is NOT tested.
    We encourage you to experiment with different exploration probability sequences
    to see how quickly you can develop a "winning" GameTree!
    """
    word_set_file = 'data/words/official_wordle_100.txt'
    max_guesses = 4

    probabilities = [0.5] * 4000
    # probabilities = linear_function(4000)
    # probabilities = piece_wise_function(2000, 2000)

    return run_learning_algorithm(word_set_file, max_guesses, probabilities, show_stats=True)


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
    part3_runner()
