class Block:

    def __init__(self, ctr_x, ctr_y):
        self.ctr_x = ctr_x
        self.ctr_y = ctr_y

    def __call__(self, typ):
        self.typ = typ

    def interact(self, cx, cy, dx, dy):

        typ = self.typ
        if typ == 'N':
            return [(cx + dx, cy + dy, dx, dy)]
        elif typ == 'A':
            if cx % 2 == 1:
                return [(cx, cy, dx, -dy)]
            else:
                return [(cx, cy, -dx, dy)]
        elif typ == 'B':
            return 'END'
        elif typ == 'C':
            if cx % 2 == 1:
                return [(cx, cy, dx, -dy), (cx + dx, cy + dy, dx, dy)]
            else:
                return [(cx, cy, -dx, dy), (cx + dx, cy + dy, dx, dy)]
        else:
            pass