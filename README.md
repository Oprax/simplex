Simplex
=======

[![GitHub license](https://img.shields.io/github/license/Oprax/simplex.svg?style=flat-square)](https://github.com/Oprax/simplex/blob/master/LICENSE)
[![pipeline status](https://gitlab.com/Oprax/simplex/badges/master/pipeline.svg)](https://gitlab.com/Oprax/simplex/commits/master)
[![PyPI](https://img.shields.io/pypi/v/ro-simplex.svg?style=flat-square)](https://pypi.org/project/ro-simplex/)


Solver using simplex algorithm for linear optimization problems.

# Example

Problem :
```
15x+7.5y+5z <= 315
2x+3y+2z <= 110
x+y+z <= 50
Max(F)=200x+150y+120z
```
Give :
```python
Simplex(
    eqs=(
        (15, 7.5, 5),
        (2, 3, 2),
        (1, 1, 1)
    ),
    constants=(315, 110, 50),
    max_func=(200, 150, 120),
)
```

# Resources

 - [Saïd Chermak (French Video)](https://www.youtube.com/watch?v=nADa_AXVrA8)
 - [Tutorial (English)](https://www.zweigmedia.com/RealWorld/tutorialsf4/framesSimplex.html)
