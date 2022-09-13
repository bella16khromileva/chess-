from abc import ABC
from typing import Callable
import logging
from functools import wraps
import time

from utils.board import BOARD_LETTERS, BOARD_NUMBERS


logging.basicConfig(format='%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    level=logging.DEBUG,
                    handlers=[logging.FileHandler("logs_chess.log"), logging.StreamHandler()]
                    )


def convert_position(position: tuple[int, str]) -> tuple[int, str]:
    """
    Converts the position from the user input to the coordinates that the function step() uses.
    """
    return position[0] - 1, position[1]


def timeit(func: Callable) -> Callable:
    """
    Calculates the execution time of other functions.
    """
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        logging.info(f'Function {func.__name__} Took {total_time:.6f} seconds')
        return result
    return timeit_wrapper


class Figure(ABC):
    def __init__(self, colour: str, figure_id: int, position: tuple[int, str]):
        self.colour = colour
        self.figure_id = figure_id
        self.position = position

    def get_position(self):
        """
        Shows the position of the piece on the board.
        """
        return self.position[0] + 1, self.position[1]

    @timeit
    def possible_move(self, target_position: tuple[int, str], board: dict[str, list]) -> bool:

        if target_position[0] not in BOARD_NUMBERS or target_position[1] not in BOARD_LETTERS:
            logging.info('Target position is out of the board')
            return False

        if self.position[0] == target_position[0] and self.position[1] == target_position[1]:
            logging.info('Piece cannot move to the same spot')
            return False

        figure_at_position = board[target_position[1]][target_position[0]]
        if figure_at_position is not None:
            if figure_at_position.colour == self.colour:
                logging.info('Piece cannot take its own pieces')
                return False

        return True

    def step(self, position: tuple[int, str], board: dict[str, list]) -> bool:
        raise NotImplementedError

    @timeit
    def figures_on_the_way_diagonally(self, current_position: tuple[int, str],
                                      target_position: tuple[int, str], board: dict[str, list]) -> bool:
        """
        Checks if there are pieces on the way diagonally l(for Bishop and Queen).
        """
        idx_cur = BOARD_LETTERS.index(current_position[1])
        idx_tar = BOARD_LETTERS.index(target_position[1])
        if abs(target_position[0] - current_position[0]) > 1 and abs(idx_tar - idx_cur) > 1:

            if target_position[0] > current_position[0] and idx_tar > idx_cur:
                digits = list(range(current_position[0] + 1, target_position[0]))
                letters_id = list(range(idx_cur + 1, idx_tar))
                letters = BOARD_LETTERS[letters_id[0]:]
                if len([1 for coord in list(zip(digits, letters)) if board[coord[1]][coord[0]] is not None]) != 0:
                    logging.info('Some figures on the way up to the right')
                    return False

            elif target_position[0] < current_position[0] and idx_tar > idx_cur:
                digits = list(range(current_position[0] - 1, target_position[0], -1))
                letters_id = list(range(idx_cur + 1, idx_tar))
                letters = BOARD_LETTERS[letters_id[0]:]
                if len([1 for coord in list(zip(digits, letters)) if board[coord[1]][coord[0]] is not None]) != 0:
                    logging.info('Some figures on the way down to the right')
                    return False

            elif target_position[0] > current_position[0] and idx_tar < idx_cur:
                digits = list(range(current_position[0] + 1, target_position[0]))
                letters_id = list(range(idx_cur - 1, idx_tar, -1))
                letters = BOARD_LETTERS[letters_id[0]:]
                if len([1 for coord in list(zip(digits, letters)) if board[coord[1]][coord[0]] is not None]) != 0:
                    logging.info('Some figures on the way up to the left')
                    return False

            elif target_position[0] < current_position[0] and idx_tar < idx_cur:
                digits = list(range(current_position[0] - 1, target_position[0], -1))
                letters_id = list(range(idx_cur - 1, idx_tar, -1))
                letters = BOARD_LETTERS[letters_id[0]:]
                if len([1 for coord in list(zip(digits, letters)) if board[coord[1]][coord[0]] is not None]) != 0:
                    logging.info('Some figures on the way down to the left')
                    return False

        return True

    @timeit
    def figures_on_the_straight_way(self, current_position: tuple[int, str],
                                    target_position: tuple[int, str], board: dict[str, list]) -> bool:
        """
        Checks if there are pieces on the straight way (for Rook and Queen).
        """

        idx_cur = BOARD_LETTERS.index(current_position[1])
        idx_tar = BOARD_LETTERS.index(target_position[1])

        if target_position[0] == current_position[0]:
            figure_path = [(target_position[0], x)
                           for x in BOARD_LETTERS[min(idx_cur, idx_tar) + 1: max(idx_cur, idx_tar) - 1]]

            if len([1 for coord in figure_path if board[coord[1]][coord[0]] is not None]) != 0:
                logging.info('Some figures on the straight way')
                return False

        if target_position[1] == current_position[1]:
            figure_path = [(x, target_position[1]) for x in list(
                range(min(target_position[0], current_position[0]),
                      max(target_position[0], current_position[0])))]

            if len([1 for coord in figure_path if board[coord[1]][coord[0]] is not None]) != 0:
                logging.info('Some figures on the straight way')
                return False

        return True


