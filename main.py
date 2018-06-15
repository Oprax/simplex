from simplex import Simplex


def main():
    simp = Simplex(
        eqs=((15, 7.5, 5), (2, 3, 2), (1, 1, 1)),
        constants=(315, 110, 50),
        max_func=(200, 150, 120),
    )
    r = simp.resolve()
    print("Result is", r)


if __name__ == "__main__":
    main()
