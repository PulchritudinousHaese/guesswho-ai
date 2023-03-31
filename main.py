"""CSC111 Winter 2023 Project: Guess Who Artifical Intelligence
This module is responsible for combining the backend and frontend of the
Guess Who application.
"""
import guess_who
from guess_who import Player, RandomPlayer, GreedyPlayer, PoorPlayer
import csv


###########################################################
# main function to run games and test performances between the GuessWho AIs that we've defined.
###########################################################
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
        can = guess_who.create_candidates(file, num_cha)
        question = guess_who.generate_all_possible_questions(file)
        player1.candidates = can
        player2.candidates = can.copy()
        player1.questions = question
        player2.questions = question.copy()
        player1.select_spy()
        player2.select_spy()
        winner = guess_who.run_game([player1, player2], can.copy())
        if winner == player1.name or winner == player2.name:
            game_sta[winner] += 1
            results[winner][i] = 1
    if p:
        pl1_wins = game_sta[pl1_name]
        pl2_wins = game_sta[pl2_name]
        print(f'[winning_probability:{pl1_name}: {(pl1_wins/num) * 100}%, {pl2_name}: {(pl2_wins/num) * 100}%]')
    if plot:
        guess_who.plot_game_statistics(results, player1.name, player2.name)

    return results


if __name__ == '__main__':

    candidates = guess_who.create_candidates('data/questions.csv', 12)       # Define data to initialize two players
    candidates1 = candidates.copy()
    questions = guess_who.generate_all_possible_questions('data/questions.csv')

    # Sample call to run GuessWho 100 times between GreedyPlayer and PoorPlayer.
    # You may change the first parameter in run_games to determine how many games you would like to run.
    # You may change the last two parameters False, to not print out the winning probability of
    # each player(last parameter), or to not plot the game results(second last parameter).
    player1 = GreedyPlayer(candidates, questions)
    player2 = PoorPlayer(candidates1, questions)
    run_games(100, [player1, player2], 12, 'data/questions.csv', True, True)
    # You can see GreedyPlayer has obviously better performance.

    # Below is a Sample call to run GuessWho 100 times with same setting, but between GreedyPlayer
    # and RandomPlayer.
    # player1 = GreedyPlayer(candidates, questions)
    # player2 = RandomPlayer(candidates1, questions)
    # run_games(100, [player1, player2], 12, 'data/questions.csv', True, True)

    # You should notive a more nuanced difference between performance of these two players compared to
    # that between PoorPlayer and GreedyPlayer. Sometimes GreedyPlayer and RandoPlayer may even have the same 
    # winning probability!