class Pawn(Figure):
    @timeit
    def step(self, target_position: tuple[int, str], board: dict[str, list]) -> bool:
        target_position = convert_position(target_position)
        if not self.possible_move(target_position, board):
            return False

        current_position = self.position
        figure_at_position = board[target_position[1]][target_position[0]]
        idx_cur = BOARD_LETTERS.index(current_position[1])
        idx_tar = BOARD_LETTERS.index(target_position[1])
        move_straight = abs(target_position[0] - current_position[0])
        move_diagonal = abs(idx_tar - idx_cur)

        if move_straight != 1 or move_diagonal > 1:
            logging.info("Pawn can only move straight or diagonally by one square (or two if it is first move)."
                         " Let's assume that this is not the first move")
            return False

        if idx_cur != idx_tar:
            if figure_at_position is None:
                logging.info("Pawns cannot move diagonally into an empty square")
                return False
        else:
            if figure_at_position is not None:
                logging.info("Pawns cannot take pieces in front of them")
                return False

        if self.colour == "white":
            if target_position[0] < current_position[0]:
                logging.info("White Pawns cannot move down")
                return False

        if self.colour == "black":
            if target_position[0] > current_position[0]:
                logging.info("Black Pawns cannot move up")
                return False

        return True


class Rook(Figure):
    @timeit
    def step(self, target_position: tuple[int, str], board: dict[str, list]) -> bool:
        target_position = convert_position(target_position)
        if not self.possible_move(target_position, board):
            return False
        current_position = self.position
        # Checks if it is a horizontal or vertical move.
        if target_position[0] != current_position[0] and target_position[1] != current_position[1]:
            print('Rook can only make a move to a cell that is in the same row or column')
            return False
        idx_cur = BOARD_LETTERS.index(current_position[1])
        idx_tar = BOARD_LETTERS.index(target_position[1])

        # Checks if move is greater than 1.
        if abs(target_position[0] - current_position[0]) > 1 or abs(idx_tar - idx_cur) > 1:

            if not self.figures_on_the_straight_way(current_position, target_position, board):
                return False

        return True


class Knight(Figure):
    @timeit
    def step(self, target_position: tuple[int, str], board: dict[str, list]) -> bool:
        target_position = convert_position(target_position)
        if not self.possible_move(target_position, board):
            return False
        current_position = self.position
        idx_cur = BOARD_LETTERS.index(current_position[1])
        idx_tar = BOARD_LETTERS.index(target_position[1])
        one_move = min(abs(target_position[0] - current_position[0]), abs(idx_tar - idx_cur))
        two_move = max(abs(target_position[0] - current_position[0]), abs(idx_tar - idx_cur))
        if one_move != 1 or two_move != 2:
            logging.info('Knight can only move in an L shape')
            return False

        return True


class King(Figure):
    @timeit
    def step(self, target_position: tuple[int, str], board: dict[str, list]) -> bool:
        target_position = convert_position(target_position)
        if not self.possible_move(target_position, board):
            return False
        current_position = self.position
        idx_cur = BOARD_LETTERS.index(current_position[1])
        idx_tar = BOARD_LETTERS.index(target_position[1])
        # Checks if move is greater than 1.
        if abs(target_position[0] - current_position[0]) > 1 or abs(idx_tar - idx_cur) > 1:
            logging.info('Kings can only move one square in any direction')
            return False

        return True


class Bishop(Figure):
    @timeit
    def step(self, target_position: tuple[int, str], board: dict[str, list]) -> bool:
        target_position = convert_position(target_position)
        if not self.possible_move(target_position, board):
            return False
        current_position = self.position
        idx_cur = BOARD_LETTERS.index(current_position[1])
        idx_tar = BOARD_LETTERS.index(target_position[1])
        # Checks if it is a diagonal move.
        if abs(target_position[0] - current_position[0]) != abs(idx_tar - idx_cur):
            logging.info('Bishop can only move diagonally')
            return False

        if not self.figures_on_the_way_diagonally(current_position, target_position, board):
            return False

        return True


class Queen(Figure):
    @timeit
    def step(self, target_position: tuple[int, str], board: dict[str, list]) -> bool:
        target_position = convert_position(target_position)
        if not self.possible_move(target_position, board):
            return False
        current_position = self.position
        idx_cur = BOARD_LETTERS.index(current_position[1])
        idx_tar = BOARD_LETTERS.index(target_position[1])

        # Checks if it is a diagonal move.
        if abs(target_position[0] - current_position[0]) == abs(idx_tar - idx_cur):
            # Checks if move is greater than 1.
            if abs(target_position[0] - current_position[0]) > 1 or abs(idx_tar - idx_cur) > 1:
                if not self.figures_on_the_way_diagonally(current_position, target_position, board):
                    return False
        # Checks if it is a horizontal or vertical move.
        elif (target_position[0] == current_position[0]) or (target_position[1] == current_position[1]):
            # Checks if move is greater than 1.
            if abs(target_position[0] - current_position[0]) > 1 or abs(idx_tar - idx_cur) > 1:
                if not self.figures_on_the_straight_way(current_position, target_position, board):
                    return False
        else:
            logging.info('Queen can move diagonally, horizontally or vertically to any number of cells')
            return False

        return True
