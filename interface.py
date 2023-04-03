"""CSC111 Winter 2023 Project: Guess Who Artifical Intelligence
This module contains the classes and necessary functions to execute
the frontend of the classic game "Guess Who".
"""
from __future__ import annotations

from tkinter import *

from guess_who import *
from features import *

import artificial_intelligence as AI

########################################################################################################################
GAME_SETTINGS = {}
FRAME = None
GAME_FEATURES = {}
GUESS_FRAME_OBJECTS = {}
QUESTION_FRAME_OBJECTS = {}
CONVERSATION_FRAME_OBJECTS = {}
PROFILE_CANVAS = None
TEXT_BOX = None

CHARACTERISTICS = [HAIRPARTITION,
                   CURLYHAIR,
                   HAT,
                   BALD,
                   SMALLMOUTH,
                   LONGHAIR,
                   RED,
                   GRAY,
                   BROWN,
                   BLONDE,
                   BLACK,
                   BIGMOUTH,
                   BIGNOSE,
                   REDCHEEKS,
                   BLUEEYES,
                   EYEBROWS,
                   FACIALHAIR,
                   MOUSTACHE,
                   BEARD,
                   GLASSES,
                   EARRING,
                   SMALLEARS
                   ]


########################################################################################################################


class HumanPlayer(Player):
    """The class representing the human player."""

    def __init__(self, candidates: dict[str, dict[str, str]], questions: list[str]) -> None:
        Player.__init__(self, candidates, questions, 'HumanPlayer')

    def make_guesses(self) -> str:
        """Make a guess at the enemy's spy."""
        return GUESS_FRAME_OBJECTS['label']['text']

    def ask_questions(self) -> str:
        """Asks a question based on which question the player selected."""
        return GAME_SETTINGS['question'] + '?'


########################################################################################################################
# MAIN PART TO RUN THE GUI BACKEND #
########################################################################################################################


def make_a_guess() -> None:
    """Makes the current guess for the HumanPlayer.
    Clears chat box.
    Runs the guess through the game.
    Possible tie covered.
    Disables all buttons.
    """
    clear_chat()
    p1 = GAME_SETTINGS['players'][0]
    q1 = p1.make_guesses()

    g2 = GAME_SETTINGS['players'][1].make_guesses()
    if GAME_SETTINGS['players'][1].spy == q1:
        insert_conversation('You are correct!\n\nComputer made \nthe final guess:\n' + g2 + '\n')

        if g2 == GAME_SETTINGS['players'][0].spy:
            insert_conversation('The Computer \nguessed correctly!\nIt is a tie\n')

        else:
            insert_conversation('The Computer \nguessed incorrectly!\nYou win!\n')

    else:
        print(GAME_SETTINGS['players'][1].spy)
        insert_conversation('You are incorrect!\n\nComputer made \nthe final guess:\n' + g2 + '\n')
        if g2 == GAME_SETTINGS['players'][0].spy:
            insert_conversation('The Computer \nguessed correctly!\nYou lose!\n')

        else:
            insert_conversation('The Computer \nguessed incorrectly!\nIt is a tie!\n')

    disable_all()
    disable_guessing()


def make_a_final_guess() -> None:
    """Makes the current final guess for the HumanPlayer. This is the guess where the computer has already guessed."""
    p1 = GAME_SETTINGS['players'][0]
    q1 = p1.make_guesses()

    if GAME_SETTINGS['players'][1].spy == q1:
        insert_conversation('You are correct!\nIt is a tie!')
    else:
        insert_conversation('You lost!\nMy Spy: ' + GAME_SETTINGS['players'][1].spy)

    insert_conversation('''Let's play again!\nClick menu\nto reset''')
    disable_all()
    disable_guessing()


def make_a_question() -> None:
    """Makes a question for the HumanPlayer"""
    clear_chat()
    p1 = GAME_SETTINGS['players'][0]
    q1 = p1.ask_questions()
    insert_conversation('You asked if the \ncomputer has:\n'
                        + feature_to_text(GAME_SETTINGS['question'])
                        + '\n')

    a1 = GAME_SETTINGS['game'].return_answer(q1, 2)  # Y or N
    print(a1)
    if a1 == 'Y':
        insert_conversation('Yes!\nMy spy has the\nfeature:\n'
                            + feature_to_text(GAME_SETTINGS['question']) + '\n')

        for face in GAME_FEATURES['faces']:
            if GAME_SETTINGS['question'] not in face.chars:
                face.up = False
                face.cover()

    else:
        insert_conversation('No!\nMy spy does not have\nthe feature:\n'
                            + feature_to_text(GAME_SETTINGS['question']) + '\n')

        for face in GAME_FEATURES['faces']:
            if GAME_SETTINGS['question'] in face.chars:
                face.up = False
                face.cover()

    QUESTION_FRAME_OBJECTS['label']['text'] = 'Choose Quesiton'
    p1.eliminate_candidates(q1, a1)
    computer_make_a_question()


