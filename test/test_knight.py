def test_step__knight_move(board, pieces):
    assert pieces[6].step((3, 'h'), board)


def test_step__is_correct_move(board, pieces):
    assert not pieces[6].step((2, 'd'), board)


def test_step__possible_move(board, pieces):
    assert not pieces[6].step((4, 'e'), board)
