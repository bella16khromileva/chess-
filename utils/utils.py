from pieces import Figure, Pawn, Rook, Knight, King, Bishop, Queen
from utils.board import BOARD_LETTERS


def fill_board(positions: list) -> tuple[dict[str, list], list]:
    """
    Places the pieces on the board in randomly generated positions.
    """
    board: dict[str, list[Figure | None]] = {k: [None] * 8 for k in BOARD_LETTERS}
    pieces: list[Figure] = []
    k = 0
    for colour in ["black", "white"]:
        pieces.append(King(colour, 1, positions[k]))
        k += 1
        pieces.append(Queen(colour, 1, positions[k]))
        k += 1

        for n in range(2):
            for piece in [Rook, Knight, Bishop]:
                pieces.append(piece(colour, n, positions[k]))
                k += 1

        for n in range(8):
            pieces.append(Pawn(colour, n, positions[k]))
            k += 1

    for piece in pieces:  # type: ignore
        board[piece.position[1]][piece.position[0]] = piece  # type: ignore

    return board, pieces
