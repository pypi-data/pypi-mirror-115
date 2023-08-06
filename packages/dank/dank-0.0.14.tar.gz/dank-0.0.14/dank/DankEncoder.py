import re

try:
    from ._dank import DFA, DFAEncoder
except ImportError as ex:
    print(f'dank module failed to load: {ex}')


class DankEncoder:
    def __init__(self, regex: str, fixed_slice: int):
        self.regex = self.preprocess(regex)
        self.fixed_slice = fixed_slice
        self._encoder = DFAEncoder(self.regex, fixed_slice)

    def num_words(self, low: int, high: int) -> int:
        return self._encoder.num_words(low, high)

    def set_fixed_slice(self, n: int):
        self._encoder.set_fixed_slice(n)

    def get_fixed_slice(self) -> int:
        return self._encoder.get_fixed_slice()

    def unrank(self, n: int) -> bytes:
        return self._encoder.unrank(n)

    def rank(self, s: bytes) -> int:
        return self._encoder.rank(s)

    def range_expand(self, range_expr: str) -> str:
        if not '-' in range_expr:
            return None
        start, end = range_expr.split('-')
        if ord(end) < ord(start):
            return None
        elements = [chr(i) for i in range(ord(start), ord(end)+1)]
        return f'({"|".join(elements)})' 

    def preprocess(self, regex: str) -> str:
        # First pass, expand all (simple) character classes
        char_classes = re.findall(r'\[(.*?)\]', regex)
        for cc in char_classes:
            if re.match(r'^.\-.$', cc):
                regex = regex.replace(f'[{cc}]', self.range_expand(cc))
            else:
                raise Exception('preprocess: unsupported regex given')
        # Second pass, expand all repetition operators
        ret = regex
        parse_stack, expr_stack, rep_stack = [], [], []
        for i, e in enumerate(regex):
            if e == '(':
                parse_stack.append(i)
            elif e == ')':
                start = parse_stack.pop()
                expr = regex[start+1:i]
                expr_stack.append(expr)
            elif e == '{':
                rep_stack.append(i)
            elif e == '}':
                expr = expr_stack.pop()
                start = rep_stack.pop()
                repe = regex[start+1:i]
                if re.match(r'^(\d)$', repe):
                    n = int(re.match(r'^(\d)$', repe)[0])
                    e = f'({expr})'
                    ret = ret.replace(e, e*n)
                    ret = ret.replace('{%s}' % n, '')
                elif re.match(r'^(\d),$', repe):
                    n = int(re.match(r'^(\d),$', repe)[0][:-1])
                    e = f'({expr})'
                    ret = ret.replace(e, e*(n+1) + '*')
                    ret = ret.replace('{%s,}' % n, '')
                elif re.match(r'^(\d),(\d)$', repe):
                    i, j = map(int, re.match(r'^(\d),(\d)$', repe)[0].split(','))
                    e = f'({expr})'
                    r = f'({"|".join(["(" + e*k + ")" for k in range(j,i-1,-1)])})'
                    ret = ret.replace(e, r)
                    ret = ret.replace('{%s,%s}' % (i, j), '')
        return ret
