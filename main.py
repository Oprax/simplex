from simplex import Simplex


def main():
    simp = Simplex(
        eqs=((1, 3), (-1, 3), (1, -1)), constants=(21, 18, 5), max_func=(1, 2)
    )
    r = simp.resolve(iter_limit=10)
    print("Result is", r)


if __name__ == "__main__":
    main()