def disable_all() -> None:
    """Disables all buttons on the main board. (except menu and exit)"""
    for b in QUESTION_FRAME_OBJECTS['buttons']:
        b.config(state=DISABLED)
    QUESTION_FRAME_OBJECTS['questionbutton'].config(state=DISABLED)
    QUESTION_FRAME_OBJECTS['clearbutton'].config(state=DISABLED)

    GUESS_FRAME_OBJECTS['guessbutton'].config(state=DISABLED)
    GUESS_FRAME_OBJECTS['clearbutton'].config(state=DISABLED)


def enable_all() -> None:
    """Enables all buttons on the main board."""
    for b in QUESTION_FRAME_OBJECTS['buttons']:
        b.config(state=NORMAL)
    QUESTION_FRAME_OBJECTS['questionbutton'].config(state=DISABLED)
    QUESTION_FRAME_OBJECTS['clearbutton'].config(state=NORMAL)

    GUESS_FRAME_OBJECTS['guessbutton'].config(state=DISABLED)
    GUESS_FRAME_OBJECTS['clearbutton'].config(state=NORMAL)


def computer_make_a_guess() -> None:
    """Makes the computer make its guess and gives the player an option to make their guess."""
    g2 = GAME_SETTINGS['players'][1].make_guesses()

    insert_conversation('You are correct!\nComputer made \nthe final guess:\n' + g2 + '\n')
    insert_conversation('The Computer \nguessed correctly!\nIt is your turn\nto tie it up!')

    disable_all()

    GUESS_FRAME_OBJECTS['clearbutton'].config(state=NORMAL)
    GUESS_FRAME_OBJECTS['guessbutton'].config(command=make_a_final_guess)
    clear_selection()


def computer_make_a_question() -> None:
    """Makes the computer make its question move."""
    disable_all()

    p2 = GAME_SETTINGS['players'][1]

    if len(p2.candidates) == 1:
        computer_make_a_guess()
    else:
        q2 = p2.ask_questions()
        a2 = GAME_SETTINGS['game'].return_answer(q2, 1)
        p2.eliminate_candidates(q2, a2)
        insert_conversation('The computer has \nasked if you have:\n' + feature_to_text(q2[0]) + '\n')

        if a2 == 'Y':
            insert_conversation('Your spy has this\nattribute!\n')
        else:
            insert_conversation('Your spy does not have this attribute!\n')
        enable_all()
        clear_selection()


def select_question(button: Button) -> None:
    """Selects a question and stores it from the specific button."""
    global GAME_SETTINGS

    GAME_SETTINGS['question'] = text_to_feature(button['text'])

    for b in QUESTION_FRAME_OBJECTS['buttons']:

        if b['text'] == button['text']:
            b.config(state=DISABLED)

        else:
            b.config(state=NORMAL)

    QUESTION_FRAME_OBJECTS['label'].config(text=button['text'])
    QUESTION_FRAME_OBJECTS['questionbutton'].config(state=NORMAL)


def text_to_player(text: str) -> Player:
    """Converts the text to the respective player and initializes the object, then returns it.
    Necessary for selecting a difficulty."""
    if text == 'GreedyPlayer':
        return AI.GreedyPlayer(GAME_SETTINGS['candidates'].copy(), GAME_SETTINGS['questions'].copy())
    elif text == 'RandomPlayer':
        return AI.RandomPlayer(GAME_SETTINGS['candidates'].copy(), GAME_SETTINGS['questions'].copy())
    elif text == 'CrazyPlayer':
        return AI.CrazyPlayer(GAME_SETTINGS['candidates'].copy(), GAME_SETTINGS['questions'].copy())
    else:
        return AI.PoorPlayer(GAME_SETTINGS['candidates'].copy(), GAME_SETTINGS['questions'].copy())


def update_question_buttons() -> None:
    """Updates all the question buttons in the button frame to be able to select a question or make a guess."""
    GAME_FEATURES['menu'].config(command=new_game)

    for button in QUESTION_FRAME_OBJECTS['buttons']:
        q = text_to_feature(button['text']) + '?'

        if q in GAME_SETTINGS['players'][0].questions:
            button.config(state=NORMAL, command=lambda b=button: select_question(b))

    GUESS_FRAME_OBJECTS['guessbutton'].config(command=make_a_guess)
    QUESTION_FRAME_OBJECTS['questionbutton'].config(command=make_a_question)


def select_player(difficulty: str) -> None:
    """Selects the player that will play (AI)"""
    global GAME_SETTINGS

    player2 = text_to_player(difficulty)  # Finds difficulty
    player2.select_spy()  # Randomly chooses spy

    # print(player2.spy)  # Enable to guess eaiser

    GAME_SETTINGS['players'].append(player2)
    clear_frame()
    summon_main_board()

    spy = name_to_face(GAME_SETTINGS['players'][0].spy)
    spy.canvas = GAME_FEATURES['spycanvas']

    # Necessary for face to grid properly
    spy.row = 1
    spy.col = 0
    spy.draw_face()

    update_question_buttons()
    GAME_SETTINGS['game'] = GuessWho(GAME_SETTINGS['players'], GAME_SETTINGS['candidates'])


