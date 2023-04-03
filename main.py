"""CSC111 Winter 2023 Project: Guess Who Artifical Intelligence
This module contains the classes and necessary functions to execute
the frontend with the backend of the classic game "Guess Who".

The files interface.py and guess_who.py are combined in this file to work together.
artifical_intelligence is provided to play against as an opponent and the player
may choose which opponent to play against.

This file also contins the main function to run games and test performaces between AIs.
"""
from __future__ import annotations

import csv
from tkinter import *

import guess_who as GW
from guess_who import Player

import artificial_intelligence as AI
from artificial_intelligence import RandomPlayer, GreedyPlayer, PoorPlayer

import interface as IF

GAME_SETTINGS = {'question': ''}


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
        can = GW.create_candidates(file, num_cha)
        question = GW.generate_all_possible_questions(file)
        player1.candidates = can
        player2.candidates = can.copy()
        player1.questions = question
        player2.questions = question.copy()
        player1.select_spy()
        player2.select_spy()
        winner = AI.run_game([player1, player2], can.copy())
        if winner == player1.name or winner == player2.name:
            game_sta[winner] += 1
            results[winner][i] = 1
    if p:
        pl1_wins = game_sta[pl1_name]
        pl2_wins = game_sta[pl2_name]
        print(f'[winning_probability:{pl1_name}: {(pl1_wins / num) * 100}%, {pl2_name}: {(pl2_wins / num) * 100}%]')
    if plot:
        AI.plot_game_statistics(results, player1.name, player2.name)

    return results


class HumanPlayer(GW.Player):
    """The class representing the human player."""

    def __init__(self, candidates: dict[str, dict[str, str]], questions: list[str]) -> None:
        GW.Player.__init__(self, candidates, questions, 'HumanPlayer')

    def make_guesses(self, game: GW.GuessWho) -> str:
        """Make a guess at the enemy's spy."""
        return IF.GUESS_FRAME_OBJECTS['label']['text']

    def ask_questions(self, game: GW.GuessWho) -> str:
        """Asks a question based on which question the player selected."""
        return GAME_SETTINGS['question'] + '?'


def make_a_guess() -> None:
    """Makes the current guess for the HumanPlayer.
    Clears chat box.
    Runs the guess through the game.
    Possible tie covered.
    Disables all buttons.
    """
    IF.clear_chat()
    p1 = GAME_SETTINGS['players'][0]
    q1 = p1.make_guesses(GAME_SETTINGS['game'])

    g2 = GAME_SETTINGS['players'][1].make_guesses(GAME_SETTINGS['game'])
    if GAME_SETTINGS['players'][1].spy == q1:
        IF.insert_conversation('You are correct!\n\nComputer made \nthe final guess:\n' + g2 + '\n')

        if g2 == GAME_SETTINGS['players'][0].spy:
            IF.insert_conversation('The Computer \nguessed correctly!\nIt is a tie\n')

        else:
            IF.insert_conversation('The Computer \nguessed incorrectly!\nYou win!\n')

    else:
        IF.insert_conversation('You are incorrect!\n\nComputer made \nthe final guess:\n' + g2 + '\n')
        if g2 == GAME_SETTINGS['players'][0].spy:
            IF.insert_conversation('The Computer \nguessed correctly!\nYou lose!\n')

        else:
            IF.insert_conversation('The Computer \nguessed incorrectly!\nIt is a tie!\n')

    disable_all()


def make_a_final_guess() -> None:
    """Makes the current final guess for the HumanPlayer. This is the guess where the computer has already guessed."""
    p1 = GAME_SETTINGS['players'][0]
    q1 = p1.make_guesses(GAME_SETTINGS['game'])

    if GAME_SETTINGS['players'][1].spy == q1:
        IF.insert_conversation('You are correct!\nIt is a tie!')
    else:
        IF.insert_conversation('You lost!\n')

    IF.insert_conversation('''Let's play again!\nClick menu\nto reset''')
    disable_all()


