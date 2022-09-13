def test_step__diagonal_move_to_empty_square(board, pieces):
    assert not pieces[8].step((5, 'f'), board)


def test_step__diagonal_move(board, pieces):
    assert pieces[9].step((3, 'f'), board)


def test_step__is_correct_move(board, pieces):
    assert not pieces[9].step((6, 'e'), board)


def test_step__is_correct_move_straight(board, pieces):
    assert not pieces[10].step((4, 'b'), board)
    assert pieces[29].step((3, 'g'), board)


def test_step__possible_move(board, pieces):
    assert not pieces[8].step((5, 'h'), board)
