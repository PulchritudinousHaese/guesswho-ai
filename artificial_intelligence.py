"""CSC111 Winter 2023 Project: Guess Who Artificial Intelligence
This module contains the subclassess AI from parent class AI (Player) in guess_who.py and the
necessary functions to backend of the classic game "Guess Who".
This file is Copyright (c) 2023 Annie Wang, Mikhail Skazhenyuk, Xinyuan Gu, Ximei Lin.
"""
from __future__ import annotations
import csv
import random
from typing import Optional
import pandas as pd
import matplotlib.pyplot as plt
from guess_who import Player, GuessWho
import guess_who
import game_tree


########################################################################
# GameTree
########################################################################
def generate_complete_game_tree(root_move: str | game_tree.STARTING_MOVE, game: guess_who.GuessWho,
                                d: int) -> game_tree.GameTree:
    """Generate a complete game tree of depth d for all valid paths the player can take from the current GuessWho Game.

    For the returned GameTree:
        - Its root move is a question.
        - It contains all possible move sequences of length <= d from game_state.
        - If d == 0, a size-one GameTree is returned.

    Note that some paths down the tree may have length < d, because they result in a game state
    with a winner in fewer than d moves. Concretely, if game_state.get_winner() is not None,
    then return just a size-one GameTree containing the root move.

    Preconditions:
        - d >= 0
        - root_move == game_tree.STARTING_MOVE or root_move is a valid move

    """
    tree = game_tree.GameTree(root_move)
    if d == 0 or game.get_winner() is not None:
        if game.get_winner() == game.players[1].name and d % 2 != 0:
            tree.player1_win_probability = 1.0
            return tree
        elif game.get_winner() == game.players[2].name and d % 2 == 0:
            tree.player2_win_probability = 1.0
            return tree
        else:
            tree.player1_win_probability = 0.0
            tree.player2_win_probability = 0.0
            return tree

    elif game.whose_turn() == 1:
        questions_copy1 = game.players[1].questions.copy()
        candidates_copy1 = game.players[1].candidates.copy()
        for question in questions_copy1:
            game.players[1].eliminate_question(question)
            answer = game.return_answer(question, 1)
            game.copy_and_record_player_move(question)
            game.players[1].eliminate_candidates(question, answer)
            new_state = game.copy_and_record_player_move(question)
            sub = generate_complete_game_tree(question, new_state, d - 1)
            tree.add_subtree(sub)
            game.players[1].questions = questions_copy1
            game.players[1].candidates = candidates_copy1
        return tree
    else:
        questions_copy2 = game.players[2].questions.copy()
        candidates_copy2 = game.players[2].candidates.copy()
        for question in questions_copy2:
            game.players[2].eliminate_question(question)
            answer = game.return_answer(question, 1)
            game.copy_and_record_player_move(question)
            game.players[2].eliminate_candidates(question, answer)
            new_state = game.copy_and_record_player_move(question)
            sub = generate_complete_game_tree(question, new_state, d - 1)
            tree.add_subtree(sub)
            game.players[2].questions = questions_copy2
            game.players[2].candidates = candidates_copy2
        tree.update_tree_probabilities()
        return tree


########################################################################
# AI
########################################################################
class CrazyPlayer(Player):
    """ This player uses a decision tree that has been created, and picks the question leading to the path
    with the highest winning probability. The decision tree has depth 10. If self.game_tree is none, CrazyPlayer
    behaves just like GreedyPlayer.
    Instance Attributes:
    - name: name of this type of player in the game.
    - spy: the spy that the player has chosen.
    - gametree: the decision tree that the player follows along if the tree is not none.
    - game: the GuessWho game that this player is in.
    """
    gametree: Optional[game_tree.GameTree]
    game: Optional[GuessWho]

    def __init__(self, candidates: dict[str, dict[str, str]], questions: list[str]) -> None:
        """ Initialize CrazyPlayer with the provided candidates, questions, and game_tree
        """
        Player.__init__(self, candidates, questions, 'CrazyPlayer')
        self.gametree = None
        self.game = None

    def ask_questions(self) -> str:
        """ The player asks question about the characterstics of the spy based on the current state of the game. The
        method mutates questions and candidates by removing the question and candodate that the player
        has already chosen.

        NOTE:
            - CrazyPlayer is always the first plyaer in every game, meaning the first to ask question, and alternate
            with the other player back and forth.

        Precondition:
            - self.game.whose_turn() == 1
        """
        if self.gametree is not None and len(self.game.process) != 0:
            opponent_move = self.game.process[-1]
            sub_tree = self.gametree.find_subtree_by_question(opponent_move)
            self.gametree = sub_tree
        if self.gametree is not None and len(self.gametree.get_subtrees()) != 0:
            max_sub = None
            subtrees = self.gametree.get_subtrees()
            max_so_far = max([tree1.player1_win_probability for tree1 in subtrees])
            for tree in subtrees:
                if tree.player1_win_probability == max_so_far:
                    max_sub = tree
            self.gametree = max_sub
            return self.gametree.question
        else:
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

    def copy(self) -> CrazyPlayer:
        """Return a copy of this player, used in generating gametree for CrazyPlayer"""
        new_player = CrazyPlayer(self.candidates, self.questions)
        return new_player

    def insert_game(self, game: GuessWho) -> None:
        """
        Update the game instance attribute to self.game.
        """
        self.game = game

    def insert_tree(self, tree: Optional[game_tree.GameTree]) -> None:
        """
        Update the tree instance attribute to self.tree.
        """
        self.gametree = tree


