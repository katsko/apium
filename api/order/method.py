import jrlib
from jrlib import jf


class CarField(jf.Obj):
    brand = jf.Str(order=-10)
    model = jf.Str(order=-15)


class Order(jrlib.Method):
    msg = jf.Str(required=True)
    city = jf.Str(required=True, order=5)
    car = CarField(order=4)
    passenger = jf.Obj(
        fields=dict(
            name=jf.Str(order=40),
            age=jf.Int(order=30)
        ),
        order=2
    )

    def execute(self):
        print('execute')
        print(type(self.msg))
        print('/execute')
        return self.msg