def run_window() -> None:
    """Runs the main GUI. Give player buttons the select player option in the main menu."""
    summon_main_menu()
    for button in GAME_FEATURES['pb']:
        button.config(command=lambda p=button['text']: select_player(p))


def new_game() -> None:
    """Starts a new game of GuessWho. Fresh start and then run the main window of the game."""
    GAME_SETTINGS['candidates'] = create_candidates('data/questions.csv', 24)  # 24 people NECESSARY.
    candidates1 = GAME_SETTINGS['candidates'].copy()
    GAME_SETTINGS['questions'] = generate_all_possible_questions('data/questions.csv')

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
    window.title('GuessWho Game')
    frame = Frame(window, width=900, height=600)
    frame.pack(side="top", expand=True, fill="both")
    frame.pack_propagate(False)
    set_frame(frame)

    new_game()
    run_window()
    window.mainloop()


########################################################################################################################


def set_frame(frm: Frame) -> None:
    """Changes the global variable frame to the given frame."""
    global FRAME

    FRAME = frm


def clear_selection() -> None:
    """Clears the current selection"""
    GUESS_FRAME_OBJECTS['label'].config(text='Select a face')
    GUESS_FRAME_OBJECTS['guessbutton'].config(state=DISABLED)


def clear_question() -> None:
    """Clears the current question"""
    QUESTION_FRAME_OBJECTS['label'].config(text='Choose Question')
    for button in QUESTION_FRAME_OBJECTS['buttons']:
        button.config(state=NORMAL)
    QUESTION_FRAME_OBJECTS['questionbutton'].config(state=DISABLED)


def disable_guessing() -> None:
    """Disables the function of the guessing button at the end of a game round."""
    GUESS_FRAME_OBJECTS['guessbutton'].config(state=DISABLED)
    for face in GAME_FEATURES['faces']:
        unbind_hovering(face)


########################################################################################################################


