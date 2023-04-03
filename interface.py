"""CSC111 Winter 2023 Project: Guess Who Artifical Intelligence
This module contains the classes and necessary functions to execute
the frontend of the classic game "Guess Who".
"""
from __future__ import annotations

import tkinter.ttk
from tkinter import *

from guess_who import *
from features import *

########################################################################################################################
frame = None
game_features = {}
guess_frame_objects = {}
question_frame_objects = {}
conversation_frame_objects = {}
# current_selection = None
profile_canvas = None
text_box = None
# select_spy = True
characteriscs = [HAIRPARTITION,
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

# def change_select_spy() -> None:
#     """Changes the global variable select_spy to the opposite."""
#     global select_spy
#     select_spy = not select_spy


def set_frame(frm: Frame) -> None:
    """Changes the global variable frame to the given frame."""
    global frame

    frame = frm


def clear_selection() -> None:
    """Clears the current selection"""
    # global current_selection

    # current_selection = None
    guess_frame_objects['label'].config(text='Select a face')
    guess_frame_objects['guessbutton'].config(state=DISABLED)


def clear_question() -> None:
    """Clears the current question"""
    question_frame_objects['label'].config(text='Please Select One')
    for button in question_frame_objects['buttons']:
        button.config(state=NORMAL)
    question_frame_objects['questionbutton'].config(state=DISABLED)


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
    """
    person: Person
    canvas: Optional[Canvas]
    rect: Optional[rect]
    col: int
    row: int
    chars: set[str]
    can_hover: bool

    def __init__(self, person: Person, game_frame: Optional[LabelFrame], col: int, row: int):
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
        """Returns a copy of itself"""
        return Face(self.person, None, self.col, self.row)

    def draw_face(self) -> None:
        """Draws an individual face."""
        global game_features
        self.canvas.delete('all')
        self.rect = self.canvas.create_rectangle(5, 5, 58, 58, fill='gray', outline='light gray')
        if self.canvas != profile_canvas:
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
            if self.canvas != profile_canvas:
                bind_hovering(self)
        else:
            self.canvas.create_arc(10, 10, 50, 50, start=-90, extent=270, width=3, style='arc')
            self.canvas.create_line(30, 45, 30, 35, width=3)
            self.canvas.create_oval(25, 55, 35, 65, fill='black')
            unbind_hovering(self)

        game_features[self.person.name] = self

    def draw_eyes(self) -> None:
        """Draws the eyes of the Face."""
        x1 = 25
        x2 = x1 + 10
        y = 20
        eye_colour = 'black'
        if BLUEEYES in self.chars:
            eye_colour = 'light blue'
        create_circle(x1, y, 4, self.canvas, 'white', 'black')
        create_circle(x2, y, 4, self.canvas, 'white', 'black')

        create_circle(x1, y, 2, self.canvas, eye_colour, 'black')
        create_circle(x2, y, 2, self.canvas, eye_colour, 'black')

    def draw_hair(self) -> None:
        """Draws the hair of the Face."""
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

        length = 1
        if LONGHAIR in self.chars:
            length = 15
        elif BALD in self.chars:
            self.canvas.create_rectangle(9, 20, 15, 25, fill=colour, outline=colour)
            self.canvas.create_rectangle(45, 20, 51, 25, fill=colour, outline=colour)
            return

        self.canvas.create_arc(10, 10, 50, 50, start=0, extent=180, width=4, style='arc', fill=colour, outline=colour)

        if CURLYHAIR in self.chars:
            for i in range(1, 4):
                create_circle(11, 24 + i * 6, 3, self.canvas, colour, colour)
                create_circle(50, 24 + i * 6, 3, self.canvas, colour, colour)
        else:
            self.canvas.create_rectangle(9, 30, 11, 35 + length, fill=colour, outline=colour)
            self.canvas.create_rectangle(49, 30, 51, 35 + length, fill=colour, outline=colour)

        if HAIRPARTITION in self.chars:
            self.canvas.create_arc(10, 10, 50, 50, start=10, style='arc', extent=70, outline=colour, width=7)
            self.canvas.create_arc(10, 10, 50, 50, start=90, style='arc', extent=70, outline=colour, width=7)

        x1 = 20
        y1 = 35
        x2 = x1 + 20

        if MOUSTACHE in self.chars:
            self.canvas.create_rectangle(x1, y1, x2, y1, fill=colour, outline=colour)
        if BEARD in self.chars:
            x3 = 10
            y3 = 50
            self.canvas.create_arc(x3, x3, y3, y3, start=-30, style='arc', extent=-120, outline=colour, width=4)
        if EYEBROWS in self.chars:
            x1 = 18
            y1 = 17
            x2 = x1 + 10
            self.canvas.create_rectangle(x1, y1, x2, y1 + 2, fill=colour, outline='black')
            x1 += 15
            x2 += 15
            self.canvas.create_rectangle(x1, y1, x2, y1 + 2, fill=colour, outline='black')

    def draw_ears(self) -> None:
        """Draws the ears of the face."""
        if SMALLEARS in self.chars:
            rad = 2
        else:
            rad = 4

        x1 = 10
        y1 = 30
        x2 = x1 + 40

        create_circle(x1, y1, rad, self.canvas, 'yellow', 'black')
        create_circle(x2, y1, rad, self.canvas, 'yellow', 'black')

    def draw_nose(self) -> None:
        """Draws the nose of the face."""
        if BIGNOSE in self.chars:
            rad = 14
        else:
            rad = 8

        x = 30
        y = 25
        self.canvas.create_polygon(x, y, x, y + 10, x + rad, y + 10, fill='orange')

    def draw_accessory(self) -> None:
        """Draws the accessory of the face."""
        if HAT in self.chars:
            x1 = 10
            y1 = 10
            x2 = x1 + 40
            y2 = y1 + 5

            self.canvas.create_rectangle(x1, y1, x2, y2, fill='brown', outline='black')
            self.canvas.create_rectangle(x1 + 10, 0, x2 - 10, y1, fill='brown', outline='black')
        if GLASSES in self.chars:
            x1 = 20
            y1 = 20
            x2 = x1 + 10
            y2 = y1 + 5
            dx = 10
            self.canvas.create_rectangle(x1, y1, x2, y2, outline='black')
            self.canvas.create_rectangle(x1 + dx, y1, x2 + dx, y2, outline='black')

            y1 = 23
            self.canvas.create_line(x1, y1, x1 - 10, y1, width=2)
            x2 += dx
            self.canvas.create_line(x2, y1, x2 + 10, y1, width=2)
        # REd cheesk
        if REDCHEEKS in self.chars:
            create_circle(20, 30, 3, self.canvas, 'red', 'red')
            create_circle(40, 30, 3, self.canvas, 'red', 'red')

        if EARRING in self.chars:
            create_circle(10, 33, 3, self.canvas, 'green', 'black')
            create_circle(50, 33, 3, self.canvas, 'green', 'black')

    def draw_mouth(self) -> None:
        """Draws the mouth of the face."""
        if SMALLMOUTH in self.chars:
            x1, y1, x2, y2 = 28, 37, 33, 42
        elif BIGMOUTH in self.chars:
            x1, y1, x2, y2 = 25, 32, 37, 43
        else:
            x1, y1, x2, y2 = 25, 35, 37, 43
        self.canvas.create_arc((x1, y1, x2, y2), start=0, extent=-180, fill='black', style='chord')

    def cover(self) -> None:
        """Covers the canvas as the character's attribute has already been guessed."""
        self.canvas.delete('all')
        self.rect = self.canvas.create_rectangle(5, 5, 58, 58, fill='gray', outline='light gray')
        self.canvas.create_arc(20, 20, 40, 40, start=-90, extent=270, width=3, style='arc')
        self.canvas.create_line(30, 45, 30, 40, width=3)
        self.canvas.create_oval(28, 48, 32, 52, fill='black')
        unbind_hovering(self)
        clear_selection()

    def characteristics_to_text_box(self) -> None:
        """Converts the current Face's characteriscs to text and put them in text box"""
        text_box.config(state=NORMAL)
        text_box.delete('1.0', END)
        text_so_far = f"{self.person.name} has the\nfollowing \ncharacteristics:\n\n"
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

        text_box.insert('1.0', text_so_far)
        text_box.config(state=DISABLED)


def name_to_face(name: str) -> Face:
    """Returns the corresponding face to the name"""
    return [face.copy() for face in game_features['faces'] if face.person.name == name][0]


def lock(event, face: Face) -> None:
    """Keeps the current face as a selection."""

    game_features['guess'] = face.person.name

    guess_frame_objects['label'].config(text=face.person.name)
    guess_frame_objects['guessbutton'].config(state=NORMAL)


def hover(event, face: Face) -> None:
    """Changes the face object to a hover state"""
    if face.can_hover:
        face.canvas.itemconfig(face.rect, fill='red')
        face_2 = face.copy()
        face_2.canvas = profile_canvas
        face_2.draw_face()
        text_box.delete('1.0', END)
        face.characteristics_to_text_box()


def unhover(event, face: Face) -> None:
    """Changes the face object to it original state"""
    global text_box
    global profile_canvas

    if face.can_hover:
        face.canvas.itemconfig(face.rect, fill='gray')
        profile_canvas.delete('all')
        profile_canvas.create_rectangle(0, 0, 60, 65, fill='gray')
        text_box.config(state=NORMAL)
        text_box.delete('1.0', END)
        text_box.config(state=DISABLED)


def bind_hovering(face: Face) -> None:
    """Binds the hovering and unhovering events to when the mouse enter/leaves the object."""
    face.canvas.bind("<Enter>", lambda event, f=face: hover(event, f))
    face.canvas.bind("<Leave>", lambda event, f=face: unhover(event, f))

    face.canvas.bind("<Button-1>", lambda event, f=face: lock(event, f))


def unbind_hovering(face: Face) -> None:
    """Unbinds the hvoereing mechanic of the face"""
    face.canvas.unbind('<Enter>')
    face.canvas.unbind('<Leave>')
    face.canvas.unbind('<Button-1>')

def person_to_face(person: Person, game_frame: LabelFrame, curr_row: int, curr_col: int) -> Face:
    """Converts a Person to a Face."""
    face = Face(person, game_frame, curr_col, curr_row)
    return face


def persons_to_faces(persons: list[Person], game_frame: LabelFrame) -> list[Face]:
    """Converts the person dataclasses to Face classes."""
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


def create_faces() -> None:
    """Create Face classes and draw them into game_frame."""
    global game_features

    main_menu_labelframe = LabelFrame(
        frame,
        text="FACES",
        font=('Helvetica', 16, 'bold')
    )
    main_menu_labelframe.grid(row=0, column=2, columnspan=3, padx=5, pady=10)

    persons = load_persons('data/characteristics.csv')
    assert len(persons) == 24

    faces = persons_to_faces(persons, main_menu_labelframe)
    game_features['faces'] = faces
    for face in faces:
        face.draw_face()


def clear_frame() -> None:
    """Clears the frame.

    Preconditions:
    - len(frame.winfo_children()) >= 1
    """
    for widgets in frame.winfo_children():
        widgets.destroy()
    frame.grid_propagate(False)


def create_exit() -> None:
    """Creates the exit button for the main game board"""
    exit_button = Button(
        frame,
        text="Exit",
        width=10,
        command=exit,
        bg='red'
    )
    exit_button.grid(row=2, column=0, pady=10)


def question_to_feature(feature: str) -> str:
    """Converts the question to the necessary constant"""
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


def convert_feature_to_text(feature: str) -> str:
    """Converts the given feature to text"""
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


def create_question_frame() -> None:
    """Creates the place to make a final guess."""
    global question_frame_objects
    buttons = []
    question_frame_objects['frame'] = LabelFrame(frame, text="Question Maker", font='Helvetica 16 bold',
                                                 width=600, height=200)
    question_frame = question_frame_objects['frame']
    curr_feature = 0
    for i in range(3):
        for j in range(6):
            button = Button(question_frame, text=convert_feature_to_text(characteriscs[curr_feature]),
                            font='Helvetica 8', width=10)
            button.grid(row=i, column=j, padx=5)
            buttons.append(button)
            curr_feature += 1
    for k in range(1, 5):
        button = Button(question_frame, text=convert_feature_to_text(characteriscs[curr_feature]),
                        font='Helvetica 8', width=10)
        button.grid(row=3, column=k, padx=5)
        curr_feature += 1
        buttons.append(button)

    question_frame_objects['clearbutton'] = Button(question_frame, text="Clear Question", command=clear_question)
    question_frame_objects['label'] = Label(question_frame, text="Please Select One", font='Helvetica 8 bold')
    question_frame_objects['questionbutton'] = Button(question_frame, text="Ask Question", state=DISABLED)

    question_frame_objects['clearbutton'].grid(row=2, column=6, padx=5, pady=5)
    question_frame_objects['label'].grid(row=0, column=6, padx=10, pady=5)
    question_frame_objects['questionbutton'].grid(row=1, column=6, padx=10, pady=5)
    question_frame_objects['buttons'] = buttons
    question_frame.grid(row=1, column=3, columnspan=3, rowspan=2, padx=0, pady=5)
    question_frame.grid_propagate(0)


def create_guess_frame() -> None:
    """Creates the place to make a final guess."""
    global guess_frame_objects

    guess_frame_objects['frame'] = LabelFrame(frame, text="Guess", font='Helvetica 16 bold')
    guess_frame = guess_frame_objects['frame']

    guess_frame_objects['label'] = Label(guess_frame, text="Select a face", font='Helvetica 10 bold')

    guess_frame_objects['guessbutton'] = Button(guess_frame, text="Make Guess", state=DISABLED)
    guess_frame_objects['clearbutton'] = Button(guess_frame, text="Clear Selection", command=clear_selection)

    guess_frame_objects['label'].pack(padx=10, pady=5)
    guess_frame_objects['guessbutton'].pack(side=LEFT, padx=5, pady=5)
    guess_frame_objects['clearbutton'].pack(side=RIGHT, padx=5, pady=5)

    guess_frame_objects['frame'].grid(row=1, column=0, columnspan=2, padx=0, pady=10)


def create_profiler() -> None:
    """Creates the profile labelframe and canvas."""
    global profile_canvas
    global text_box
    global game_features

    profile_frame = LabelFrame(frame, text="Profiler", font='Helvetica 16 bold')

    spy_label = Label(profile_frame, text="Your Spy:", font='Helvetica 10 bold')
    spy_label.grid(row=0, column=0)

    spy_canvas = Canvas(profile_frame, width=55, height=60, borderwidth=2, relief='solid')
    spy_canvas.create_rectangle(0, 0, 60, 65, fill='gray')
    spy_canvas.grid(row=1, column=0, padx=5, pady=10)
    game_features['spycanvas'] = spy_canvas

    profile_canvas = Canvas(profile_frame, width=55, height=60, borderwidth=2, relief="solid")
    profile_canvas.create_rectangle(0, 0, 60, 65, fill='gray')
    profile_canvas.grid(row=1, column=1, padx=5, pady=10)

    text_box = Text(profile_frame, width=20, height=12, state='disabled')
    text_box.grid(row=2, column=0, columnspan=2, padx=10, pady=14)

    profile_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10)


