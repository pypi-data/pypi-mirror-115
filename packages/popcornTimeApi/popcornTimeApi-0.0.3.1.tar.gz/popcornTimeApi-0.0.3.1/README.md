# Popcorntime Api

Library to use the api of popcorntime in python

## Getting started

Install the library from git with `pip install popcornTimeApi`

```python
from popcorntimeapi.Popcorn import PopcornTimeApi

popcorn = PopcornTimeApi()

random_movie = popcorn.get_random()

print(random_movie.title)

```

## How to update package

(Python3 just to be sure)

1. Update package version number in `setup.py`
2. `python3.7 setup.py sdist`
3. `python3.7 -m twine upload dist/*`