class Face:
    """Responsible for being the canvas of the face of a person.

    Instance Attributes:
    - person: Stores the person class behind the face
    - canvas: The Canvas object on which the face is drawn
    - rect: The rectangle behind the face (to change colour when mouse is move over it)
    - col: The column of the face
    - row: The row of the face
    - chars: The person's characteristics
    - can_hover: Whether the face highlights when hovered over

    Representation Invariants:
    - self.person is not None
    - self.canvas is not None or self.rect is None
    """
    person: Person
    canvas: Optional[Canvas]
    rect: Optional[rect]
    col: int
    row: int
    chars: set[str]
    can_hover: bool

    def __init__(self, person: Person, game_frame: Optional[LabelFrame], col: int, row: int) -> None:
        self.person = person
        self.canvas = Canvas(
            game_frame,
            width=60, height=60,
            bg="dark gray",
        )
        self.rect = self.canvas.create_rectangle(5, 5, 58, 58, fill='gray', outline='light gray')
        self.col = col
        self.row = row
        self.chars = person.features
        self.can_hover = True

    def copy(self) -> Face:
        """Returns a copy of itself.
        New initialization."""
        return Face(self.person, None, self.col, self.row)

    def draw_face(self) -> None:
        """Draws an individual face onto self.canvas.
        Clear the canvas workspace.
        If the canvas is not a profile canvas, initialize it only the correct grid square in the face_frame.
        If one can_hover, then draw all the necessary characteristics, otherwise draw a question mark.
        """
        self.canvas.delete('all')
        self.rect = self.canvas.create_rectangle(5, 5, 58, 58, fill='gray', outline='light gray')
        if self.canvas != PROFILE_CANVAS:
            self.canvas.grid(row=self.row, column=self.col, padx=8, pady=10)
        create_circle(30, 30, 20, self.canvas, 'yellow', 'black')

        if self.can_hover:
            self.draw_eyes()
            self.draw_hair()
            self.draw_nose()
            self.draw_accessory()
            self.draw_mouth()
            self.draw_ears()
            self.canvas.create_text(30, 55, text=self.person.name, fill="black", font='Helvetica 8 bold')
            if self.canvas != PROFILE_CANVAS:
                bind_hovering(self)
        else:
            self.canvas.create_arc(20, 20, 40, 40, start=-90, extent=270, width=3, style='arc')
            self.canvas.create_line(30, 45, 30, 40, width=3)
            self.canvas.create_oval(28, 48, 32, 52, fill='black')
            unbind_hovering(self)

    def draw_eyes(self) -> None:
        """Draws the eyes of the Face."""
        x1 = 25
        x2 = x1 + 10
        y = 20

        # Determine the eye colour
        eye_colour = 'black'
        if BLUEEYES in self.chars:
            eye_colour = 'light blue'

        # Draw the whites of the eyes
        create_circle(x1, y, 4, self.canvas, 'white', 'black')
        create_circle(x2, y, 4, self.canvas, 'white', 'black')

        # Draw the irises
        create_circle(x1, y, 2, self.canvas, eye_colour, 'black')
        create_circle(x2, y, 2, self.canvas, eye_colour, 'black')

    def draw_hair(self) -> None:
        """Draws the hair of the Face."""
        # Determine the hair colour
        if BLONDE in self.chars:
            colour = 'navajo white'
        elif BLACK in self.chars:
            colour = 'black'
        elif BROWN in self.chars:
            colour = 'brown'
        elif RED in self.chars:
            colour = 'red'
        else:
            colour = 'light gray'

        # Draws the Eyebrows
        if EYEBROWS in self.chars:
            x1 = 18
            y1 = 17
            x2 = x1 + 10
            self.canvas.create_rectangle(x1, y1, x2, y1 + 2, fill=colour, outline='black')
            x1 += 15
            x2 += 15
            self.canvas.create_rectangle(x1, y1, x2, y1 + 2, fill=colour, outline='black')

        # Draws the facial hair
        x1 = 20
        y1 = 35
        x2 = x1 + 20
        if MOUSTACHE in self.chars:  # Draws the moustache
            self.canvas.create_rectangle(x1, y1, x2, y1, fill=colour, outline=colour)
        if BEARD in self.chars:  # Draws the beard
            x3 = 10
            y3 = 50
            self.canvas.create_arc(x3, x3, y3, y3, start=-30, style='arc', extent=-120, outline=colour, width=4)

        # Assign length
        length = 1
        if LONGHAIR in self.chars:
            length = 15
        elif BALD in self.chars:
            self.canvas.create_rectangle(9, 20, 15, 25, fill=colour, outline=colour)
            self.canvas.create_rectangle(45, 20, 51, 25, fill=colour, outline=colour)

            # Early return as no other hair
            return

        # Creates the main hairline
        self.canvas.create_arc(10, 10, 50, 50, start=0, extent=180, width=4, style='arc', fill=colour, outline=colour)

        if CURLYHAIR in self.chars:  # Curly hair (circles)
            for i in range(1, 4):
                create_circle(11, 24 + i * 6, 3, self.canvas, colour, colour)
                create_circle(50, 24 + i * 6, 3, self.canvas, colour, colour)
        else:  # Regular straight hair
            self.canvas.create_rectangle(9, 30, 11, 35 + length, fill=colour, outline=colour)
            self.canvas.create_rectangle(49, 30, 51, 35 + length, fill=colour, outline=colour)

        if HAIRPARTITION in self.chars:  # Creates a hair partition
            self.canvas.create_arc(10, 10, 50, 50, start=10, style='arc', extent=70, outline=colour, width=7)
            self.canvas.create_arc(10, 10, 50, 50, start=90, style='arc', extent=70, outline=colour, width=7)

    def draw_ears(self) -> None:
        """Draws the ears of the face."""
        # Determine size
        if SMALLEARS in self.chars:
            rad = 2
        else:
            rad = 4

        # Draw actual ears
        x1 = 10
        y1 = 30
        x2 = x1 + 40
        create_circle(x1, y1, rad, self.canvas, 'yellow', 'black')
        create_circle(x2, y1, rad, self.canvas, 'yellow', 'black')

    def draw_nose(self) -> None:
        """Draws the nose of the face."""
        # Determine size
        if BIGNOSE in self.chars:
            rad = 14
        else:
            rad = 8

        # Draw nose
        x = 30
        y = 25
        self.canvas.create_polygon(x, y, x, y + 10, x + rad, y + 10, fill='orange')

    def draw_accessory(self) -> None:
        """Draws the accessory of the face."""
        if HAT in self.chars:  # Draw hat
            x1 = 10
            y1 = 10
            x2 = x1 + 40
            y2 = y1 + 5

            self.canvas.create_rectangle(x1, y1, x2, y2, fill='brown', outline='black')  # Draw brim
            self.canvas.create_rectangle(x1 + 10, 0, x2 - 10, y1, fill='brown', outline='black')  # Draw top

        if GLASSES in self.chars:  # Graw classes
            # Lenses
            x1 = 20
            y1 = 20
            x2 = x1 + 10
            y2 = y1 + 5
            dx = 10
            self.canvas.create_rectangle(x1, y1, x2, y2, outline='black')
            self.canvas.create_rectangle(x1 + dx, y1, x2 + dx, y2, outline='black')

            # Side thingies
            y1 = 23
            self.canvas.create_line(x1, y1, x1 - 10, y1, width=2)
            x2 += dx
            self.canvas.create_line(x2, y1, x2 + 10, y1, width=2)

        if REDCHEEKS in self.chars:  # Red Cheeks
            create_circle(20, 30, 3, self.canvas, 'red', 'red')
            create_circle(40, 30, 3, self.canvas, 'red', 'red')

        if EARRING in self.chars:  # Earrings are simple green circles
            create_circle(10, 33, 3, self.canvas, 'green', 'black')
            create_circle(50, 33, 3, self.canvas, 'green', 'black')

    def draw_mouth(self) -> None:
        """Draws the mouth of the face."""
        # Determine size
        if SMALLMOUTH in self.chars:
            x1, y1, x2, y2 = 28, 37, 33, 42
        elif BIGMOUTH in self.chars:
            x1, y1, x2, y2 = 25, 32, 37, 43
        else:
            x1, y1, x2, y2 = 25, 35, 37, 43

        # Draw actual mouth
        self.canvas.create_arc((x1, y1, x2, y2), start=0, extent=-180, fill='black', style='chord')

    def cover(self) -> None:
        """Covers the canvas as the character's attribute has already been guessed.
        Called in main.py. Deletes the character's face and instead draws a question mark. Unbind the hovering
        and also clear the selection in case this character was selected."""
        self.canvas.delete('all')
        self.rect = self.canvas.create_rectangle(5, 5, 58, 58, fill='gray', outline='light gray')
        self.canvas.create_arc(20, 20, 40, 40, start=-90, extent=270, width=3, style='arc')
        self.canvas.create_line(30, 45, 30, 40, width=3)
        self.canvas.create_oval(28, 48, 32, 52, fill='black')
        unbind_hovering(self)
        clear_selection()

    def characteristics_to_text_box(self) -> None:
        """Converts the current Face's characteriscs to text and put them in text box.
        Adds it to one accumulating string and finally inserts it.

        This lists all the characteristics in the left side text box when specifying a Face in a profile."""
        TEXT_BOX.config(state=NORMAL)  # Open textbox
        TEXT_BOX.delete('1.0', END)  # Clear it

        text_so_far = f"{self.person.name} has the\nfollowing \ncharacteristics:\n\n"  # ACCUMULATOR

        if HAIRPARTITION in self.chars:
            text_so_far += 'Hair Partition\n'
        if CURLYHAIR in self.chars:
            text_so_far += 'Curly Hair\n'
        if HAT in self.chars:
            text_so_far += 'Hat\n'
        if BALD in self.chars:
            text_so_far += 'Bald\n'
        if SMALLMOUTH in self.chars:
            text_so_far += 'Small Mouth\n'
        if LONGHAIR in self.chars:
            text_so_far += 'Long Hair\n'
        if RED in self.chars:
            text_so_far += 'Red Hair\n'
        if GRAY in self.chars:
            text_so_far += 'Gray Hair\n'
        if BROWN in self.chars:
            text_so_far += 'Brown Hair\n'
        if BLONDE in self.chars:
            text_so_far += 'Blonde Hair\n'
        if BLACK in self.chars:
            text_so_far += 'Black Hair\n'
        if BIGMOUTH in self.chars:
            text_so_far += 'Big Mouth\n'
        if BIGNOSE in self.chars:
            text_so_far += 'Big Nose\n'
        if REDCHEEKS in self.chars:
            text_so_far += 'Rosy Cheeks\n'
        if BLUEEYES in self.chars:
            text_so_far += 'Blue Eyes\n'
        if EYEBROWS in self.chars:
            text_so_far += 'Eye Brows\n'
        if FACIALHAIR in self.chars:
            text_so_far += 'Facial Hair\n'
        if MOUSTACHE in self.chars:
            text_so_far += 'Moustache\n'
        if BEARD in self.chars:
            text_so_far += 'Beard\n'
        if GLASSES in self.chars:
            text_so_far += 'Glasses\n'
        if EARRING in self.chars:
            text_so_far += 'Earrings\n'
        if SMALLEARS in self.chars:
            text_so_far += 'Small Ears\n'

        TEXT_BOX.insert('1.0', text_so_far)
        TEXT_BOX.config(state=DISABLED)  # Disable it


