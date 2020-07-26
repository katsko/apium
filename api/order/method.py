import jrlib
from jrlib import jf


class Auth(jrlib.Method):
    token = jf.Str(order=-100)

    @jrlib.order(-100)
    def __middle(self):
        print('auth middle')
        if not self.token == '1':
            raise ValueError('Access denied')

    def validate_token(self, value):
        print('ext validator (token) -100')


class MyStr1(jf.Str):
    def validate(self):
        super(MyStr1, self).validate()
        print('validator in field (brand) -10')


class MyStr2(jf.Str):
    def validate(self):
        super(MyStr2, self).validate()
        print('validator in field (model) -15')


class CarField(jf.Obj):
    brand = MyStr1(order=-10)
    model = MyStr2(order=-15)

    def validate_brand(self, value):
        print('ext validator (brand) -10')

    def validate_model(self, value):
        print('ext validator (model) -15')

    def validate(self):
        super(CarField, self).validate()
        print('validator in field (car) 4')


class Order(Auth):
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
    about = jf.Str()

    def execute(self):
        print('execute')
        print(type(self.msg))
        print('/execute')
        return self.msg

    def validate_msg(self, value):
        print('ext validator (msg) -')

    def validate_about(self, value):
        print('ext validator (about) -')

    def validate_city(self, value):
        print('ext validator (city) 5')

    def validate_car(self, value):
        print('ext validator (car) 4')

    def validate_passenger(self, value):
        print('ext validator (passenger) 2')