def make_a_question() -> None:
    """Makes a question for the HumanPlayer"""
    IF.clear_chat()
    p1 = GAME_SETTINGS['players'][0]
    q1 = p1.ask_questions(GAME_SETTINGS['game'])
    IF.insert_conversation('You asked if the \ncomputer has:\n'
                           + IF.convert_feature_to_text(GAME_SETTINGS['question'])
                           + '\n')

    a1 = GAME_SETTINGS['game'].return_answer(q1, 2)  # Y or N

    if a1 == 'Y':
        IF.insert_conversation('Yes!\nMy spy has the\nfeature:\n'
                               + IF.convert_feature_to_text(GAME_SETTINGS['question']) + '\n')

        for face in IF.GAME_FEATURES['faces']:
            if GAME_SETTINGS['question'] not in face.chars:
                face.up = False
                face.cover()

    else:
        IF.insert_conversation('No!\nMy spy does not have\nthe feature:\n'
                               + IF.convert_feature_to_text(GAME_SETTINGS['question']) + '\n')

        for face in IF.GAME_FEATURES['faces']:
            if GAME_SETTINGS['question'] in face.chars:
                face.up = False
                face.cover()

    p1.eliminate_candidates(q1, a1)
    computer_make_a_question()


def disable_all() -> None:
    """Disables all buttons on the main board. (except menu and exit)"""
    for b in IF.QUESTION_FRAME_OBJECTS['buttons']:
        b.config(state=DISABLED)
    IF.QUESTION_FRAME_OBJECTS['questionbutton'].config(state=DISABLED)
    IF.QUESTION_FRAME_OBJECTS['clearbutton'].config(state=DISABLED)

    IF.GUESS_FRAME_OBJECTS['guessbutton'].config(state=DISABLED)
    IF.GUESS_FRAME_OBJECTS['clearbutton'].config(state=DISABLED)


def enable_all() -> None:
    """Disables all buttons on the main board."""
    for b in IF.QUESTION_FRAME_OBJECTS['buttons']:
        b.config(state=NORMAL)
    IF.QUESTION_FRAME_OBJECTS['questionbutton'].config(state=DISABLED)
    IF.QUESTION_FRAME_OBJECTS['clearbutton'].config(state=NORMAL)

    IF.GUESS_FRAME_OBJECTS['guessbutton'].config(state=DISABLED)
    IF.GUESS_FRAME_OBJECTS['clearbutton'].config(state=NORMAL)


def computer_make_a_guess() -> None:
    """Makes the computer make its guess and gives the player an option to make their guess."""
    g2 = GAME_SETTINGS['players'][1].make_guesses(GAME_SETTINGS['game'])

    IF.insert_conversation('You are correct!\nComputer made \nthe final guess:\n' + g2 + '\n')
    IF.insert_conversation('The Computer \nguessed correctly!\nIt is your turn\nto tie it up!')

    disable_all()

    IF.GUESS_FRAME_OBJECTS['clearbutton'].config(state=NORMAL)
    IF.GUESS_FRAME_OBJECTS['guessbutton'].config(command=make_a_final_guess)
    IF.clear_selection()


def computer_make_a_question() -> None:
    """Makes the computer make its question move."""
    disable_all()

    p2 = GAME_SETTINGS['players'][1]

    if len(p2.candidates) == 1:
        computer_make_a_guess()
    else:
        q2 = p2.ask_questions(GAME_SETTINGS['game'])
        a2 = GAME_SETTINGS['game'].return_answer(q2, 1)
        p2.eliminate_candidates(q2, a2)
        IF.insert_conversation('The computer has \nasked if you have:\n' + IF.convert_feature_to_text(q2[0]) + '\n')

        if a2 == 'Y':
            IF.insert_conversation('Your spy has this\nattribute!\n')
        else:
            IF.insert_conversation('Your spy does not have this attribute!\n')
        enable_all()
        IF.clear_selection()


def select_question(button: Button) -> None:
    """Selects a question and stores it from the specific button."""
    global GAME_SETTINGS

    GAME_SETTINGS['question'] = IF.question_to_feature(button['text'])

    for b in IF.QUESTION_FRAME_OBJECTS['buttons']:

        if b['text'] == button['text']:
            b.config(state=DISABLED)

        else:
            b.config(state=NORMAL)

    IF.QUESTION_FRAME_OBJECTS['label'].config(text=button['text'])
    IF.QUESTION_FRAME_OBJECTS['questionbutton'].config(state=NORMAL)


def text_to_player(text: str) -> GW.Player:
    """Converts the text to the respective player and initializes the object, then returns it.
    Necessary for selecting a difficulty."""
    if text == 'GreedyPlayer':
        return AI.GreedyPlayer(GAME_SETTINGS['candidates'].copy(), GAME_SETTINGS['questions'].copy())
    elif text == 'RandomPlayer':
        return AI.RandomPlayer(GAME_SETTINGS['candidates'].copy(), GAME_SETTINGS['questions'].copy())
    else:
        return AI.PoorPlayer(GAME_SETTINGS['candidates'].copy(), GAME_SETTINGS['questions'].copy())