def name_to_face(name: str) -> Face:
    """Returns the corresponding face to the name."""
    return [face.copy() for face in GAME_FEATURES['faces'] if face.person.name == name][0]


def lock(event: Event, face: Face) -> None:
    """Keeps the current face as a selection.
    Changes the GAME_FEATURES and updates the guess frame to hold the current select Face for
    a potential guess."""
    global GAME_FEATURES

    GAME_FEATURES['guess'] = face.person.name

    GUESS_FRAME_OBJECTS['label'].config(text=face.person.name)
    GUESS_FRAME_OBJECTS['guessbutton'].config(state=NORMAL)


def hover(event: Event, face: Face) -> None:
    """Changes the face object to a hover state.
    When the mouse is not hover over the respective face:
        Shows face in Profiler and adds text to text box.
        Highlights original canvas as red."""
    if face.can_hover:
        face.canvas.itemconfig(face.rect, fill='red')
        face_2 = face.copy()
        face_2.canvas = PROFILE_CANVAS
        face_2.draw_face()
        TEXT_BOX.delete('1.0', END)
        face.characteristics_to_text_box()


def unhover(event: Event, face: Face) -> None:
    """Changes the face object to its original state.
    When the mouse is not hovering over the respective face:
        Clears profiler.
        Unhighlights original canvas.
    """
    global TEXT_BOX
    global PROFILE_CANVAS

    if face.can_hover:
        face.canvas.itemconfig(face.rect, fill='gray')
        PROFILE_CANVAS.delete('all')
        PROFILE_CANVAS.create_rectangle(0, 0, 60, 65, fill='gray')
        TEXT_BOX.config(state=NORMAL)
        TEXT_BOX.delete('1.0', END)
        TEXT_BOX.config(state=DISABLED)


