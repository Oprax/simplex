from fractions import Fraction

from tabulate import tabulate


__all__ = ["Simplex"]


class Simplex(object):
    """
    Class to solve a linear optimization problem using simplex algorithm.
    """

    def __init__(self, eqs=tuple(), constants=tuple(), max_func=tuple()):
        """
        Setup and fill table with information from user.

        :param eqs: List of equations (also call constraints),
                    each equation is also a iterable.
        :param constants: List of constant, must have the same size of eqs
        :param max_func: Maximize objective function,
                         must have the same size of an equation
        :type eqs: iterable
        :type constants: iterable
        :type max_func: iterable

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

        self._headers = []
        for i in range(self._size_eq):
            self._headers.append("x{}".format(i + 1))
        for i in range(self._nb_eq):
            self._headers.append("e{}".format(i + 1))
        self._headers.append("C")
        self._headers.append("R")

        self._line_headers = []
        for i in range(self._nb_eq):
            self._line_headers.append("e{}".format(i + 1))
        self._line_headers.append("F")

        self._table = {}
        for line in range(self._size_lines):
            for col in range(self._size_cols):
                self._table[col, line] = Fraction(0)
        self._need_min = False
        for line, eq in enumerate(self._eqs):
            self._table[self._size_eq + line, line] = 1
            for col, part in enumerate(eq):
                if part < 0:
                    self._need_min = True
                self._table[col, line] = Fraction(part)
        for col, part in enumerate(self._max_func):
            if self._need_min:
                self._table[col, self._nb_eq] = Fraction(part * -1)
            else:
                self._table[col, self._nb_eq] = Fraction(part)
        for line, part in enumerate(self._constants):
            self._table[self._size_eq + self._nb_eq, line] = Fraction(part)

    @property
    def table(self):
        """
        :return: Dictionary representing table,
                 use tuple(col, line) as key.
        :rtype: dict
        """
        return dict(self._table)

    def _next_step(self):
        """
        Compute the next step table
        """
        col_pivot, line_pivot = self._compute_ratio(col_pivot=self._compute_col_pivot())
        self._line_headers.insert(0, self._headers[col_pivot])
        self._line_headers.pop()
        self._line_headers[self._size_lines - 1] = "F"
        tmp_table = dict(self._table)
        pivot = Fraction(self._table[col_pivot, line_pivot])
        print("({}, {}) = {}".format(col_pivot, line_pivot, pivot))

        for line in range(self._size_lines):
            for col in range(self._size_cols - 1):
                tmp_table[col, line] = self._table[col, line] - (
                    (self._table[col_pivot, line] * self._table[col, line_pivot])
                    / pivot
                )

        for line in range(self._size_lines):
            tmp_table[col_pivot, line] = 0
        tmp_table[col_pivot, line_pivot] = 1
        for col in range(self._size_cols - 1):
            if col != col_pivot:
                tmp_table[col, line_pivot] = self._table[col, line_pivot] / pivot
        self._table = dict(tmp_table)

    def _extract_max_func(self):
        """
        Extract maximize function from table.
        :return: List representing maximize objective function.
        :rtype: list
        """
        line = self._nb_eq
        max_func = []
        for i in range(self._size_cols - 2):
            max_func.append(self._table[i, line])
        return max_func

    def _extract_constants(self):
        """
        Extract constants from table.
        :return: List of each constants
        :rtype: list
        """
        tmp = []
        for line in range(self._nb_eq):
            tmp.append(float(self._table[self._size_cols - 2, line]))
        return tmp

    def _compute_col_pivot(self):
        """
        Compute the col index of pivot, which is the col with the biggest number in maximize function.
        :return: Index of the pivot's column
        :rtype: int
        """
        tmp = self._extract_max_func()
        if self._need_min:
            return tmp.index(min(tmp))
        return tmp.index(max(tmp))

    def _compute_ratio(self, col_pivot=0):
        """
        Compute column ration, and with ratio compute the pivot's line.
        :param col_pivot: Index of the pivot column
        :type col_pivot: int
        :return: Position of pivot represent by tuple(col, line)
        :rtype: tuple
        """
        tmp = []
        for line in range(self._size_lines - 1):
            ratio = (
                self._table[self._size_cols - 2, line] / self._table[col_pivot, line]
            )
            tmp.append(ratio)
            self._table[self._size_cols - 1, line] = Fraction(ratio)
        m = min(tmp)
        while m < 0:
            tmp.remove(m)
            m = min(tmp)
        return col_pivot, tmp.index(m)

    def print_table(self, table):
        """
        Function to print table with a nice formatting.
        :param table: Table to show
        :type table: dict
        """
        tmp = []
        for line in range(self._size_lines):
            tmp.append([])
            for col in range(self._size_cols):
                tmp[line].append(str(table[col, line]))
        print(
            tabulate(
                tmp, self._headers, showindex=self._line_headers, tablefmt="fancy_grid"
            )
        )

    def resolve(self, show_step=True, iter_limit=10):
        """
        Run algorithm until the final step.
        :param show_step: Show table between each step.
        :param iter_limit: Number max of iteration.
        :type show_step: bool
        :type iter_limit: int
        :return: List of unknown found by simplex, representing by tuple(x1, x2, x3, etc)
        :rtype: tuple
        """
        count = 0
        if show_step:
            print("INITAL TABLE")
            self.print_table(self._table)
        while self._is_end():
            count += 1
            self._next_step()
            if show_step:
                print("STEP {}".format(count))
                self.print_table(self._table)
            if count >= iter_limit:
                break
        res = self._extract_constants()
        index = list(self._line_headers)
        index.pop()
        index = [int(x[1]) - 1 for x in index]
        if len(index) != len(res):
            raise ValueError("Number of unknow and number of ")
        tmp = [0] * len(res)
        for i, v in enumerate(res):
            tmp[index[i]] = v
        return tuple(tmp)

    def _is_end(self):
        """
        Determine if simplex is finish (or not)
        :return: boolean indicate if simplex is finish (or not)
        :rtype: bool
        """
        if self._need_min:
            return min(self._extract_max_func()) < 0
        else:
            return max(self._extract_max_func()) > 0


if __name__ == "__main__":
    import doctest

    doctest.testmod()
