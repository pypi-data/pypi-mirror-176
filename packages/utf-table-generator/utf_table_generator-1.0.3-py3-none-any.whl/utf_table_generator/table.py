class Table:
    VERTICAL = '║'
    HORIZONTAL = '═'
    CROSS_DOWN = '╦'
    CROSS_UP = '╩'
    CROSS = '╬'
    CROSS_LEFT = '╠'
    CROSS_RIGHT = '╣'
    CORNER_TOP_RIGHT = '╗'
    CORNER_TOP_LEFT = '╔'
    CORNER_BOTTOM_RIGHT = '╝'
    CORNER_BOTTOM_LEFT = '╚'

    def __init__(self, titles, variables, precision=5):
        self.titles = titles
        self.precision = precision
        self.formats = []
        self.numbers = []
        for var, title in zip(variables, self.titles):
            f, n = {
                int: self.int,
                float: self.float,
                bool: self.bool,
                str: self.str
            }.get(type(var), self.other)(var, title)
            self.formats.append(f)
            self.numbers.append(n)

    def get_header(self):
        f = self.get_border(
            self.CROSS_DOWN, self.CORNER_TOP_LEFT, self.CORNER_TOP_RIGHT
        )
        title_formats = [f'%{n}s ' for n in self.numbers]
        f += '\n' + self.get_row(title_formats, self.titles)
        f += '\n' + self.get_border(
            self.CROSS, self.CROSS_LEFT, self.CROSS_RIGHT
        )
        return f

    def get_footer(self):
        return self.get_border(
            self.CROSS_UP, self.CORNER_BOTTOM_LEFT, self.CORNER_BOTTOM_RIGHT
        )

    def get_border(self, delimiter_char, l_char, r_char):
        delimiter = (' + "' + delimiter_char + '" + ')
        mid = delimiter.join([
            f'"{self.HORIZONTAL}" * {n + 1}'
            for n in self.numbers
        ])
        return f'print("{l_char}" + {mid} + "{r_char}")'

    def get_row(self, formats=None, values=None):
        if formats is None:
            formats = self.formats
        values = '"' + '", "'.join(map(str, values)) + '"' if values else ''
        f = self.VERTICAL + self.VERTICAL.join(formats) + self.VERTICAL
        row = 'print("{}" % ({}))'
        row = row.format(f, values)
        return row

    def get_code(self):
        return '\n'.join([self.get_header(), self.get_row(), self.get_footer()])

    def __str__(self):
        return self.get_code()

    def float(self, value, title):
        n = self.precision + len(str(int(value))) + 3
        n = max(n, len(title))
        n += 1
        return f'%{n}.{self.precision}f ', n

    @staticmethod
    def int(value, title):
        n = len(str(value)) + 1
        n = max(n, len(str(title)))
        n += 1
        return f'%{n}d ', n

    @staticmethod
    def str(value, title):
        n = len(value) + 1
        n = max(n, len(str(title)))
        n += 1
        return f'%{n}s ', n

    def bool(self, value, title):
        return self.str(str(value), title)
    
    def other(self, value, title):
        return self.str(str(value), title)
