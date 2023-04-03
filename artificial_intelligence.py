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
from python_ta.contracts import check_contracts
import game_tree

from typing import Optional


########################################################################
# GameTree
#############
    
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
        # print(f'winner{game.get_winner()}')
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

      
class CrazyPlayer(Player):
    """ This player uses a decision tree that has been created, and picks the question leading to the path
    with the highest winning probability. The decision tree has depth 7. If self.game_tree is none, CrazyPlayer
    behaves just like GreedyPlayer.
    Instance Attributes:
    - name: name of this type of player in the game.
    - spy: the spy that the player has chosen.
    - gametree: the decision tree that the player follows along if the tree is not none.
    - game: the GuessWho game that this player is in.
    """
    game_tree: Optional[game_tree.GameTree]
    game: Optional[GuessWho]

    def __init__(self, candidates: dict[str, dict[str, str]], questions: list[str]):
        """ Initialize CrazyPlayer with the provided candidates, questions, and game_tree
        """
        Player.__init__(self, candidates, questions, 'CrazyPlayer')
        self.game_tree = None
        self.game = None

    def insert_game(self, game):
        """
        Update the game instance attribute to self.game
        """
        self.game = game

    def insert_tree(self, tree: game_tree):
        """
        Update the tree instance attribute to self.tree
        """
        self.gametree = tree

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
        if self.game_tree is not None and len(self.game.process) != 0:
            opponent_move = self.game.process[-1]
            sub_tree = self.game_tree.find_subtree_by_move(opponent_move)
            self.game_tree = sub_tree
        if self.game_tree is not None and len(self.game_tree.get_subtrees()) != 0:
            max_sub = None
            subtrees = self.game_tree.get_subtrees()
            max_so_far = max([tree1.player1_win_probability for tree1 in subtrees])
            for tree in subtrees:
                if tree.player1_win_probability == max_so_far:
                    max_sub = tree
            self.game_tree = max_sub
            return self.game_tree.question
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

    def _copy(self) -> CrazyPlayer:
        """Return a copy of this player, used in generating gametree for CrazyPlayer"""
        new_player = CrazyPlayer(self.candidates, self.questions, self.game_tree, self.game)
        return new_player
      

class ExploringPlayer(Player):
    """A player that sometimes plays greedily and sometimes plays randomly."""
    _game_tree: Optional[game_tree.GameTree]
    _exploration_probability: float
    game: guess_who.GuessWho

    def __init__(self, game_tree: game_tree.GameTree, exploration_probabilty: float) -> None:
        """Initialize the Player."""
        Player.__init__(self, candidates, questions, 'ExploringPlayer')
        self._game_tree = game_tree
        self._exploration_probability = exploration_probabilty

    def insert_game(self, game: guess_who.GuessWho) -> None:
        self.game = game

    def ask_questions(self) -> str:
        """ Make a guess given the current game. """
        possible_questions = self.questions
        game = self.game
        if len(game.process) > 0 and self._game_tree is not None:
            question = game.process[-1]
            if not self._game_tree.get_subtrees():
                self._game_tree = None
            else:
                self._game_tree = self._game_tree.find_subtree_by_question(question)

        if self._game_tree is None or len(self._game_tree.get_subtrees()) == 0:
            return random.choice(possible_questions)
        else:
            x = random.random()
            if x < self._exploration_probability:
                question = random.choice(possible_questions)
                self._game_tree = self._game_tree.find_subtree_by_question(question)
                return question

            else:
                subtree = self._game_tree.get_subtrees()
                question = max(subtree, key=lambda s_tree: s_tree.win_probability).question
                self._game_tree = self._game_tree.find_subtree_by_question(question)
                return question


def run_learning_algorithm(file: str, max_guesses: int, probabilities: list[float],
                           show_stats: bool = True) -> game_tree.GameTree:
    """ Play a sequence of GuessWho games using an ExploringPlayer and RandomPlayer.
    Preconditions:
        - file and max_guesses satisfy the preconditions of run_game
        - all(0.0 <= p <= 1.0 for p in exploration_probabilities)
        - probabilities != []
    """

    results = {}
    results['num_game'] = []
    results['ExploringPlayer'] = []
    results['RandomPlayer'] = []
    n = 0
    tree = game_tree.GameTree()
    can = guess_who.create_candidates(file, max_guesses)
    quest = guess_who.generate_all_possible_questions(file)

    for probability in probabilities:
        p1 = ExploringPlayer(tree, probability)
        p2 = RandomPlayer(can, quest)
        game = run_game([p1, p2], candidates)

        if game == 'ExploringPlyaer':
            results['ExploringPlayer'].append(1)
            results['RandomPlayer'].append(0)
            tree.insert_question_sequence(game.process, 1.0)
        else:
            results['ExploringPlayer'].append(0)
            results['RandomPlayer'].append(1)
            tree.insert_question_sequence(game.process)
        n += 1
        results['num_game'].append(n)

    if show_stats:
        plot_winner_statistics(results, 'ExploringPlayer', 'RandomPlayer')

    return tree


