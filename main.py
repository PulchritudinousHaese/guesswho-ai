"""CSC111 Winter 2023 Project: Guess Who Artifical Intelligence
This module contains the classes and necessary functions to execute
the frontend with the backend of the classic game "Guess Who".

The files interface.py and guess_who.py are combined in this file to work together.
artifical_intelligence is provided to play against as an opponent and the player
may choose which opponent to play against.

This file also contins the main function to run games and test performaces between AIs.
"""
import guess_who
from guess_who import Player, RandomPlayer, GreedyPlayer, PoorPlayer
import csv

from __future__ import annotations

from tkinter import *

import interface as IF
import guess_who as GW
import artificial_intelligence as AI

game_settings = {'question': ''}


###########################################################
# main function to run games and test performances between the GuessWho AIs that we've defined.
###########################################################
def run_games(num: int, players: list[Player], num_cha: int, file: csv, plot: bool = False, p: bool = False) -> dict:
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
        print(f'[winning_probability:{pl1_name}: {(pl1_wins / num) * 100}%, {pl2_name}: {(pl2_wins / num) * 100}%]')
    if plot:
        guess_who.plot_game_statistics(results, player1.name, player2.name)

    return results


class HumanPlayer(GW.Player):
    """The class representing the human player."""

    def __init__(self, candidates: dict[str, dict[str, str]], questions: list[str]):
        GW.Player.__init__(self, candidates, questions, 'HumanPlayer')

    def make_guesses(self, game: GW.GuessWho) -> str:
        """Make a guess at the enemy's spy."""
        return IF.guess_frame_objects['label']['text']

    def ask_questions(self, game: GW.GuessWho) -> str:
        """Asks a question based on which question the player selected."""
        return game_settings['question'] + '?'


def make_a_guess() -> None:
    """Makes the current guess for the HumanPlayer"""
    IF.clear_chat()
    p1 = game_settings['players'][0]
    q1 = p1.make_guesses(game_settings['game'])
    # print(game_settings['players'][1].spy, q1)
    if game_settings['players'][1].spy == q1:
        g2 = game_settings['players'][1].make_guesses(game_settings['game'])
        IF.insert_conversation('You are correct!\n\nComputer made \nthe final guess:\n' + g2 + '\n')
        if g2 == game_settings['players'][0].spy:
            IF.insert_conversation('The Computer \nguessed correctly!\nIt is a tie\n')
        else:
            IF.insert_conversation('The Computer \nguessed incorrectly!\nYou win!\n')
    disable_all()


def make_a_final_guess() -> None:
    """Makes the current final guess for the HumanPlayer"""
    p1 = game_settings['players'][0]
    q1 = p1.make_guesses(game_settings['game'])
    # print(game_settings['players'][1].spy, q1)
    if game_settings['players'][1].spy == q1:
        IF.insert_conversation('You are correct!\nIt is a tie!')
    else:
        IF.insert_conversation('You lost!\n')
    disable_all()
    IF.insert_conversation('''Let's play again!\nClick menu\nto reset''')
    disable_all()


def make_a_question() -> None:
    """Makes a question for the HumanPlayer"""
    IF.clear_chat()
    p1 = game_settings['players'][0]
    q1 = p1.ask_questions(game_settings['game'])
    IF.insert_conversation('You asked if the \ncomputer has:\n'
                           + IF.convert_feature_to_text(game_settings['question'])
                           + '\n')
    a1 = game_settings['game'].return_answer(q1, 2)  # Y or N
    if a1 == 'Y':
        IF.insert_conversation('Yes!\nMy spy has the\nfeature:\n'
                               + IF.convert_feature_to_text(game_settings['question']) + '\n')
        for face in IF.game_features['faces']:
            if game_settings['question'] not in face.chars:
                face.up = False
                face.cover()
    else:
        IF.insert_conversation('No!\nMy spy does not have\nthe feature:\n'
                               + IF.convert_feature_to_text(game_settings['question']) + '\n')
        for face in IF.game_features['faces']:
            if game_settings['question'] in face.chars:
                face.up = False
                face.cover()
    p1.eliminate_candidates(q1, a1)
    computer_make_a_question()