def unbind_hovering(face: Face) -> None:
    """Unbinds the hvoereing mechanic of the face."""
    face.canvas.unbind('<Enter>')
    face.canvas.unbind('<Leave>')
    face.canvas.unbind('<Button-1>')


def bind_hovering(face: Face) -> None:
    """Binds the hovering and unhovering events to when the mouse enter/leaves the object.
    Makes it so unhover and hover function work, also that cicking selects a guess."""
    face.canvas.bind("<Enter>", lambda event, f=face: hover(event, f))
    face.canvas.bind("<Leave>", lambda event, f=face: unhover(event, f))

    face.canvas.bind("<Button-1>", lambda event, f=face: lock(event, f))


def person_to_face(person: Person, game_frame: LabelFrame, curr_row: int, curr_col: int) -> Face:
    """Converts a Person to a Face."""
    face = Face(person, game_frame, curr_col, curr_row)
    return face


def persons_to_faces(persons: list[Person], game_frame: LabelFrame) -> list[Face]:
    """Converts the person dataclasses to Face classes.
    Reads the given person list, converts them puts them in the given game_frame.
    Helper function call to person_to_face."""
    faces_so_far = []
    curr_row = 0
    curr_col = 0

    for person in persons:
        faces_so_far.append(person_to_face(person, game_frame, curr_row, curr_col))

        curr_col += 1
        if curr_col == 6:
            curr_col = 0
            curr_row += 1

    return faces_so_far


def text_to_feature(feature: str) -> str:
    """Converts the question to the necessary constant."""
    text = ''

    if feature == 'Hair Partition':
        text = HAIRPARTITION
    elif feature == 'Curly Hair':
        text = CURLYHAIR
    elif feature == 'Hat':
        text = HAT
    elif feature == 'Bald':
        text = BALD
    elif feature == 'Small Mouth':
        text = SMALLMOUTH
    elif feature == 'Long Hair':
        text = LONGHAIR
    elif feature == 'Red Hair':
        text = RED
    elif feature == 'Gray Hair':
        text = GRAY
    elif feature == 'Brown Hair':
        text = BROWN
    elif feature == 'Blonde Hair':
        text = BLONDE
    elif feature == 'Black Hair':
        text = BLACK
    elif feature == 'Big Mouth':
        text = BIGMOUTH
    elif feature == 'Big Nose':
        text = BIGNOSE
    elif feature == 'Rosy Cheeks':
        text = REDCHEEKS
    elif feature == 'Blue Eyes':
        text = BLUEEYES
    elif feature == 'Eye Brows':
        text = EYEBROWS
    elif feature == 'Facial Hair':
        text = FACIALHAIR
    elif feature == 'Moustache':
        text = MOUSTACHE
    elif feature == 'Beard':
        text = BEARD
    elif feature == 'Glasses':
        text = GLASSES
    elif feature == 'Earrings':
        text = EARRING
    elif feature == 'Small Ears':
        text = SMALLEARS

    return text


def feature_to_text(feature: str) -> str:
    """Converts the given feature to text."""
    text = ''

    if feature == HAIRPARTITION:
        text = 'Hair Partition'
    elif feature == CURLYHAIR:
        text = 'Curly Hair'
    elif feature == HAT:
        text = 'Hat'
    elif feature == BALD:
        text = 'Bald'
    elif feature == SMALLMOUTH:
        text = 'Small Mouth'
    elif feature == LONGHAIR:
        text = 'Long Hair'
    elif feature == RED:
        text = 'Red Hair'
    elif feature == GRAY:
        text = 'Gray Hair'
    elif feature == BROWN:
        text = 'Brown Hair'
    elif feature == BLONDE:
        text = 'Blonde Hair'
    elif feature == BLACK:
        text = 'Black Hair'
    elif feature == BIGMOUTH:
        text = 'Big Mouth'
    elif feature == BIGNOSE:
        text = 'Big Nose'
    elif feature == REDCHEEKS:
        text = 'Rosy Cheeks'
    elif feature == BLUEEYES:
        text = 'Blue Eyes'
    elif feature == EYEBROWS:
        text = 'Eye Brows'
    elif feature == FACIALHAIR:
        text = 'Facial Hair'
    elif feature == MOUSTACHE:
        text = 'Moustache'
    elif feature == BEARD:
        text = 'Beard'
    elif feature == GLASSES:
        text = 'Glasses'
    elif feature == EARRING:
        text = 'Earrings'
    elif feature == SMALLEARS:
        text = 'Small Ears'

    return text


def clear_frame() -> None:
    """Clears the global FRAME.

    Preconditions:
    - len(frame.winfo_children()) >= 1
    """
    for widgets in FRAME.winfo_children():
        widgets.destroy()

    FRAME.grid_propagate(False)


