
try:
    import _dank
except ImportError:
    print('dank module failed to load, check your installation')


class DankEncoder:
    def __init__(self):
        enc = _dank.DFAEncoder('(a|b)+', 5)
        print(f'DankEncoder constructor: {enc.unrank(0)}')