def disable_all() -> None:
    """Disables all buttons on the main board."""
    for b in IF.question_frame_objects['buttons']:
        b.config(state=DISABLED)
    IF.question_frame_objects['questionbutton'].config(state=DISABLED)
    IF.question_frame_objects['clearbutton'].config(state=DISABLED)

    IF.guess_frame_objects['guessbutton'].config(state=DISABLED)
    IF.guess_frame_objects['clearbutton'].config(state=DISABLED)


def enable_all() -> None:
    """Disables all buttons on the main board."""
    for b in IF.question_frame_objects['buttons']:
        b.config(state=NORMAL)
    IF.question_frame_objects['questionbutton'].config(state=DISABLED)
    IF.question_frame_objects['clearbutton'].config(state=NORMAL)

    IF.guess_frame_objects['guessbutton'].config(state=DISABLED)
    IF.guess_frame_objects['clearbutton'].config(state=NORMAL)


def fake_think() -> None:
    """Fakes thinking like a computer"""
    game_settings['window'].after(6000, fake_think)


def computer_make_a_guess() -> None:
    """Makes the computer make its guess and gives the player an option to make their guess."""
    g2 = game_settings['players'][1].make_guesses(game_settings['game'])
    IF.insert_conversation('You are correct!\nComputer made \nthe final guess:\n' + g2 + '\n')
    IF.insert_conversation('The Computer \nguessed correctly!\nIt is your turn\nto tie it up!')
    disable_all()
    IF.guess_frame_objects['clearbutton'].config(state=NORMAL)
    IF.guess_frame_objects['guessbutton'].config(command=make_a_final_guess)
    IF.clear_selection()


def computer_make_a_question() -> None:
    """Makes the computer make its question move"""
    disable_all()
    # IF.conversation_frame_objects['bar'].start()
    p2 = game_settings['players'][1]
    if len(p2.candidates) == 1:
        computer_make_a_guess()
    else:
        q2 = p2.ask_questions(game_settings['game'])
        a2 = game_settings['game'].return_answer(q2, 1)
        p2.eliminate_candidates(q2, a2)
        fake_think()
        IF.insert_conversation('The computer has \nasked if you have:\n' + IF.convert_feature_to_text(q2[0]) + '\n')
        fake_think()
        if a2 == 'Y':
            IF.insert_conversation('Your spy has this\nattribute!\n')
        else:
            IF.insert_conversation('Your spy does not have this attribute!\n')
        enable_all()
        # IF.conversation_frame_objects['bar'].stop()
        IF.clear_selection()


def select_question(button: Button) -> None:
    """Selects a question and stores it"""
    global game_settings
    game_settings['question'] = IF.question_to_feature(button['text'])
    for b in IF.question_frame_objects['buttons']:
        if b['text'] == button['text']:
            b.config(state=DISABLED)
        else:
            b.config(state=NORMAL)
    IF.question_frame_objects['label'].config(text=button['text'])
    IF.question_frame_objects['questionbutton'].config(state=NORMAL)


def determine_if_enabled(button: Button) -> None:
    """Determines whether or no the question button should be enabled."""
    # print(game_settings['players'][0].questions)
    question = IF.question_to_feature(button['text']) + '?'
    # print(question, question in game_settings['players'][0].questions)
    if question in game_settings['players'][0].questions and button['text'] != game_settings['question']:
        button.config(state=NORMAL)
    else:
        button.config(state=DISABLED)