def create_profiler() -> None:
    """Creates the profile labelframe and canvas.
    PROFILE_CANVAS: The canvas containing the Face which the player is seeing the characteristics of
    TEXT_BOX: Has the actual characteristics of the Face being hovered over
    GAME_FEATURES: Stores the spy_canvas to show the player's spy."""
    global PROFILE_CANVAS
    global TEXT_BOX
    global GAME_FEATURES

    profile_frame = LabelFrame(FRAME, text="Profiler", font='Helvetica 16 bold')

    spy_label = Label(profile_frame, text="Your Spy:", font='Helvetica 10 bold')
    spy_label.grid(row=0, column=0)

    spy_canvas = Canvas(profile_frame, width=55, height=60, borderwidth=2, relief='solid')
    spy_canvas.create_rectangle(0, 0, 60, 65, fill='gray')
    spy_canvas.grid(row=1, column=0, padx=5, pady=10)
    GAME_FEATURES['spycanvas'] = spy_canvas

    PROFILE_CANVAS = Canvas(profile_frame, width=55, height=60, borderwidth=2, relief="solid")
    PROFILE_CANVAS.create_rectangle(0, 0, 60, 65, fill='gray')
    PROFILE_CANVAS.grid(row=1, column=1, padx=5, pady=10)

    TEXT_BOX = Text(profile_frame, width=20, height=12, state='disabled')
    TEXT_BOX.grid(row=2, column=0, columnspan=2, padx=10, pady=14)

    profile_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10)


def create_menu_button() -> None:
    """Creates the button that will take the player back to main menu."""
    GAME_FEATURES['menu'] = Button(FRAME, text='Menu', width=10)
    GAME_FEATURES['menu'].grid(row=2, column=1, padx=10, pady=10)


def create_exit() -> None:
    """Creates the exit button for the main game board. Inserts it."""
    exit_button = Button(
        FRAME,
        text="Exit",
        width=10,
        command=exit,
        bg='red'
    )
    exit_button.grid(row=2, column=0, pady=10)


def create_guess_frame() -> None:
    """Creates the place to make a final guess.
    Everything is stored into GUESS_FRAME_OBJECTS
    - 'frame': The LabelFrame containing everything.
    - 'clearbutton': Clears the current guess selection.
    - 'label': Label of the guess
    - 'guessbutton': Supposed to make a guess later on."""
    global GUESS_FRAME_OBJECTS

    GUESS_FRAME_OBJECTS['frame'] = LabelFrame(FRAME, text="Guess", font='Helvetica 16 bold')
    guess_frame = GUESS_FRAME_OBJECTS['frame']

    GUESS_FRAME_OBJECTS['label'] = Label(guess_frame, text="Select a face", font='Helvetica 10 bold')

    GUESS_FRAME_OBJECTS['guessbutton'] = Button(guess_frame, text="Make Guess", state=DISABLED)
    GUESS_FRAME_OBJECTS['clearbutton'] = Button(guess_frame, text="Clear Selection", command=clear_selection)

    GUESS_FRAME_OBJECTS['label'].pack(padx=10, pady=5)
    GUESS_FRAME_OBJECTS['guessbutton'].pack(side=LEFT, padx=5, pady=5)
    GUESS_FRAME_OBJECTS['clearbutton'].pack(side=RIGHT, padx=5, pady=5)

    GUESS_FRAME_OBJECTS['frame'].grid(row=1, column=0, columnspan=2, padx=0, pady=10)


def create_faces() -> None:
    """Create Face classes and draw them into game_frame. All of them."""
    global GAME_FEATURES

    main_menu_labelframe = LabelFrame(
        FRAME,
        text="FACES",
        font=('Helvetica', 16, 'bold')
    )
    main_menu_labelframe.grid(row=0, column=2, columnspan=3, padx=5, pady=10)

    persons = load_persons('data/characteristics.csv')
    assert len(persons) == 24

    faces = persons_to_faces(persons, main_menu_labelframe)
    GAME_FEATURES['faces'] = faces
    for face in faces:
        face.draw_face()


def create_question_frame() -> None:
    """Creates the place to make a final guess.
    Everything is stored into QUESITON_FRAME_OBJECTS
    - 'frame': The LabelFrame containing everything.
    - 'clearbutton': Clears the current question selection.
    - 'buttons': Contains every quesitons Button object
    - 'label': Label of the question
    - 'questionbutton': Supposed to make a quesiton later on."""
    global QUESTION_FRAME_OBJECTS

    buttons = []
    QUESTION_FRAME_OBJECTS['frame'] = LabelFrame(FRAME, text="Question Maker", font='Helvetica 16 bold',
                                                 width=600, height=200)
    question_frame = QUESTION_FRAME_OBJECTS['frame']
    curr_feature = 0

    for i in range(3):

        for j in range(6):
            button = Button(question_frame, text=feature_to_text(CHARACTERISTICS[curr_feature]),
                            font='Helvetica 8', width=10)
            button.grid(row=i, column=j, padx=5)
            buttons.append(button)
            curr_feature += 1

    for k in range(1, 5):
        button = Button(question_frame,
                        text=feature_to_text(CHARACTERISTICS[curr_feature]),
                        font='Helvetica 8',
                        width=10)

        button.grid(row=3, column=k, padx=5)
        curr_feature += 1
        buttons.append(button)

    QUESTION_FRAME_OBJECTS['clearbutton'] = Button(question_frame, text="Clear Question", command=clear_question)
    QUESTION_FRAME_OBJECTS['label'] = Label(question_frame, text="Choose Question", font='Helvetica 8 bold')
    QUESTION_FRAME_OBJECTS['questionbutton'] = Button(question_frame, text="Ask Question", state=DISABLED)

    QUESTION_FRAME_OBJECTS['clearbutton'].grid(row=2, column=6, padx=5, pady=5)
    QUESTION_FRAME_OBJECTS['label'].grid(row=0, column=6, padx=10, pady=5)
    QUESTION_FRAME_OBJECTS['questionbutton'].grid(row=1, column=6, padx=10, pady=5)

    QUESTION_FRAME_OBJECTS['buttons'] = buttons

    question_frame.grid(row=1, column=3, columnspan=3, rowspan=2, padx=0, pady=5)
    question_frame.grid_propagate(0)


