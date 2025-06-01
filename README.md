# Gomoku Game♟️

Welcome to Gomoku, also known as Five in a Row! This is a classic strategy board game where the goal is to be the first player to get an unbroken row of five of their pieces horizontally, vertically, or diagonally.

This implementation features a graphical user interface (GUI) and several game modes, including Player vs Player, Player vs AI, and a demonstration of AI vs AI using different algorithms.

---

## Features ✨

* **Graphical User Interface (GUI):** A user-friendly interface built with Pygame.
* **Player vs Player (PvP):** Play against a friend on the same computer.
* **Player vs AI (PvAI):** Test your skills against an AI opponent that uses the **Alpha-Beta Pruning** algorithm.
* **AI vs AI (AIvAI):** Watch two AIs battle it out! This mode showcases:
    * **Minimax Algorithm**
    * **Alpha-Beta Pruning Algorithm**

---

## Prerequisites 🛠️

Before you can run the game, you need to have **Python** installed on your system.

Additionally, this game uses the **Pygame** library for its graphics and event handling.

---

## Installation ⚙️

1.  **Ensure Python is installed:** If you don't have Python, download and install it from [python.org](https://www.python.org/downloads/).

2.  **Install Pygame:** Open your terminal or command prompt and run the following command:
    ```bash
    pip install pygame
    ```

---

## How to Run the Game ▶️

1.  **Download or clone the game files** to your local machine.
2.  **Navigate to the game's directory** in your terminal or command prompt.
3.  **Run the main Python file** (e.g., `main.py`, `gomoku.py`, or similar – please check the actual filename in the project). Execute the following command, replacing `main.py` with the correct filename if necessary:
    ```bash
    python main.py
    ```
4.  The game window should open, and you can select your desired game mode from the GUI.

---

## How to Play  Gomoku

* The game is played on a grid (typically 15x15).
* Players take turns placing one of their pieces on an empty intersection of the grid.
* The first player to achieve an unbroken line of **five** of their pieces (horizontally, vertically, or diagonally) wins the game.
* If the board is filled and no player has achieved five in a row, the game is a draw (though this is rare in standard Gomoku).

---

Enjoy the game! 🎉