########################################################################
class GreedyPlayer(Player):
    """ A player who has the higher winning probability in the game.
    Instance Attributes:
        - name: name of the type of player in the game.
        - spy: the spy that the player has chosen.
    """

    def __init__(self, candidates: dict[str, dict[str, str]], questions: list[str]):
        Player.__init__(self, candidates, questions, 'GreedyPlayer')

    def make_guesses(self) -> str:
        """ The player makes a guess of the name of the opponent's spy at the end of the game."""

        for name in self.candidates:
            return name

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
        print(f'greedy player q: {question}')
        print(f'greedy player left q: {self.questions}')
        return question



class RandomPlayer(Player):
    """ A player who randomly asks question without using a strategy.
    """

    def __init__(self, candidates: dict[str, dict[str, str]], questions: list[str]):
        Player.__init__(self, candidates, questions, 'RandomPlayer')

    def make_guesses(self) -> str:
        """ The player makes a guess of the name of the opponent's spy at the last round of the game.
        Precondition:
            - len(self.candidates) == 1
        """
        for name in self.candidates:
            return name

    def ask_questions(self) -> str:
        """ A player randomly asks questions based on the current state of game.
         Preconditions:
            - game._whose_turn() == self.n
        """
        question = random.choice(self.questions)
        self.eliminate_question(question)
        print(f'random player q: {question}')
        print(f'random player left q: {self.questions}')
        return question


class PoorPlayer(Player):
    """ A player who deliberately chooses the worst qurestion.
    """

    def __init__(self, candidates: dict[str, dict[str, str]], questions: list[str]):
        Player.__init__(self, candidates, questions, 'PoorPlayer')

    def make_guesses(self) -> str:
        """ The player makes a guess of the name of the opponent's spy at the last round of the game.
        Precondition:
            - len(self.candidates) == 1
        """
        for name in self.candidates:
            return name

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
        print(f'poor player q: {question}')
        print(f'poor player left q: {self.questions}')
        return question


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


@check_contracts
def run_game(players: list[Player], candidates: dict[str, dict[str, str]]) -> dict[str, str | int]:
    """Run a GuessWho game between the two given players and returns the winner at the end of the game.
       Use candidates as the self.candidates of the game. Return a dictionary containing the winner and the number of
       questions each player asks.
       Preconditions:
        - candidates is not an empty dictionary.
        - all({player.spy is not None for player in players})
    """
    game = GuessWho(players, candidates)
    player1 = game.players[1]
    player2 = game.players[2]
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

    guess1 = player1.make_guesses()
    guess2 = player2.make_guesses()
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
    results = {'num_games': [n for n in range(1, num + 1)], pl1.name: default, pl2.name: default1}
    num_q = {'num_games': [n for n in range(1, num + 1)], 'num_questions': []}
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
   
  
  def run_crazy(num: int, pla: Player, n: int, f: csv, plot: bool, p: bool = False) -> Optional[str]:
    """ Run GuessWho num timesRun GuessWho num times between CrazyPlayer and any given player in pla.
        CrazyPlayer follows a gametree of depth d.

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
    results = {'num_games': [n for n in range(1, num + 1)], 'CrazyPlayer': default, pla.name: default1}
    num_q = {'num_games': [n for n in range(1, num + 1)], 'num_questions': []}
    game_sta = {'CrazyPlayer': 0, pla.name: 0}
    for i in range(0, num):
        print(f'name: {i}')
        can = guess_who.create_candidates(f, n)
        question = guess_who.generate_all_possible_questions(f)
        pla.candidates = can.copy()
        pla.questions = question.copy()
        pla.select_spy()
        crazy_player = CrazyPlayer(can.copy(), question)
        crazy_player.select_spy()
        t_player1 = RandomPlayer(can.copy(), question.copy())
        t_player2 = RandomPlayer(can.copy(), question.copy())
        t_player1.spy = crazy_player.spy
        t_player2.spy = pla.spy
        t_player2.name = 'RandomPlayer1'
        t_game = guess_who.GuessWho([t_player1, t_player2], can.copy())
        tree = generate_complete_game_tree(game_tree.STARTING_MOVE, t_game, 6)
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
    candidates = guess_who.create_candidates('data/questions.csv', 16)
    candidates1 = candidates.copy()
    candidates2 = candidates.copy()
    questions = guess_who.generate_all_possible_questions('data/questions.csv')
    player1 = GreedyPlayer(candidates, questions)
    player2 = PoorPlayer(candidates1, questions.copy())
    player1.select_spy()
    player2.select_spy()
    game = guess_who.GuessWho([player1, player2], candidates2)
    # # print(run_game([player1, player2], candidates2))
    #
    # print(run_games(100, [player1, player2], 12, 'data/questions.csv', True, True))

    print(generate_complete_game_tree(game_tree.STARTING_MOVE, game, 7))
