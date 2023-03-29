"""CSC111 Winter 2023 Project: Guess Who Artifical Intelligence
This module contains the classes and necessary functions to execute
the frontend of the classic game "Guess Who".
"""
from __future__ import annotations

from typing import Optional

from tkinter import *

from guess_who import *
from features import *


cells = [[''] * 6] * 4


class Face:
    """Responsible for being the canvas of the face of a person.

    Instance Attributes:

    """
    def __init__(self, name: str, game_frame: LabelFrame, col: int, row: int,
                 characteristics: Optional[list[str]] = None):
        self.name = name
        self.canvas = Canvas(
            game_frame,
            width=60, height=60,
            bg="light gray",
        )
        self.col = col
        self.row = row
        self.characteristics = characteristics

    def draw_face(self) -> None:
        """Draws an individual face."""

        self.canvas.grid(row=self.row, column=self.col)
        create_circle(30, 28, 20, self.canvas, 'yellow', 'black')

        if self.characteristics is not None:
            self.draw_eyes()
        #     self.draw_hair()
        #     self.draw_facial_hair()
        #     self.draw_ears()
            self.draw_nose()
        #     self.draw_accessory()
            self.draw_mouth()

    def draw_eyes(self) -> None:
        """Draws the eyes of the Face."""
        create_circle(25, 20, 2, self.canvas, 'black', 'black')
        create_circle(35, 20, 2, self.canvas, 'black', 'black')

    def draw_hair(self) -> None:
        """Draws the hair of the Face."""
        pass


    def draw_facial_hair(self) -> None:
        pass

    def draw_ears(self) -> None:
        pass

    def draw_nose(self) -> None:
        """Draws the nose of the face."""
        if self.characteristics[4] == BIGNOSE:
            rad = 4
        else:
            rad = 2
        create_circle(30, 30, rad, self.canvas, 'orange', 'orange')

    def draw_accessory(self) -> None:
        pass

    def draw_mouth(self) -> None:
        """Draws the mouth of the Face."""
        if self.characteristics[-1] == SMALLMOUTH:
            x1, y1, x2, y2 = 27, 28, 33, 38
        elif self.characteristics[-1] == MEDIUMMOUTH:
            x1, y1, x2, y2 = 23, 28, 37, 38
        else:
            x1, y1, x2, y2 = 20, 28, 40, 43
        self.canvas.create_arc((x1, y1, x2, y2), start=-30, extent=-120, fill='black', style=tk.CHORD)


window = Tk()

frame = Frame(window, width=700, height=350)
frame.pack(side="top", expand=False, fill="both")
frame.pack_propagate(0)


def characteristics_to_list(person: Person) -> list[str]:
    """Converts a person class to a list of characteristics."""
    return [person.ear_size, person.hair_style, person.hair_length, person.hair_colour, person.nose_size,
            person.facial_hair, person.accessory, person.mouth_size]


def person_to_face(person: Person, game_frame: LabelFrame, curr_row: int, curr_col: int) -> Face:
    """Converts a Person to a Face."""
    if not person.up:
        face = Face(person.name, game_frame, curr_col, curr_row)
    else:
        face = Face(person.name, game_frame, curr_col, curr_row, characteristics_to_list(person))
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



def clear_menu():
    for widgets in frame.winfo_children():
        widgets.destroy()


def summon_main_menu():
    main_menu_label = LabelFrame(
        frame,
        text="FACES",
        font=('Helvetica', 16, 'bold')
    )
    main_menu_label.pack(padx=5, pady=20)

    persons = load_persons('characteristics.csv')
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


def back_to_menu():
    clear_menu()
    summon_main_menu()


def summon_main_board():
    game_frame = LabelFrame(
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

    game_frame.pack(pady=8)
    exit_button.pack()
    print_faces(game_frame)


def print_faces(game_frame):
    pass

def create_circle(x, y, r, canvas, colour, outline_colour):
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
        width=2,
        outline=outline_colour
    )


if __name__ == "__main__":
    summon_main_menu()
    window.mainloop()