def clear_chat() -> None:
    """Clears the conversation text box."""
    CONVERSATION_FRAME_OBJECTS['box'].config(state=NORMAL)
    CONVERSATION_FRAME_OBJECTS['box'].delete('1.0', END)
    CONVERSATION_FRAME_OBJECTS['box'].config(state=DISABLED)


def insert_conversation(text: str) -> None:
    """Insert a conversation into the text box."""
    text += '\n'

    CONVERSATION_FRAME_OBJECTS['box'].config(state=NORMAL)
    CONVERSATION_FRAME_OBJECTS['box'].insert(END, text)
    CONVERSATION_FRAME_OBJECTS['box'].config(state=DISABLED)


def create_conversation() -> None:
    """Creates the computer conversation box on the side of the board.
    Everything is stored in CONVERSATION_FRAME_OBJECTS
    - 'frame': Frame where everything is stored.
    - 'box': Conversation box with text later on
    """
    global CONVERSATION_FRAME_OBJECTS

    CONVERSATION_FRAME_OBJECTS['frame'] = LabelFrame(FRAME, text='Computer Says', font='Helvetica 16 bold')
    CONVERSATION_FRAME_OBJECTS['box'] = Text(CONVERSATION_FRAME_OBJECTS['frame'], width=20, height=20, state='disabled',
                                             font='Helvetica 8')

    CONVERSATION_FRAME_OBJECTS['frame'].grid(row=0, column=5, padx=5)
    CONVERSATION_FRAME_OBJECTS['box'].grid(row=0, column=0, padx=10, pady=10)


def summon_main_board() -> None:
    """Summons the main board of the GUI.

    Firstly, clears the frame.
    The summons the following parts of the interface in the following order:
    - main menu button
    - faces with their face frame
    - the guessing frame with the guess button
    - the conversation frame holding the conversation with the computer
    - the exit button
    - the profile frame (also contains spy)
    - the question frame with all quesitons"""

    clear_frame()

    create_menu_button()
    create_faces()
    create_guess_frame()
    create_conversation()
    create_exit()
    create_profiler()
    create_question_frame()


def summon_main_menu() -> None:
    """Creates the main menu with 3 options for the possible AI and buttons to select them.
    Also contains main game title and exit button."""
    clear_frame()

    main_frame = LabelFrame(
        FRAME,
        height=300,
        width=400
    )

    main_label = Label(
        main_frame,
        text="GuessWho",
        font='Helvetica 80 bold'
    )
    main_label_2 = Label(
        main_frame,
        text="the python game.",
        font='Helvetica 12 italic'
    )
    player_buttons = []
    players = ['CrazyPlayer', 'GreedyPlayer', 'RandomPlayer', 'PoorPlayer']

    for player in players:
        player_buttons.append(Button(
            main_frame,
            text=player,
            width=20
        )
        )

    exit_button = Button(
        main_frame,
        text="Exit",
        width=20,
        command=exit,
        bg='red'
    )

    main_frame.pack()
    main_label.pack()
    main_label_2.pack()

    player_buttons[0].pack(pady=(50, 5))

    for i in range(1, 4):
        player_buttons[i].pack(pady=5)

    GAME_FEATURES['pb'] = player_buttons

    exit_button.pack(pady=50)


def create_circle(x: int, y: int, r: int, canvas: Canvas, colour: str, outline_colour: str) -> None:
    """Creates a circle in the given Canvas.
    The circle is filled with the given colour and outlined with outline_colour.
    """
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    canvas.create_oval(
        x0,
        y0,
        x1,
        y1,
        fill=colour,
        width=1,
        outline=outline_colour,
    )


if __name__ == "__main__":
    # window = Tk()
    #
    # FRAME = Frame(window, width=800, height=600)
    # FRAME.pack(side="top", expand=True, fill="both")
    # FRAME.pack_propagate(False)
    #
    # summon_main_menu()
    # window.mainloop()

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['tkinter', 'guess_who', 'features'],
        'disable': ['forbidden-top-level-code',
                    'wildcard-import',
                    'too-many-branches',
                    'forbidden-global-variables',
                    'unused-argument',
                    'too-many-arguments'
                    ],
        'allowed-io': []
    })