def update_question_buttons() -> None:
    """Updates all the question buttons in the button frame to be able to select a question or make a guess."""
    IF.GAME_FEATURES['menu'].config(command=new_game)

    for button in IF.QUESTION_FRAME_OBJECTS['buttons']:
        q = IF.question_to_feature(button['text']) + '?'

        if q in GAME_SETTINGS['players'][0].questions:
            button.config(state=NORMAL, command=lambda b=button: select_question(b))

    IF.GUESS_FRAME_OBJECTS['guessbutton'].config(command=make_a_guess)
    IF.QUESTION_FRAME_OBJECTS['questionbutton'].config(command=make_a_question)


def select_player(difficulty: str) -> None:
    """Selects the player that will play (AI)"""
    global GAME_SETTINGS

    player2 = text_to_player(difficulty)  # Finds difficulty
    player2.select_spy()  # Randomly chooses spy

    # print(player2.spy)  # Enable to guess eaiser

    GAME_SETTINGS['players'].append(player2)
    IF.clear_frame()
    IF.summon_main_board()

    spy = IF.name_to_face(GAME_SETTINGS['players'][0].spy)
    spy.canvas = IF.GAME_FEATURES['spycanvas']

    # Necessary for face to grid properly
    spy.row = 1
    spy.col = 0
    spy.draw_face()

    update_question_buttons()
    GAME_SETTINGS['game'] = GW.GuessWho(GAME_SETTINGS['players'], GAME_SETTINGS['candidates'])


def run_window() -> None:
    """Runs the main GUI. Give player buttons the select player option in the main menu."""
    IF.summon_main_menu()
    for button in IF.GAME_FEATURES['pb']:
        button.config(command=lambda p=button['text']: select_player(p))


def new_game() -> None:
    """Starts a new game of GuessWho. Frehs start and then run the main window of the game."""
    GAME_SETTINGS['candidates'] = GW.create_candidates('data/questions.csv', 24)  # 24 people NECESSARY.
    candidates1 = GAME_SETTINGS['candidates'].copy()
    GAME_SETTINGS['questions'] = GW.generate_all_possible_questions('data/questions.csv')

    questions1 = GAME_SETTINGS['questions'].copy()
    player1 = HumanPlayer(candidates1, questions1)
    player1.select_spy()
    GAME_SETTINGS['players'] = [player1]
    run_window()


def initiate() -> None:
    """Runs the main code for the game.
    Initiate the main frame and winow."""
    window = Tk()
    GAME_SETTINGS['window'] = window

    frame = Frame(window, width=900, height=600)
    frame.pack(side="top", expand=True, fill="both")
    frame.pack_propagate(False)
    IF.set_frame(frame)

    new_game()
    run_window()
    window.mainloop()


if __name__ == "__main__":
    initiate()

if __name__ == '__main__':
    # candidates = guess_who.create_candidates('data/questions.csv', 12)  # Define data to initialize two players
    # candidates1 = candidates.copy()
    # questions = guess_who.generate_all_possible_questions('data/questions.csv')

    # Sample call to run GuessWho 100 times between GreedyPlayer and PoorPlayer.
    # You may change the first parameter in run_games to determine how many games you would like to run.
    # You may change the last two parameters False, to not print out the winning probability of
    # each player(last parameter), or to not plot the game results(second last parameter).
    # player1 = GreedyPlayer(candidates, questions)
    # player2 = PoorPlayer(candidates1, questions)
    # run_games(100, [player1, player2], 12, 'data/questions.csv', True, True)
    # You can see GreedyPlayer has obviously better performance.

    # Below is a Sample call to run GuessWho 100 times with same setting, but between GreedyPlayer
    # and RandomPlayer.
    # player1 = GreedyPlayer(candidates, questions)
    # player2 = RandomPlayer(candidates1, questions)
    # run_games(100, [player1, player2], 12, 'data/questions.csv', True, True)

    # You should notice a more nuanced difference between the performance of RandomPlayer and GreedyPlayer
    # and the performance of PoorPlayer and GreedyPlayer. Sometimes GreedyPlayer and RandoPlayer may even have the same
    # winning probability!

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['tkinter', 'guess_who', 'features', 'artificial_intelligence', 'csv', 'interface'],
        'disable': ['forbidden-top-level-code',
                    'wildcard-import',
                    'too-many-branches',
                    'forbidden-global-variables',
                    'unused-argument',
                    'too-many-arguments',
                    'too-many-locals',
                    'unused-import'
                    ],
        'allowed-io': []
    })
