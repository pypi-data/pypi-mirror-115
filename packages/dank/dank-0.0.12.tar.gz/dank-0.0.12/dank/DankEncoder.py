
try:
    from ._dank import DFA, DFAEncoder
except ImportError as ex:
    print(f'dank module failed to load: {ex}')


class DankEncoder:
    def __init__(self):
        enc = DFAEncoder('(a|b)+', 5)
        print(f'DankEncoder constructor: {enc.unrank(0)}')
