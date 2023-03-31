"""CSC111 Winter 2023 Project: Guess Who Artifical Intelligence
This module contains the classes and necessary functions to execute
the frontend of the classic game "Guess Who".
"""
from __future__ import annotations

from typing import Optional

from tkinter import *

from guess_who import *
from features import *


########################################################################################################################


class Face:
    """Responsible for being the canvas of the face of a person.

    Instance Attributes:

    """
    def __init__(self, person: Person, game_frame: LabelFrame, col: int, row: int,
                 x: Optional[int] = 0, y: Optional[int] = 0):
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
        bind_hovering(self)
        self.x = x
        self.y = y

    def draw_face(self) -> None:
        """Draws an individual face."""

        self.canvas.grid(row=self.row, column=self.col)
        create_circle(self.x + 30, self.y + 30, 20, self.canvas, 'yellow', 'black')

        if self.person.up:
            self.draw_eyes()
            self.draw_hair()
            self.draw_facial_hair()
            self.draw_ears()
            self.draw_nose()
            self.draw_accessory()
            self.draw_mouth()
            self.canvas.create_text(30, 53, text=self.person.name, fill="white", font=('Helvetica 7 bold'))

    def draw_eyes(self) -> None:
        """Draws the eyes of the Face."""
        x1 = self.x + 25
        x2 = x1 + 10
        y = self.y + 20
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

        self.canvas.create_arc(10, 10, 50, 50, start=0, extent=180, width=5, style='arc', fill=colour, outline=colour)

        if CURLYHAIR in self.chars:
            for i in range(1, 4):
                create_circle(11, 24 + i * 6, 3, self.canvas, colour, colour)
                create_circle(50, 24 + i * 6, 3, self.canvas, colour, colour)
        else:
            self.canvas.create_rectangle(9, 30, 11, 35 + length, fill=colour, outline=colour)
            self.canvas.create_rectangle(49, 30, 51, 35 + length, fill=colour, outline=colour)

        if HAIRPARTITION in self.chars:
            # TODO: Create polygons
            pass

        # else:  # TODO: Determine if wavy hair is part of it
        #     x1, y1, x2, y2 = 6, 27, 10, 30
        #     x1 += self.x
        #     x2 += self.x
        #     y1 += self.y
        #     y2 += self.y
        #
        #     for _ in range(length):
        #         self.canvas.create_rectangle(x1, y1, x2, y2, fill=colour, outline=colour)
        #         self.canvas.create_rectangle(x1 + 3, y1 + 3, x2 + 3, y2 + 3, fill=colour, outline=colour)
        #
        #         self.canvas.create_rectangle(x1 + 40, y1, x2 + 40, y2, fill=colour, outline=colour)
        #         self.canvas.create_rectangle(x1 + 43, y1 + 3, x2 + 43, y2 + 3, fill=colour, outline=colour)
        #
        #         y1 += 5
        #         y2 += 5

    def draw_facial_hair(self) -> None:
        """Draws the facial hair of the person."""
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

        x1 = 20 + self.x
        y1 = 35 + self.y
        x2 = x1 + 20
        y2 = y1 + 12

        if MOUSTACHE in self.chars:
            self.canvas.create_rectangle(x1, y1, x2, y1, fill=colour, outline=colour)
        if BEARD in self.chars:
            x3 = self.x + 10
            y3 = self.y + 50
            self.canvas.create_arc(x3, x3, y3, y3, start=-30, style='arc', extent=-120, outline=colour, width=4)
        # if style == FULLBEARD:
        #     self.canvas.create_rectangle(x1, y1, x1 + 2, y2, fill=colour, outline=colour)
        #     self.canvas.create_rectangle(x2, y1, x2 + 2, y2, fill=colour, outline=colour)

    def draw_ears(self) -> None:
        """Draws the ears of the face."""
        if BIGEARS in self.chars:
            rad = 2
        else:
            rad = 4

        x1 = 10 + self.x
        y1 = 30 + self.y
        x2 = x1 + 40

        create_circle(x1, y1, rad, self.canvas, 'yellow', 'black')
        create_circle(x2, y1, rad, self.canvas, 'yellow', 'black')

    def draw_nose(self) -> None:
        """Draws the nose of the face."""
        if BIGNOSE in self.chars:
            rad = 14
        else:
            rad = 8

        x = self.x + 30
        y = self.y + 25
        self.canvas.create_polygon(x, y, x, y + 10, x + rad, y + 10, fill='orange')

    def draw_accessory(self) -> None:
        """Draws the accessory of the face."""
        if HAT in self.chars:
            x1 = 10 + self.x
            y1 = 10 + self.y
            x2 = x1 + 40
            y2 = y1 + 5

            self.canvas.create_rectangle(x1, y1, x2, y2, fill='brown', outline='black')
            self.canvas.create_rectangle(x1 + 10, 0, x2 - 10, y1, fill='brown', outline='black')
        # TODO: The rest


    def draw_mouth(self) -> None:
        """Draws the mouth of the face."""
        if SMALLMOUTH in self.chars:
            x1, y1, x2, y2 = 28, 37, 33, 42
        elif BIGMOUTH in self.chars:
            x1, y1, x2, y2 = 25, 32, 37, 43
        else:
            x1, y1, x2, y2 = 25, 35, 37, 43
        self.canvas.create_arc((x1, y1, x2, y2), start=0, extent=-180, fill='black', style=tk.CHORD)


