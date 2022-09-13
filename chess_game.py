import random
from itertools import product
import logging


from utils.utils import fill_board
from utils.board import BOARD_LETTERS


logging.basicConfig(format='%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    level=logging.DEBUG,
                    handlers=[logging.FileHandler("logs_chess.log"), logging.StreamHandler()]
                    )

# Generate random positions for all chess pieces
random.seed(1)
random_position = random.sample(list(product(list(range(8)), BOARD_LETTERS)), 32)


board, pieces = fill_board(random_position)
p1 = pieces[22]
print(p1)
print(p1.get_position())
try:
    print(f"Piece: {p1.__class__.__name__} {p1.colour}, at position: {p1.get_position()}")
    print("Allowed to move: ", p1.step((6, "d"), board))
except Exception as e:
    logging.error(f"Unhandled exception {e}")