def clear_conversation() -> None:
    """Clears the conversation in the conversation text box"""
    conversation_frame_objects['box'].delete('1.0', END)


def clear_chat() -> None:
    """Clears the conversation text box"""
    conversation_frame_objects['box'].config(state=NORMAL)
    conversation_frame_objects['box'].delete('1.0', END)
    conversation_frame_objects['box'].config(state=DISABLED)


def insert_conversation(text: str) -> None:
    """Insert a conversation into the text box"""

    text += '\n'
    conversation_frame_objects['box'].config(state=NORMAL)
    conversation_frame_objects['box'].insert(END, text)
    conversation_frame_objects['box'].config(state=DISABLED)


def create_conversation() -> None:
    """Creates the computer conversation on the side of the board."""
    global conversation_frame_objects

    conversation_frame_objects['frame'] = LabelFrame(frame, text='Computer Says', font='Helvetica 16 bold')
    conversation_frame_objects['box'] = Text(conversation_frame_objects['frame'], width=20, height=20, state='disabled',
                                             font='Helvetica 8')
    # conversation_frame_objects['bar'] = tkinter.ttk.Progressbar(conversation_frame_objects['frame'],
    #                                                             mode='indeterminate')

    conversation_frame_objects['frame'].grid(row=0, column=5, padx=5)
    conversation_frame_objects['box'].grid(row=0, column=0, padx=10, pady=10)
    # conversation_frame_objects['bar'].grid(row=1, column=0)


def create_menu_button() -> None:
    """Creates the button that will take the player back to main menu."""
    game_features['menu'] = Button(frame, text='Menu', width=10)
    game_features['menu'].grid(row=2, column=1, padx=10, pady=10)


def summon_main_board() -> None:
    """Summons the main board of the GUI."""

    clear_frame()


    create_menu_button()
    create_faces()
    create_guess_frame()
    create_conversation()
    create_exit()
    create_profiler()
    create_question_frame()


def back_to_menu() -> None:
    """Returns the board to the main menu."""
    clear_frame()
    summon_main_menu()


def summon_main_menu() -> None:
    """Creates the main menu LabelFrame and all the buttons options.
    for the given player."""
    global game_features

    clear_frame()

    main_frame = LabelFrame(
        frame,
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
    players = ['GreedyPlayer', 'RandomPlayer', 'PoorPlayer']

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
    for i in range(1, 3):
        player_buttons[i].pack(pady=5)
    game_features['pb'] = player_buttons
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
    window = Tk()

    frame = Frame(window, width=800, height=600)
    frame.pack(side="top", expand=True, fill="both")
    frame.pack_propagate(False)

    summon_main_menu()
    window.mainloop()
