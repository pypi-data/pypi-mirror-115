
try:
    from ._dank import dank
except ImportError:
    print('dank module failed to load, check your installation')


class DankEncoder:
    def __init__(self):
        enc = dank.DFAEncoder('(a|b)+', 5)
        print(f'DankEncoder constructor: {enc.unrank(0)}')
