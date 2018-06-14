from fractions import Fraction

from tabulate import tabulate


class Simplex(object):
    """
    Class to solve a linear optimization problem using simplex algorithm.
    """
    def __init__(self, eqs=tuple(), constants=tuple(), max_func=tuple()):
        """
        Setup and fill table with information from user.

        :param eqs:
        :param constants:
        :param max_func:

        :Example:
        >>> simp = Simplex(
        ...    eqs=((15, 7.5, 5), (2, 3, 2), (1, 1, 1)),
        ...    constants=(315, 110, 50),
        ...    max_func=(200, 150, 120))
        >>> r = simp.resolve(show_step=False)
        >>> print("Result is", r)
        Result is (4.0, 10.0, 36.0)
        """
        if len(eqs) != len(constants) or len(eqs) == 0:
            raise ValueError("Need same number of constant and equations")
        self._eqs = eqs
        self._constants = constants
        self._max_func = max_func

        self._nb_eq = len(self._eqs)
        self._size_eq = len(self._eqs[0])
        if self._size_eq != len(max_func) or self._size_eq == 0:
            raise ValueError("Each equation must have the same size !")
        for eq in self._eqs:
            if self._size_eq != len(eq):
                raise ValueError("Each equation must have the same size !")

        self._size_cols = self._size_eq + self._nb_eq + 2
        self._size_lines = self._nb_eq + 1

        self.headers = []
        for i in range(self._size_eq):
            self.headers.append(f"x{i+1}")
        for i in range(self._nb_eq):
            self.headers.append(f"e{i+1}")
        self.headers.append("C")
        self.headers.append("R")

        self.line_headers = []
        for i in range(self._size_eq):
            self.line_headers.append(f"e{i+1}")
        self.line_headers.append("F")

        self._table = {}
        for line in range(self._size_lines):
            for col in range(self._size_cols):
                self._table[col, line] = Fraction(0)
        for line, eq in enumerate(self._eqs):
            self._table[self._size_eq + line, line] = 1
            for col, part in enumerate(eq):
                self._table[col, line] = Fraction(part)
        for col, part in enumerate(self._max_func):
            self._table[col, self._size_eq] = Fraction(part)
        for line, part in enumerate(self._constants):
            self._table[self._nb_eq * 2, line] = Fraction(part)

    @property
    def table(self):
        return self._table

    def next_step(self):
        """

        :return:
        """
        col_pivot, line_pivot = self.compute_ratio(col_pivot=self.compute_col_pivot())
        tmp_table = dict(self._table)
        pivot = Fraction(self._table[col_pivot, line_pivot])

        for line in range(self._size_lines):
            for col in range(self._size_cols - 1):
                tmp_table[col, line] = self._table[col, line] - (
                    (self._table[col_pivot, line] * self._table[col, line_pivot]) / pivot
                )

        for line in range(self._size_lines):
            tmp_table[col_pivot, line] = 0
        tmp_table[col_pivot, line_pivot] = 1
        for col in range(self._size_cols - 1):
            if col != col_pivot:
                tmp_table[col, line_pivot] = self._table[col, line_pivot] / pivot
        self._table = dict(tmp_table)

    def extract_max_func(self):
        """

        :return:
        """
        line = self._nb_eq
        max_func = []
        for i in range(self._size_cols - 1):
            max_func.append(self._table[i, line])
        return max_func

    def extract_constants(self):
        """

        :return:
        """
        tmp = []
        for line in range(self._nb_eq):
            tmp.append(float(self._table[self._size_cols - 2, line]))
        return tmp

    def compute_col_pivot(self):
        """

        :return:
        """
        tmp = self.extract_max_func()
        return tmp.index(max(tmp))

    def compute_ratio(self, col_pivot=0):
        """

        :param col_pivot:
        :return:
        """
        tmp = []
        for line in range(self._size_lines - 1):
            ratio = self._table[self._size_cols - 2, line] / self._table[col_pivot, line]
            tmp.append(ratio)
            self._table[self._size_cols - 1, line] = Fraction(ratio)
        return col_pivot, tmp.index(min(tmp))

    def print_table(self, table):
        """

        :param table:
        :return:
        """
        tmp = []
        for line in range(self._size_lines):
            tmp.append([])
            for col in range(self._size_cols):
                tmp[line].append(str(table[col, line]))
        print(
            tabulate(
                tmp, self.headers, showindex=self.line_headers, tablefmt="fancy_grid"
            )
        )

    def resolve(self, show_step=True, iter_limit=10):
        """
        
        :param show_step: 
        :param iter_limit: 
        :return: 
        """
        count = 0
        while max(self.extract_max_func()) > 0:
            count += 1
            self.next_step()
            if show_step:
                print(f"STEP {count}")
                self.print_table(self._table)
            if count >= iter_limit:
                break
        return tuple(self.extract_constants())


if __name__ == '__main__':
    import doctest
    doctest.testmod()
