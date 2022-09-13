def test_step__horizontal_move(board, pieces):
    assert pieces[0].step((6, 'g'), board)


def test_step__vertical_move(board, pieces):
    assert pieces[0].step((5, 'f'), board)
    assert pieces[16].step((7, 'g'), board)


def test_step__diagonal_move(board, pieces):
    assert pieces[0].step((5, 'e'), board)


def test_step__is_correct_move(board, pieces):
    assert not pieces[0].step((4, 'f'), board)


def test_step__possible_move(board, pieces):
    assert not pieces[0].step((6, 'f'), board)
