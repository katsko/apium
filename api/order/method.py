import jrlib
from jrlib import jf


class Order(jrlib.Method):
    msg = jf.Str(required=True)
    city = jf.Str(required=True, order=1)

    def execute(self):
        print('execute')
        print(type(self.msg))
        print('/execute')
        return self.msg
