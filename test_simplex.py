from simplex import Simplex


def test_simplex_resolve():
    simp = Simplex(
        eqs=((15, 7.5, 5), (2, 3, 2), (1, 1, 1)),
        constants=(315, 110, 50),
        max_func=(200, 150, 120),
    )
    assert simp.resolve(show_step=False) == (36.0, 4.0, 10.0)