def hover(event, face: Face):
    face.canvas.itemconfig(face.rect, fill='red')

def unhover(event, face: Face):
    face.canvas.itemconfig(face.rect, fill='gray')

def bind_hovering(face: Face) -> None:
    face.canvas.bind("<Enter>", lambda event, f=face: hover(event, f))
    face.canvas.bind("<Leave>", lambda event, f=face: unhover(event, f))

    face.canvas.tag_bind(face.rect, "<Button-1>", clear_menu)


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




def create_faces(persons: list[Person], game_frame: LabelFrame) -> None:
    """Create Face classes and draw them into game_frame."""
    pass


def clear_menu() -> None:
    """Clears the frame.

    Preconditions:
    - len(frame.winfo_children()) >= 1
    """
    for widgets in frame.winfo_children():
        widgets.destroy()


def summon_main_menu() -> None:
    """Summons the main menu of the GUI."""
    main_menu_label = LabelFrame(
        frame,
        text="FACES",
        font=('Helvetica', 16, 'bold')
    )
    main_menu_label.pack(padx=5, pady=20)

    persons = load_persons('data/characteristics.csv')
    assert len(persons) == 24

    faces = persons_to_faces(persons, main_menu_label)
    for face in faces:
        face.draw_face()

    # two_player_button = Button(
    #     frame,
    #     text="Player vs another player",
    #     width=20,
    #     height=5,
    #     command=lambda m=0: [clear_menu(), summon_main_board()]
    # )

    # computer_enemy = Button(
    #     frame,
    #     text="Play vs computer",
    #     width=20,
    #     height=5,
    #     command=play_vs_computer
    # )

    exit_button = Button(
        frame,
        text="Exit",
        width=20,
        command=exit,
        bg='red'
    )
    # two_player_button.pack(padx=5, pady=7)
    # computer_enemy.pack(padx=5, pady=7)
    exit_button.pack(pady=14)


def back_to_menu() -> None:
    """Returns the board to the main menu."""
    clear_menu()
    summon_main_menu()


def summon_main_board(player: Optional[Player] = None) -> None:
    """Creates the main LabelFrame containing faces (face_frame), the necessary buttons to make question, etc.
    for the given player."""
    face_frame = LabelFrame(
        frame,
        height=300,
        width=400
    )

    exit_button = Button(
        frame,
        text="Exit",
        width=20,
        command=exit,
        bg='red'
    )

    face_frame.pack(pady=8)
    exit_button.pack()
    print_faces(face_frame)


def print_faces(game_frame):
    pass


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


window = Tk()

frame = Frame(window, width=700, height=350)
frame.pack(side="top", expand=False, fill="both")
frame.pack_propagate(0)


if __name__ == "__main__":
    summon_main_menu()
    window.mainloop()