class GreedyPlayer(Player):
    """ This player picks the questions that eliminates the closet to half of candidates in the game.
    Instance Attributes:
        - name: name of this type of player in the game.
        - spy: the spy that the player has chosen.
    """

    def __init__(self, candidates: dict[str, dict[str, str]], questions: list[str]) -> None:
        Player.__init__(self, candidates, questions, 'GreedyPlayer')

    def ask_questions(self) -> str:
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

    def copy(self) -> GreedyPlayer:
        """Return a copy of this player, used in generating gametree for CrazyPlayer"""
        new_player = GreedyPlayer(self.candidates, self.questions)
        return new_player


class RandomPlayer(Player):
    """ A player who randomly asks question without using a strategy.
    """

    def __init__(self, candidates: dict[str, dict[str, str]], questions: list[str]) -> None:
        Player.__init__(self, candidates, questions, 'RandomPlayer')

    def ask_questions(self) -> str:
        """ A player randomly asks questions based on the current state of game.
         Preconditions:
            - game._whose_turn() == self.n
        """
        question = random.choice(self.questions)
        self.eliminate_question(question)
        return question

    def copy(self) -> RandomPlayer:
        """Return a copy of this player, used in generating gametree for CrazyPlayer"""
        new_player = RandomPlayer(self.candidates, self.questions)
        return new_player


class PoorPlayer(Player):
    """ A player who deliberately chooses the worst qurestion.
    """

    def __init__(self, candidates: dict[str, dict[str, str]], questions: list[str]) -> None:
        Player.__init__(self, candidates, questions, 'PoorPlayer')

    def ask_questions(self) -> str:
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

    def copy(self) -> PoorPlayer:
        """Return a copy of this player, used in generating gametree for CrazyPlayer"""
        new_player = PoorPlayer(self.candidates, self.questions)
        return new_player


##################################
# run games
##################################
def plot_winner_statistics(result1: dict[str, list[int]], player1: str, player2: str) -> None:
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
    df = pd.DataFrame(result1)
    ax1 = df.plot(kind='scatter', x='num_games', y=player1, color='r', label=player1)
    df.plot(kind='scatter', x='num_games', y=player2, color='g', label=player2, ax=ax1)
    ax1.set_xlabel('number_of_games')
    ax1.set_ylabel('results (0 = lost) (1 = won)')
    plt.show()


def plot_num_games_statistics(result2: dict[str, list[int]]) -> None:
    """ Plot the number of questions that each player asks in each game

        Preconditions:
     - len(results[num_games]) >= 1
     - len(results[num_games]) == len(results[player1]) == len(results[player2])
     - all(isinstance(key,str) for key in results)

    """
    df = pd.DataFrame(result2)
    ax2 = df.plot(kind='scatter', x='num_games', y='num_questions', color='b')
    ax2.set_xlabel('number_of_games')
    ax2.set_ylabel('number_questions_each_game')
    plt.show()


def run_game(players: list[Player], candidates: dict[str, dict[str, str]]) -> dict[str, str | int]:
    """Run a GuessWho game between the two given players and returns the winner at the end of the game.
       Use candidates as the self.candidates of the game. Return a dictionary containing the winner and the number of
       questions each player asks. CrazyPlayer only put in as the first player in list.
       Preconditions:
        - candidates is not an empty dictionary.
        - all({player.spy is not None for player in players})
        - players[0].name == 'CrazyPlayer'
    """
    game = GuessWho(players, candidates)
    player1 = game.players[1]
    player2 = game.players[2]
    if player1.name == 'CrazyPlayer':
        player1.game = game
    single_result = {'winner': None, 'num_questions': 0}
    p1_question = player1.questions
    p2_question = game.players[2].questions
    while len(player1.candidates) != 1 and len(player2.candidates) != 1 and p1_question != [] and p2_question != []:
        question1 = player1.ask_questions()
        answer1 = game.return_answer(question1, 2)
        player1.eliminate_candidates(question1, answer1)
        question2 = player2.ask_questions()
        answer2 = game.return_answer(question2, 1)
        player2.eliminate_candidates(question2, answer2)
        single_result['num_questions'] += 1

    winner = game.get_winner()
    single_result['winner'] = winner

    return single_result


