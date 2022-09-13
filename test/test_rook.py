def test_step__vertical_move(board, pieces):
    assert pieces[5].step((7, 'c'), board)


def test_step__horizontal_move(board, pieces):
    assert pieces[5].step((8, 'd'), board)


def test_step__is_correct_move(board, pieces):
    assert not pieces[5].step((6, 'g'), board)


def test_step__figures_on_the_way(board, pieces):
    assert not pieces[5].step((8, 'g'), board)


def test_step__possible_move(board, pieces):
    assert not pieces[5].step((8, 'c'), board)
