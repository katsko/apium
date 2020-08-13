import jrlib
from jrlib import jf


class AuthLogBefore(jrlib.Method):
    @jrlib.order(-100)
    def __middle(self):
        print("auth log before")


class AuthCheck(AuthLogBefore):
    token = jf.Str(order=-100)

    @jrlib.order(-100)
    def __middle(self):
        print("auth middle")
        if not self.token == "1":
            raise ValueError("Access denied")

    def validate_token(self, value):
        print("ext validator (token) -100")


class Auth(AuthCheck):
    @jrlib.order(-100)
    def __middle(self):
        print("auth log after")


class MyStr1(jf.Str):
    def validate(self):
        super(MyStr1, self).validate()
        print("validator in field (brand) -10")


class MyStr2(jf.Str):
    def validate(self):
        super(MyStr2, self).validate()
        print("validator in field (model) -15")


class CarField(jf.Obj):
    brand = MyStr1(order=-10)
    model = MyStr2(order=-15)

    def validate_brand(self, value):
        print("ext validator (brand) -10")

    def validate_model(self, value):
        print("ext validator (model) -15")

    def validate(self):
        super(CarField, self).validate()
        print("validator in field (car) 4")


class CarMiddle1(jrlib.Method):
    @jrlib.order(40)
    def __middle(self):
        print("car middle 1")


class CarMiddle2(jrlib.Method):
    @jrlib.order(41)
    def __middle(self):
        print("car middle 2")


class PassengerMiddle(jrlib.Method):
    @jrlib.order(20)
    def __middle(self):
        print("passenger middle")


class FirstOrderMiddle(jrlib.Method):
    @jrlib.order(-100000)
    def __middle(self):
        print("first order middle -100000")


class Last2Middle(jrlib.Method):

    # run this middleware after middlewares without order
    @jrlib.order_last
    def __middle(self):
        print("last2 middle")


class Last1Middle(jrlib.Method):

    # run this middleware after middlewares without order
    @jrlib.order_last
    def __middle(self):
        print("last1 middle")


class First1Middle(jrlib.Method):

    # run this middleware before middlewares without order
    @jrlib.order_first
    def __middle(self):
        print("first1 middle")


class First2Middle(jrlib.Method):

    # run this middleware before middlewares without order
    @jrlib.order_first
    def __middle(self):
        print("first2 middle")


class BigOrderMiddle(jrlib.Method):
    @jrlib.order(1000000)
    def __middle(self):
        print("big order middle 1000000")


class MinusBigOrderMiddle(jrlib.Method):
    @jrlib.order(-1000000)
    def __middle(self):
        print("minus big order middle -1000000")


class Middle1WoutOrder(jrlib.Method):

    # run after ordered middlewares but before @order_last
    def __middle(self):
        print("without order middle 1")


class Middle2WoutOrder(jrlib.Method):

    # run after ordered middlewares but before @order_last
    def __middle(self):
        print("without order middle 2")


class Order(
    BigOrderMiddle,
    MinusBigOrderMiddle,
    FirstOrderMiddle,
    Auth,
    CarMiddle1,
    Last1Middle,
    CarMiddle2,
    PassengerMiddle,
    Middle1WoutOrder,
    Last2Middle,
    Middle2WoutOrder,
    First1Middle,
    First2Middle,
):
    msg = jf.Str(required=True)
    city = jf.Str(required=True, order=50)
    car = CarField(order=40)
    passenger = jf.Obj(
        fields=dict(name=jf.Str(order=400), age=jf.Int(order=300)), order=20
    )
    about = jf.Str()

    def execute(self):
        return self.msg

    def validate_msg(self, value):
        print("ext validator (msg) -")

    def validate_about(self, value):
        print("ext validator (about) -")

    def validate_city(self, value):
        print("ext validator (city) 5")

    def validate_car(self, value):
        print("ext validator (car) 4")

    def validate_passenger(self, value):
        print("ext validator (passenger) 2")
