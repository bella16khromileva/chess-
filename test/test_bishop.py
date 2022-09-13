def test_step__diagonal_move(board, pieces):
    assert pieces[7].step((8, 'g'), board)


def test_step__is_correct_move(board, pieces):
    assert not pieces[7].step((3, 'd'), board)
    assert not pieces[20].step((8, 'a'), board)


def test_step__figures_on_the_way_down_right(board, pieces):
    assert not pieces[7].step((2, 'g'), board)


def test_step__figures_on_the_way_up_left(board, pieces):
    assert not pieces[7].step((7, 'b'), board)


def test_step__figures_on_the_way_down_left(board, pieces):
    assert pieces[20].step((5, 'a'), board)


def test_step__possible_move(board, pieces):
    assert not pieces[7].step((8, 'a'), board)