def text_to_player(text: str) -> GW.Player:
    """Converts the text to the respective player and initializes the object, then returns it."""
    if text == 'GreedyPlayer':
        return AI.GreedyPlayer(game_settings['candidates'].copy(), game_settings['questions'].copy())
    if text == 'RandomPlayer':
        return AI.RandomPlayer(game_settings['candidates'].copy(), game_settings['questions'].copy())
    if text == 'PoorPlayer':
        return AI.PoorPlayer(game_settings['candidates'].copy(), game_settings['questions'].copy())


def update_question_buttons() -> None:
    """Updates all the question buttons in the button frame."""
    IF.game_features['menu'].config(command=new_game)
    for button in IF.question_frame_objects['buttons']:
        q = IF.question_to_feature(button['text']) + '?'
        if q in game_settings['players'][0].questions:
            button.config(state=NORMAL, command=lambda b=button: select_question(b))
    IF.guess_frame_objects['guessbutton'].config(command=make_a_guess)
    IF.question_frame_objects['questionbutton'].config(command=make_a_question)


def select_player(difficulty: str) -> None:
    """Selects the player that will play (AI)"""
    global game_settings

    # print(player1.spy)
    player2 = text_to_player(difficulty)
    player2.select_spy()
    print(player2.spy)
    game_settings['players'].append(player2)
    IF.clear_frame()
    IF.summon_main_board()
    spy = IF.name_to_face(game_settings['players'][0].spy)
    spy.canvas = IF.game_features['spycanvas']
    spy.row = 1
    spy.col = 0
    spy.draw_face()
    update_question_buttons()
    game_settings['game'] = GW.GuessWho(game_settings['players'], game_settings['candidates'])


def run_window() -> None:
    """Runs the main GUI"""
    IF.summon_main_menu()
    for button in IF.game_features['pb']:
        button.config(command=lambda p=button['text']: select_player(p))


def new_game() -> None:
    """Starts a new game of GuessWho"""
    game_settings['candidates'] = GW.create_candidates('data/questions.csv', 24)
    candidates1 = game_settings['candidates'].copy()
    game_settings['questions'] = GW.generate_all_possible_questions('data/questions.csv')

    questions1 = game_settings['questions'].copy()
    player1 = HumanPlayer(candidates1, questions1)
    player1.select_spy()
    game_settings['players'] = [player1]
    run_window()


def initiate() -> None:
    """Runs the main code for the game."""
    window = Tk()
    game_settings['window'] = window

    frame = Frame(window, width=900, height=600)
    frame.pack(side="top", expand=True, fill="both")
    frame.pack_propagate(False)
    IF.set_frame(frame)
    new_game()
    run_window()
    window.mainloop()


if __name__ == '__main__':
#     candidates = guess_who.create_candidates('data/questions.csv', 12)  # Define data to initialize two players
#     candidates1 = candidates.copy()
#     questions = guess_who.generate_all_possible_questions('data/questions.csv')

    # Sample call to run GuessWho 100 times between GreedyPlayer and PoorPlayer.
    # You may change the first parameter in run_games to determine how many games you would like to run.
    # You may change the last two parameters False, to not print out the winning probability of
    # each player(last parameter), or to not plot the game results(second last parameter).
#     player1 = GreedyPlayer(candidates, questions)
#     player2 = PoorPlayer(candidates1, questions)
#     run_games(100, [player1, player2], 12, 'data/questions.csv', True, True)
    # You can see GreedyPlayer has obviously better performance.

    # Below is a Sample call to run GuessWho 100 times with same setting, but between GreedyPlayer
    # and RandomPlayer.
    # player1 = GreedyPlayer(candidates, questions)
    # player2 = RandomPlayer(candidates1, questions)
    # run_games(100, [player1, player2], 12, 'data/questions.csv', True, True)

    # You should notice a more nuanced difference between the performance of RandomPlayer and GreedyPlayer
    # and the performance of PoorPlayer and GreedyPlayer. Sometimes GreedyPlayer and RandoPlayer may even have the same 
    # winning probability!
    
    # Starts the main GUI
    initiate()
    
