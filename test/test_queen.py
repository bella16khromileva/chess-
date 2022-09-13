def test_step__diagonal_move(board, pieces):
    assert pieces[1].step((5, 'c'), board)


def test_step__figures_on_the_way_up_right(board, pieces):
    assert not pieces[1].step((7, 'g'), board)


def test_step__possible_move(board, pieces):
    assert not pieces[1].step((2, 'f'), board)
    assert not pieces[17].step((1, 'e'), board)


def test_step__is_correct_move(board, pieces):
    assert not pieces[1].step((3, 'g'), board)
    assert pieces[17].step((5, 'c'), board)