def run_games(num: int, players: list[Player], num_cha: int, file: csv, plot: bool, p: bool = False) -> Optional[str]:
    """ Run GuessWho num times between player1 and player2 with characters in file and num_cha of characters .
        The function returns the results of each game. Parameter plot determines if the user wants to plot the game
        results and number of questions asked in each game.
        Optional Parameter:
        - p: determines if the user wants to print out the winning probability of each player, and the number of
        questions asked by each player in every round.
        Preconditions:
        - file is a non-empty file with questions and answers related to characteristics of each character
        at each line
    """
    default = [0] * num
    default1 = default.copy()
    pl1 = players[0]
    pl2 = players[1]
    results = {'num_games': list(range(1, num + 1)), pl1.name: default, pl2.name: default1}
    num_q = {'num_games': list(range(1, num + 1)), 'num_questions': []}
    game_sta = {players[0].name: 0, players[1].name: 0}
    for i in range(0, num):
        can = guess_who.create_candidates(file, num_cha)
        question = guess_who.generate_all_possible_questions(file)
        pl1.candidates = can
        pl2.candidates = can.copy()
        pl1.questions = question
        pl2.questions = question.copy()
        pl1.select_spy()
        pl2.select_spy()
        result = run_game([pl1, pl2], can.copy())
        if result['winner'] == pl1.name or result['winner'] == pl2.name:
            game_sta[result['winner']] += 1
            results[result['winner']][i] = 1
        num_q['num_questions'].append(result['num_questions'])

    if plot:
        plot_winner_statistics(results, pl1.name, pl2.name)
        plot_num_games_statistics(num_q)

    if p:
        wins_1 = game_sta[pl1.name]
        wins_2 = game_sta[pl2.name]
        return f'[winning_probability:{pl1.name}: {(wins_1 / num) * 100}%, {pl2.name}: {(wins_2 / num) * 100}%]'
    else:
        return None


def run_crazy(num: int, pla: Player, n: int, f: csv, plot: bool, p: bool = False) -> Optional[str]:
    """ Run GuessWho num timesRun GuessWho num times between CrazyPlayer and any given player in pla.
        CrazyPlayer follows a gametree of depth 13.

        The function returns the results of each game. Parameter plot determines if the user wants to plot the game
        results and number of questions asked in each game. CrazyPlayer must be put in as the first player in the list.

        Optional Parameter:
        - p: determines if the user wants to print out the winning probability of each player, and the number of
        questions asked by each player in every round.
        Preconditions:
        - file is a non-empty file with questions and answers related to characteristics of each character
        at each line
        - players[0].name == 'CrazyPlayer'
    """
    default = [0] * num
    default1 = default.copy()
    results = {'num_games': list(range(1, num + 1)), 'CrazyPlayer': default, pla.name: default1}
    num_q = {'num_games': list(range(1, num + 1)), 'num_questions': []}
    game_sta = {'CrazyPlayer': 0, pla.name: 0}
    for i in range(0, num):
        can = guess_who.create_candidates(f, n)
        question = guess_who.generate_all_possible_questions(f)
        pla.candidates = can.copy()
        pla.questions = question.copy()
        pla.select_spy()
        crazy_player = CrazyPlayer(can.copy(), question)
        crazy_player.select_spy()
        tree = generate_tree_each_game(can.copy(), question.copy(), [crazy_player, pla])
        # Generate a decision tree by playing games between two RandomPlayer.
        crazy_player.insert_tree(tree)
        crazy_player.select_spy()
        result = run_game([crazy_player, pla], can.copy())
        if result['winner'] == 'CrazyPlayer' or result['winner'] == pla.name:
            game_sta[result['winner']] += 1
            results[result['winner']][i] = 1
        num_q['num_questions'].append(result['num_questions'])

    if plot:
        plot_winner_statistics(results, 'CrazyPlayer', pla.name)
        plot_num_games_statistics(num_q)

    if p:
        wins_1 = game_sta['CrazyPlayer']
        wins_2 = game_sta[pla.name]
        return f'[winning_probability: CrazyPlayer: {(wins_1 / num) * 100}%, {pla.name}: {(wins_2 / num) * 100}%]'
    else:
        return None


def generate_tree_each_game(candidates: dict, questions: list[str], players: list[Player]) -> game_tree.GameTree:
    """
    Generate game tree based on different GuessWho games.
    Preconditions:
        - players[0].name == 'CrazyPlayer'
    """
    t_player1 = RandomPlayer(candidates.copy(), questions.copy())
    t_player2 = RandomPlayer(candidates.copy(), questions.copy())
    t_player1.spy = players[0].spy
    t_player2.spy = players[1].spy
    t_player2.name = 'RandomPlayer1'
    t_game = guess_who.GuessWho([t_player1, t_player2], candidates.copy())
    tree = generate_complete_game_tree(game_tree.STARTING_MOVE, t_game, 10)
    return tree


# if __name__ == '__main__':
#     # import python_ta
#     # python_ta.check_all(config={
#     #     'extra-imports': ['__future__', 'guess_who', 'matplotlib.pyplot', 'pandas', 'csv', 'random',
#     #                       'matplotlib', 'game_tree', 'typing'],
#     #     'allowed-io': ['open', 'f-strings', 'print'],  # the names (strs) of functions that call print/open/input
#     #     'max-line-length': 120
#     # })
